from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, RendezVous, Médecin
from .serializers import PatientSerializer, RendezVousSerializer, MédecinSerializer

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

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            if request.method == 'GET':
                serializer = self.get_serializer(patient)
                return Response(serializer.data)
            elif request.method == 'PATCH':
                serializer = self.get_serializer(patient, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({'error': 'Profil patient non trouvé'}, status=404)

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Patient').exists():
            return RendezVous.objects.filter(patient__user=user)
        elif user.groups.filter(name='Médecin').exists():
            return RendezVous.objects.filter(médecin__user=user)
        return RendezVous.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.groups.filter(name='Patient').exists():
            try:
                patient = Patient.objects.get(user=user)
                serializer.save(patient=patient)
            except Patient.DoesNotExist:
                raise serializers.ValidationError("Profil patient non trouvé.")
        else:
            raise serializersValidationError("Seuls les patients peuvent créer des rendez-vous.")

class MédecinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Médecin.objects.all()
    serializer_class = MédecinSerializer
    permission_classes = [permissions.IsAuthenticated]