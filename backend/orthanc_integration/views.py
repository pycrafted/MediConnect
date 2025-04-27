import requests
import logging
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from django.http import HttpResponse, FileResponse
from datetime import datetime
from core.models import Patient, DicomImage
from core.serializers import DicomImageSerializer
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser

logger = logging.getLogger(__name__)

# Configuration Orthanc depuis settings
ORTHANC_URL = settings.ORTHANC_URL
ORTHANC_AUTH = settings.ORTHANC_AUTH

def get_orthanc_response(url, method='get', auth=ORTHANC_AUTH, files=None, params=None):
    """Utilitaire pour effectuer des requêtes HTTP vers Orthanc."""
    try:
        response = requests.request(
            method=method,
            url=url,
            auth=auth,
            files=files,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(f"Erreur requête Orthanc {url}: {str(e)}")
        raise

def get_instance_id_from_response(response):
    """Extrait l'instance ID d'une réponse Orthanc ou récupère la dernière instance."""
    try:
        data = response.json()
        instance_id = data.get('ID')
        if not instance_id:
            raise ValueError("ID d’instance non trouvé dans la réponse")
        return instance_id
    except ValueError as e:
        logger.warning(f"Réponse Orthanc non-JSON ou vide: {str(e)}, récupération dernière instance")
        time.sleep(1)  # Attendre 1 seconde pour s'assurer que l'instance est enregistrée
        instances_response = get_orthanc_response(f'{ORTHANC_URL}/instances')
        instances = instances_response.json()
        if not instances:
            raise ValueError("Aucune instance trouvée")
        return instances[-1]

class OrthancPatientsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Récupère les patients Orthanc associés à l'utilisateur connecté."""
        try:
            user = request.user
            if not user.groups.filter(name='Patient').exists():
                return Response(
                    {'error': 'Accès réservé aux patients'},
                    status=status.HTTP_403_FORBIDDEN
                )

            patient = Patient.objects.get(user=user)
            if not patient.orthanc_id:
                return Response(
                    {'error': 'Aucun ID Orthanc associé'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Récupérer tous les patients Orthanc
            patients_response = get_orthanc_response(f'{ORTHANC_URL}/patients')
            orthanc_patients = patients_response.json()

            # Filtrer pour ne retourner que le patient correspondant
            filtered_patients = []
            if patient.orthanc_id in orthanc_patients:
                patient_response = get_orthanc_response(
                    f'{ORTHANC_URL}/patients/{patient.orthanc_id}'
                )
                patient_details = patient_response.json()
                filtered_patients.append({
                    'id': patient.orthanc_id,
                    'name': patient_details.get('MainDicomTags', {}).get(
                        'PatientName', 'Inconnu'
                    ),
                    'created_at': patient_details.get('LastUpdate', 'Inconnu')
                })

            return Response(filtered_patients, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Profil patient non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        except requests.RequestException:
            return Response(
                {'error': 'Erreur de connexion à Orthanc'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DicomImageView(APIView):
    def get(self, request, instance_id=None):
        if instance_id:
            try:
                dicom_image = DicomImage.objects.get(instance_id=instance_id)
                # Vérifier si l'utilisateur a accès à cette image
                if request.user.is_authenticated:
                    patient = Patient.objects.get(user=request.user)
                    if dicom_image.patient != patient:
                        return Response(
                            {'error': 'Accès non autorisé à cette image'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                # Si non authentifié, permettre l'accès (pour la balise <img>)
                return FileResponse(dicom_image.image, content_type='image/png')
            except DicomImage.DoesNotExist:
                return Response({'error': 'Image non trouvée'}, status=status.HTTP_404_NOT_FOUND)
            except Patient.DoesNotExist:
                return Response(
                    {'error': 'Profil patient non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentification requise pour lister les images'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            try:
                patient = Patient.objects.get(user=request.user)
                dicom_images = DicomImage.objects.filter(patient=patient)
                serializer = DicomImageSerializer(dicom_images, many=True)
                return Response(serializer.data)
            except Patient.DoesNotExist:
                return Response(
                    {'error': 'Profil patient non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )

class DicomToPngView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            user = request.user
            patient = Patient.objects.get(user=user)
            file = request.FILES.get('file')
            description = request.data.get('description', '')

            if not file:
                return Response(
                    {'error': 'Aucun fichier fourni'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Uploader vers Orthanc
            response = get_orthanc_response(
                f'{ORTHANC_URL}/instances',
                method='post',
                files={'file': file}
            )

            # Récupérer l’instance_id
            instance_id = get_instance_id_from_response(response)
            logger.info(f"Dernière instance récupérée: {instance_id}")

            # Vérifier si l’instance existe déjà
            if DicomImage.objects.filter(instance_id=instance_id).exists():
                logger.info(f"Instance {instance_id} déjà enregistrée")
                return Response(
                    {'instance_id': instance_id, 'message': 'Image déjà existante'},
                    status=status.HTTP_200_OK
                )

            # Récupérer l’image PNG rendue depuis Orthanc
            png_response = get_orthanc_response(
                f'{ORTHANC_URL}/instances/{instance_id}/rendered',
                params={'accept': 'image/png'}
            )
            png_data = png_response.content

            # Enregistrer dans PostgreSQL
            dicom_image = DicomImage.objects.create(
                patient=patient,
                instance_id=instance_id,
                description=description,
                image=ContentFile(png_data, name=f"{instance_id}.png")
            )

            # Récupérer les métadonnées Orthanc
            instance_response = get_orthanc_response(f'{ORTHANC_URL}/instances/{instance_id}')
            if instance_response.status_code == 200:
                instance_data = instance_response.json()
                main_dicom_tags = instance_data.get('MainDicomTags', {})
                dicom_image.patient_name = main_dicom_tags.get('PatientName', 'Inconnu')
                dicom_image.study_date = main_dicom_tags.get('StudyDate', 'Inconnu')
                dicom_image.save()

            return Response(
                {'instance_id': instance_id, 'message': 'Upload réussi'},
                status=status.HTTP_200_OK
            )
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Profil patient non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        except (requests.RequestException, ValueError) as e:
            return Response(
                {'error': f'Erreur lors de l’upload: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DicomImageListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Liste les images DICOM d’un patient avec leurs métadonnées."""
        try:
            patient = Patient.objects.get(user=request.user)
            dicom_images = DicomImage.objects.filter(patient=patient).order_by('-uploaded_at')

            image_list = []
            for dicom_image in dicom_images:
                try:
                    instance_response = get_orthanc_response(
                        f'{ORTHANC_URL}/instances/{dicom_image.instance_id}'
                    )
                    instance_data = instance_response.json()
                    main_dicom_tags = instance_data.get('MainDicomTags', {})
                    logger.info(f"MainDicomTags pour instance {dicom_image.instance_id}: {main_dicom_tags}")

                    study_date = main_dicom_tags.get('StudyDate', 'Inconnu')
                    if study_date != 'Inconnu':
                        try:
                            study_date = datetime.strptime(
                                study_date, '%Y%m%d'
                            ).strftime('%d/%m/%Y')
                        except ValueError:
                            logger.warning(f"Format StudyDate invalide pour instance {dicom_image.instance_id}: {study_date}")
                            study_date = 'Inconnu'

                    image_list.append({
                        'instance_id': dicom_image.instance_id,
                        'description': dicom_image.description or 'Aucune',
                        'uploaded_at': dicom_image.uploaded_at,
                        'patient_name': main_dicom_tags.get('PatientName', 'Inconnu'),
                        'study_date': study_date
                    })
                except requests.RequestException as e:
                    logger.error(
                        f"Erreur récupération instance {dicom_image.instance_id}: {str(e)}"
                    )
                    continue

            return Response(image_list, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Profil patient non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )