from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import requests
from django.conf import settings
import logging
import pydicom
import numpy as np
from PIL import Image
from django.http import HttpResponse
import os






logger = logging.getLogger(__name__)

class OrthancPatientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Appel à l'API REST d'Orthanc pour lister les patients
            response = requests.get(
                f"{settings.ORTHANC_URL}/patients",
                auth=(settings.ORTHANC_USERNAME, settings.ORTHANC_PASSWORD)
            )
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la requête Orthanc : {str(e)}")
            return Response({"error": "Impossible de récupérer les patients"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



logger = logging.getLogger(__name__)


class DicomToPngView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        temp_path = None  # Initialiser temp_path pour éviter UnboundLocalError
        try:
            # Vérifier si un fichier DICOM est envoyé
            if 'file' not in request.FILES:
                return Response({"error": "Aucun fichier DICOM fourni"}, status=status.HTTP_400_BAD_REQUEST)

            dicom_file = request.FILES['file']

            # Lire le fichier DICOM avec pydicom
            try:
                ds = pydicom.dcmread(dicom_file)
            except Exception as e:
                logger.error(f"Erreur lors de la lecture du fichier DICOM : {str(e)}")
                return Response({"error": "Fichier DICOM invalide"}, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier la présence des données d'image
            if not hasattr(ds, 'PixelData'):
                return Response({"error": "Fichier DICOM sans données d'image"}, status=status.HTTP_400_BAD_REQUEST)

            # Extraire les données de l'image
            try:
                pixel_array = ds.pixel_array
            except Exception as e:
                logger.error(f"Erreur lors de l'extraction des pixels : {str(e)}")
                return Response({"error": f"Impossible d'extraire les données d'image : {str(e)}"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Normaliser les pixels pour une image 8 bits
            pixel_array = (pixel_array - np.min(pixel_array)) / (
                        np.max(pixel_array) - np.min(pixel_array) + 1e-10) * 255
            pixel_array = pixel_array.astype(np.uint8)

            # Convertir en image PNG avec Pillow
            image = Image.fromarray(pixel_array)

            # Sauvegarder temporairement l'image
            temp_dir = os.path.join(settings.BASE_DIR, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, f"{dicom_file.name}.png")
            image.save(temp_path, format='PNG')

            # Lire le fichier PNG et le renvoyer
            with open(temp_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='image/png')
                response['Content-Disposition'] = f'inline; filename="{dicom_file.name}.png"'
                return response

        except Exception as e:
            logger.error(f"Erreur lors de la conversion DICOM en PNG : {str(e)}")
            return Response({"error": f"Erreur lors de la conversion : {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Nettoyer le fichier temporaire uniquement si temp_path est défini
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception as e:
                    logger.error(f"Erreur lors de la suppression du fichier temporaire : {str(e)}")