from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import requests
from django.conf import settings
import logging

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