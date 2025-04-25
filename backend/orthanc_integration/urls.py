from django.urls import path
from .views import OrthancPatientsView, DicomToPngView

urlpatterns = [
    path('patients/', OrthancPatientsView.as_view(), name='orthanc-patients'),
    path('dicom-to-png/', DicomToPngView.as_view(), name='dicom-to-png'),
]