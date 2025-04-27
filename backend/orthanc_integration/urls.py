from django.urls import path
from .views import OrthancPatientsView, DicomToPngView, DicomImageListView, DicomImageView

urlpatterns = [
    path('patients/', OrthancPatientsView.as_view(), name='orthanc-patients'),
    path('dicom-to-png/', DicomToPngView.as_view(), name='dicom-to-png'),
    path('images/', DicomImageListView.as_view(), name='dicom-images'),
    path('images/<str:instance_id>/', DicomImageView.as_view(), name='dicom-image'),
]