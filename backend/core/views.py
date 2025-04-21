from rest_framework import viewsets, permissions
from .models import Patient, Médecin, RendezVous
from .serializers import PatientSerializer
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import action
from rest_framework.response import Response

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Médecin').exists():
            return Patient.objects.filter(médecins__user=user)
        elif user.groups.filter(name='Patient').exists():
            return Patient.objects.filter(user=user)
        return Patient.objects.none()

    @action(detail=False, methods=['get'])
    def me(self, request):
        patient = Patient.objects.get(user=request.user)
        serializer = self.get_serializer(patient)
        return Response(serializer.data)