from rest_framework import serializers
from .models import Patient, Médecin, RendezVous, DicomImage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class DicomImageSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DicomImage
        fields = ['instance_id', 'patient', 'description', 'uploaded_at', 'image']

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'insurance_number': {'write_only': True}
        }

    def validate(self, data):
        user = self.context['request'].user
        if not user.groups.filter(name__in=['Médecin', 'Assistant']).exists():
            raise serializers.ValidationError("Seuls les médecins/assistants peuvent modifier les patients")
        return data

class MédecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Médecin
        fields = ['id', 'user', 'specialty', 'license_number', 'hôpital']

class RendezVousSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    médecin = serializers.PrimaryKeyRelatedField(queryset=Médecin.objects.all(), write_only=True)
    médecin_display = serializers.StringRelatedField(source='médecin', read_only=True)

    class Meta:
        model = RendezVous
        fields = ['id', 'patient', 'médecin', 'médecin_display', 'date', 'reason', 'created_at']