from rest_framework import serializers
from .models import Patient, Médecin, RendezVous
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'insurance_number': {'write_only': True}  # Masqué en lecture
        }

    def validate(self, data):
        user = self.context['request'].user
        if not user.groups.filter(name__in=['Médecin', 'Assistant']).exists():
            raise serializers.ValidationError("Seuls les médecins/assistants peuvent modifier les patients")
        return data