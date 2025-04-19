from django.db import models
from django.contrib.auth.models import User
import logging

# Configurer le logger
logger = logging.getLogger(__name__)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    medical_history = models.TextField(blank=True)
    insurance_number = models.CharField(max_length=50, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_name = self.user.first_name or 'Unknown'
        last_name = self.user.last_name or 'Unknown'
        logger.info(f'[Patient] Accès au patient : {first_name} {last_name} (ID: {self.id}, User ID: {self.user.id})')
        logger.debug(f'[Patient] Valeurs brutes - first_name: {self.user.first_name}, last_name: {self.user.last_name}')
        if not self.user.first_name or not self.user.last_name:
            logger.warning(f'[Patient] Noms manquants pour User ID: {self.user.id}')
        return f"{first_name} {last_name}"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

class Médecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='médecin_profile')
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    patients = models.ManyToManyField(Patient, related_name="médecins", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_name = self.user.first_name or 'Unknown'
        last_name = self.user.last_name or 'Unknown'
        logger.info(f'[Médecin] Accès au médecin : {first_name} {last_name} (ID: {self.id}, User ID: {self.user.id})')
        logger.debug(f'[Médecin] Valeurs brutes - first_name: {self.user.first_name}, last_name: {self.user.last_name}')
        if not self.user.first_name or not self.user.last_name:
            logger.warning(f'[Médecin] Noms manquants pour User ID: {self.user.id}')
        return f"Dr {first_name} {last_name}"

    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"

class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='assistant_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_name = self.user.first_name or 'Unknown'
        last_name = self.user.last_name or 'Unknown'
        logger.info(f'[Assistant] Accès à l’assistant : {first_name} {last_name} (ID: {self.id}, User ID: {self.user.id})')
        logger.debug(f'[Assistant] Valeurs brutes - first_name: {self.user.first_name}, last_name: {self.user.last_name}')
        if not self.user.first_name or not self.user.last_name:
            logger.warning(f'[Assistant] Noms manquants pour User ID: {self.user.id}')
        return f"{first_name} {last_name}"

    class Meta:
        verbose_name = "Assistant"
        verbose_name_plural = "Assistants"

class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendez_vous')
    médecin = models.ForeignKey(Médecin, on_delete=models.CASCADE, related_name='rendez_vous')
    date = models.DateTimeField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        patient_str = str(self.patient)
        médecin_str = str(self.médecin)
        logger.info(f'[RendezVous] Accès au RDV : {patient_str} avec {médecin_str} le {self.date} (ID: {self.id})')
        return f"RDV {patient_str} avec {médecin_str} le {self.date}"

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"