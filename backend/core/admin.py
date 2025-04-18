from django.contrib import admin
from .models import Patient, Médecin, Assistant, RendezVous
import logging

# Configurer le logger
logger = logging.getLogger(__name__)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'phone', 'insurance_number', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'insurance_number']
    list_filter = ['created_at']

    def save_model(self, request, obj, form, change):
        logger.info(f'[Admin] Sauvegarde patient : {obj.user.first_name} {obj.user.last_name} (ID: {obj.id})')
        super().save_model(request, obj, form, change)


@admin.register(Médecin)
class MédecinAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialty', 'license_number', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'specialty', 'license_number']
    list_filter = ['specialty', 'created_at']

    def save_model(self, request, obj, form, change):
        logger.info(f'[Admin] Sauvegarde médecin : {obj.user.first_name} {obj.user.last_name} (ID: {obj.id})')
        super().save_model(request, obj, form, change)


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__first_name', 'user__last_name']
    list_filter = ['created_at']

    def save_model(self, request, obj, form, change):
        logger.info(f'[Admin] Sauvegarde assistant : {obj.user.first_name} {obj.user.last_name} (ID: {obj.id})')
        super().save_model(request, obj, form, change)


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['patient', 'médecin', 'date', 'reason', 'created_at']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'médecin__user__first_name',
                     'médecin__user__last_name']
    list_filter = ['date', 'médecin']

    def save_model(self, request, obj, form, change):
        logger.info(f'[Admin] Sauvegarde RDV : {obj.patient} avec {obj.médecin} le {obj.date} (ID: {obj.id})')
        super().save_model(request, obj, form, change)