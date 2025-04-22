from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class OrthancPatientsView(APIView):
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

class OrthancInstanceFileView(APIView):
    def get(self, request, instance_id):
        try:
            # Appel à Orthanc pour récupérer le fichier DICOM
            response = requests.get(
                f"{settings.ORTHANC_URL}/instances/{instance_id}/file",
                auth=(settings.ORTHANC_USERNAME, settings.ORTHANC_PASSWORD),
                stream=True
            )
            response.raise_for_status()

            # Créer une réponse HTTP avec le contenu du fichier DICOM
            http_response = HttpResponse(
                content=response.content,
                content_type='application/dicom'
            )
            # Ajouter les en-têtes CORS
            http_response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return http_response
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération du fichier DICOM : {str(e)}")
            return Response({"error": "Impossible de récupérer le fichier DICOM"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)