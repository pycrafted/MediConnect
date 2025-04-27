from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class Hôpital(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    téléphone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    )
    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    emergency_phone = models.CharField(max_length=20, null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    current_medications = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    insurance_number = models.CharField(max_length=50, null=True, blank=True)
    orthanc_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            age = today.year - self.date_of_birth.year
            if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            return age
        return None

    def has_complete_profile(self):
        required_fields = ['date_of_birth', 'gender', 'phone', 'address', 'city', 'postal_code']
        return all(getattr(self, field) for field in required_fields)

class Médecin(models.Model):
    SPECIALTY_CHOICES = (
        ('GENERALISTE', 'Médecine générale'),
        ('CARDIOLOGUE', 'Cardiologie'),
        ('DERMATOLOGUE', 'Dermatologie'),
        ('PEDIATRE', 'Pédiatrie'),
        # Ajoute d'autres spécialités si nécessaire
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)
    license_number = models.CharField(max_length=50)
    hôpital = models.ForeignKey(Hôpital, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(null=True, blank=True)
    patients = models.ManyToManyField(Patient, related_name='médecins')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr {self.user.first_name} {self.user.last_name}"

class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hôpital = models.ForeignKey(Hôpital, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    médecin = models.ForeignKey(Médecin, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rendez-vous de {self.patient} avec {self.médecin} le {self.date}"

    def clean(self):
        if self.date < timezone.now():
            raise ValidationError("La date du rendez-vous ne peut pas être dans le passé.")


class DicomImage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='dicom_images')
    instance_id = models.CharField(max_length=255, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='dicom_images/', null=True, blank=True)  # Nouveau champ

    def __str__(self):
        return f"Image DICOM {self.instance_id} pour {self.patient}"