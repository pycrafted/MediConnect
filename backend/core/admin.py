from django.contrib import admin
from django import forms
from .models import Patient, Médecin, Assistant, RendezVous
import logging

# Configurer le logger
logger = logging.getLogger(__name__)

class PatientAdminForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        # Sauvegarder le User en premier
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        logger.debug(f'[PatientAdminForm] Sauvegarde User ID: {user.id}, first_name: {user.first_name}, last_name: {user.last_name}')
        user.save()  # Sauvegarde immédiate
        return super().save(commit=commit)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    form = PatientAdminForm
    list_display = ['user', 'date_of_birth', 'phone', 'insurance_number', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'insurance_number']
    list_filter = ['created_at']

    def save_model(self, request, obj, form, change):
        logger.info(f'[Admin] Sauvegarde patient : {obj.user.first_name} {obj.user.last_name} (ID: {obj.id})')
        super().save_model(request, obj, form, change)

class MédecinAdminForm(forms.ModelForm):
    class Meta:
        model = Médecin
        fields = '__all__'

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        logger.debug(f'[MédecinAdminForm] Sauvegarde User ID: {user.id}, first_name: {user.first_name}, last_name: {user.last_name}')
        user.save()
        return super().save(commit=commit)

@admin.register(Médecin)
class MédecinAdmin(admin.ModelAdmin):
    form = MédecinAdminForm
    list_display = ['user', 'specialty', 'license_number', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'specialty', 'license_number']
    list_filter = ['specialty', 'created_at']

    def save_model(self, request, obj, form, change):
        logger.info(f'[Admin] Sauvegarde médecin : {obj.user.first_name} {obj.user.last_name} (ID: {obj.id})')
        super().save_model(request, obj, form, change)

class AssistantAdminForm(forms.ModelForm):
    class Meta:
        model = Assistant
        fields = '__all__'

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        logger.debug(f'[AssistantAdminForm] Sauvegarde User ID: {user.id}, first_name: {user.first_name}, last_name: {user.last_name}')
        user.save()
        return super().save(commit=commit)

@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    form = AssistantAdminForm
    list_display = ['user', 'created_at']
    search_fields = ['user__first_name', 'user__last_name']
    list_filter = ['created_at']

    def save_model(self, request, obj, form, change):
        logger.info(f'[Admin] Sauvegarde assistant : {obj.user.first_name} {obj.user.last_name} (ID: {obj.id})')
        super().save_model(request, obj, form, change)

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['patient', 'médecin', 'date', 'reason', 'created_at']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'médecin__user__first_name', 'médecin__user__last_name']
    list_filter = ['date', 'médecin']

    def save_model(self, request, obj, form, change):
        logger.info(f'[Admin] Sauvegarde RDV : {obj.patient} avec {obj.médecin} le {obj.date} (ID: {obj.id})')
        super().save_model(request, obj, form, change)