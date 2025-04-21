from django.urls import path
from .views import OrthancPatientsView

urlpatterns = [
    path('patients/', OrthancPatientsView.as_view(), name='orthanc-patients'),
]