from django.db import models
from django.contrib.auth.models import User
import logging

# Configurer le logger
logger = logging.getLogger(__name__)

class Hôpital(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de l'hôpital")
    adresse = models.CharField(max_length=255, verbose_name="Adresse")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    code_postal = models.CharField(max_length=10, verbose_name="Code postal")
    téléphone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    def __str__(self):
        return f"{self.nom} ({self.ville})"

    class Meta:
        verbose_name = "Hôpital"
        verbose_name_plural = "Hôpitaux"
        ordering = ['nom']

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]
    gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICES, verbose_name="Genre")
    address = models.CharField(max_length=255, verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville", default="Paris")
    postal_code = models.CharField(max_length=10, verbose_name="Code postal", default="00000")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    emergency_contact = models.CharField(max_length=100, blank=True, default="", verbose_name="Contact d'urgence")
    emergency_phone = models.CharField(max_length=20, blank=True, default="", verbose_name="Téléphone d'urgence")

    blood_type = models.CharField(
        max_length=3,
        verbose_name="Groupe sanguin",
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')],
        blank=True
    )
    allergies = models.TextField(blank=True, verbose_name="Allergies")
    current_medications = models.TextField(blank=True, verbose_name="Médicaments actuels")
    medical_history = models.TextField(blank=True, verbose_name="Antécédents médicaux")
    insurance_number = models.CharField(max_length=50, blank=True, unique=True, verbose_name="Numéro de sécurité sociale")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def age(self):
        """Calcule l'âge du patient à partir de sa date de naissance."""
        import datetime
        today = datetime.date.today()
        return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def has_complete_profile(self):
        """Vérifie si le profil médical est complet."""
        required_fields = [self.blood_type, self.allergies, self.medical_history]
        return all(field for field in required_fields)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['user__last_name']

class Médecin(models.Model):
    SPECIALTY_CHOICES = [
        ('CARDIOLOGIE', 'Cardiologie'),
        ('DERMATOLOGIE', 'Dermatologie'),
        ('GENERALISTE', 'Médecine générale'),
        ('RADIOLOGIE', 'Radiologie'),
        ('PEDIATRIE', 'Pédiatrie'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='médecin_profile')
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, verbose_name="Spécialité")
    license_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de licence")
    hôpital = models.ForeignKey(Hôpital, on_delete=models.SET_NULL, null=True, verbose_name="Hôpital d'affiliation")
    bio = models.TextField(blank=True, verbose_name="Biographie")
    patients = models.ManyToManyField(Patient, related_name="médecins", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_name = self.user.first_name or 'Unknown'
        last_name = self.user.last_name or 'Unknown'
        logger.info(f"[Médecin] Accès au médecin : {first_name} {last_name} (ID: {self.id}, User ID: {self.user.id})")
        logger.debug(f"[Médecin] Valeurs brutes - first_name: {self.user.first_name}, last_name: {self.user.last_name}")
        if not self.user.first_name or not self.user.last_name:
            logger.warning(f"[Médecin] Noms manquants pour User ID: {self.user.id}")
        return f"Dr {first_name} {last_name}"

    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"

class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='assistant_profile')
    hôpital = models.ForeignKey(Hôpital, on_delete=models.SET_NULL, null=True, verbose_name="Hôpital d'affiliation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_name = self.user.first_name or 'Unknown'
        last_name = self.user.last_name or 'Unknown'
        logger.info(f"[Assistant] Accès à l'assistant : {first_name} {last_name} (ID: {self.id}, User ID: {self.user.id})")
        logger.debug(f"[Assistant] Valeurs brutes - first_name: {self.user.first_name}, last_name: {self.user.last_name}")
        if not self.user.first_name or not self.user.last_name:
            logger.warning(f"[Assistant] Noms manquants pour User ID: {self.user.id}")
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
        logger.info(f"[RendezVous] Accès au RDV : {patient_str} avec {médecin_str} le {self.date} (ID: {self.id})")
        return f"RDV {patient_str} avec {médecin_str} le {self.date}"

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        constraints = [
            models.UniqueConstraint(
                fields=['médecin', 'date'],
                name='unique_rendezvous_medecin_date'
            ),
            models.UniqueConstraint(
                fields=['patient', 'date'],
                name='unique_rendezvous_patient_date'
            )
        ]