import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from core.models import Patient, DicomImage
import logging
import time
import json

logger = logging.getLogger(__name__)

ORTHANC_URL = 'http://localhost:8042'
ORTHANC_AUTH = ('mediconnect', 'securepassword123')

class OrthancPatientsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if not user.groups.filter(name='Patient').exists():
                return Response({'error': 'Seuls les patients peuvent accéder à cette ressource'}, status=status.HTTP_403_FORBIDDEN)

            patient = Patient.objects.get(user=user)
            if not patient.orthanc_id:
                return Response({'error': 'Aucun ID Orthanc associé au patient'}, status=status.HTTP_404_NOT_FOUND)

            response = requests.get(f'{ORTHANC_URL}/patients', auth=ORTHANC_AUTH)
            response.raise_for_status()
            orthanc_patients = response.json()

            filtered_patients = []
            for patient_id in orthanc_patients:
                if patient_id == patient.orthanc_id:
                    patient_details = requests.get(f'{ORTHANC_URL}/patients/{patient_id}', auth=ORTHANC_AUTH).json()
                    filtered_patients.append({
                        'id': patient_id,
                        'name': patient_details.get('MainDicomTags', {}).get('PatientName', 'Inconnu'),
                        'created_at': patient_details.get('LastUpdate', 'Inconnu')
                    })

            return Response(filtered_patients, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({'error': 'Profil patient non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except requests.RequestException as e:
            logger.error(f"Erreur Orthanc: {str(e)}")
            return Response({'error': 'Erreur lors de la connexion à Orthanc'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DicomToPngView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        instance_id = request.query_params.get('id')
        if not instance_id:
            return Response({'error': 'ID de l’instance requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.get(
                f'{ORTHANC_URL}/instances/{instance_id}/rendered',
                auth=ORTHANC_AUTH
            )
            response.raise_for_status()
            return Response(response.content, status=status.HTTP_200_OK, content_type='image/png')
        except requests.RequestException as e:
            logger.error(f"Erreur récupération PNG: {str(e)}")
            return Response({'error': 'Erreur lors de la récupération de l’image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        file = request.FILES.get('file')
        description = request.data.get('description', '')
        if not file:
            return Response({'error': 'Aucun fichier fourni'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user
            patient = Patient.objects.get(user=user)

            if not file.name.lower().endswith('.dcm'):
                return Response({'error': 'Le fichier doit être au format DICOM (.dcm)'}, status=status.HTTP_400_BAD_REQUEST)

            # Uploader vers Orthanc
            response = requests.post(
                f'{ORTHANC_URL}/instances',
                auth=ORTHANC_AUTH,
                files={'file': (file.name, file, 'application/dicom')}
            )
            response.raise_for_status()

            # Débogage : Logger la réponse brute
            logger.debug(f"Réponse Orthanc brute: {response.text}")

            # Si la réponse est vide, récupérer la dernière instance
            instance_id = None
            try:
                instance_data = response.json()
                instance_id = instance_data.get('ID')
                if not instance_id:
                    raise ValueError('ID de l’instance manquant dans la réponse')
            except (ValueError, json.JSONDecodeError) as e:
                logger.warning(f"Réponse non-JSON ou vide: {str(e)}, tentative de récupération de la dernière instance")
                # Attendre brièvement pour s'assurer que l'instance est indexée
                time.sleep(1)
                # Récupérer la liste des instances
                instances_response = requests.get(f'{ORTHANC_URL}/instances', auth=ORTHANC_AUTH)
                instances_response.raise_for_status()
                instances = instances_response.json()
                if instances:
                    instance_id = instances[0]  # Prendre la première (dernière ajoutée)
                    logger.debug(f"Dernière instance récupérée: {instance_id}")
                else:
                    logger.error("Aucune instance trouvée dans Orthanc")
                    return Response({'error': 'Aucune instance trouvée après upload'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Mettre à jour orthanc_id si vide
            if not patient.orthanc_id:
                instance_details = requests.get(f'{ORTHANC_URL}/instances/{instance_id}', auth=ORTHANC_AUTH).json()
                patient.orthanc_id = instance_details.get('ParentPatient')
                patient.save()

            # Enregistrer l’image dans DicomImage
            DicomImage.objects.create(
                patient=patient,
                instance_id=instance_id,
                description=description
            )

            # Retourner l’instance_id et un message
            return Response({
                'instance_id': instance_id,
                'message': 'Image DICOM uploadée avec succès'
            }, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({'error': 'Profil patient non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        except requests.RequestException as e:
            logger.error(f"Erreur upload DICOM: {str(e)}")
            return Response({'error': 'Erreur lors du traitement du fichier DICOM'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Erreur inattendue: {str(e)}")
            return Response({'error': f'Erreur inattendue lors de l’upload: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DicomImageListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            patient = Patient.objects.get(user=user)
            dicom_images = DicomImage.objects.filter(patient=patient).order_by('-uploaded_at')

            image_list = []
            for dicom_image in dicom_images:
                try:
                    # Récupérer les détails de l’instance
                    instance_response = requests.get(
                        f'{ORTHANC_URL}/instances/{dicom_image.instance_id}',
                        auth=ORTHANC_AUTH
                    )
                    instance_response.raise_for_status()
                    instance_data = instance_response.json()

                    image_list.append({
                        'instance_id': dicom_image.instance_id,
                        'description': dicom_image.description,
                        'uploaded_at': dicom_image.uploaded_at,
                        'patient_name': instance_data.get('MainDicomTags', {}).get('PatientName', 'Inconnu'),
                        'study_date': instance_data.get('MainDicomTags', {}).get('StudyDate', 'Inconnu')
                    })
                except requests.RequestException as e:
                    logger.error(f"Erreur récupération instance {dicom_image.instance_id}: {str(e)}")
                    continue

            return Response(image_list, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({'error': 'Profil patient non trouvé'}, status=status.HTTP_404_NOT_FOUND)