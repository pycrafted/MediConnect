from django.urls import path
from .views import OrthancPatientsView, OrthancInstanceFileView

urlpatterns = [
    path('patients/', OrthancPatientsView.as_view(), name='orthanc-patients'),
    path('instances/<str:instance_id>/file/', OrthancInstanceFileView.as_view(), name='orthanc-instance-file'),
]