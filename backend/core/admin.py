from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Patient, Médecin, Assistant, RendezVous, Hôpital
import logging

logger = logging.getLogger(__name__)

# Inline pour Hôpital
class HôpitalAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'téléphone', 'email')
    search_fields = ('nom', 'ville', 'code_postal')
    list_filter = ('ville',)

# Inline pour Patient
class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'Profil Patient'
    fields = (
        'date_of_birth', 'gender', 'address', 'city', 'postal_code',
        'phone', 'emergency_contact', 'emergency_phone', 'blood_type',
        'allergies', 'current_medications', 'medical_history', 'insurance_number'
    )
    readonly_fields = ('created_at', 'updated_at')

# Inline pour Médecin
class MédecinInline(admin.StackedInline):
    model = Médecin
    can_delete = False
    verbose_name_plural = 'Profil Médecin'
    fields = ('specialty', 'license_number', 'hôpital', 'bio', 'patients')
    readonly_fields = ('created_at', 'updated_at')

# Inline pour Assistant
class AssistantInline(admin.StackedInline):
    model = Assistant
    can_delete = False
    verbose_name_plural = 'Profil Assistant'
    fields = ('hôpital',)
    readonly_fields = ('created_at', 'updated_at')

# Personnalisation de l'admin User
class CustomUserAdmin(UserAdmin):
    inlines = (PatientInline, MédecinInline, AssistantInline)

    def save_model(self, request, obj, form, change):
        logger.info(f"[UserAdmin] Sauvegarde de l'utilisateur: {obj.username} (ID: {obj.id}) par {request.user}")
        super().save_model(request, obj, form, change)

# Enregistrement des modèles
admin.site.register(Hôpital, HôpitalAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date_of_birth', 'gender', 'phone', 'city', 'age', 'has_complete_profile', 'created_at')
    list_filter = ('gender', 'city', 'blood_type', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'phone', 'insurance_number')
    date_hierarchy = 'created_at'
    ordering = ('user__last_name',)

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('user', 'date_of_birth', 'gender', 'phone', 'address', 'city', 'postal_code')
        }),
        ("Contact d'urgence", {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('Informations médicales', {
            'fields': ('blood_type', 'allergies', 'current_medications', 'medical_history', 'insurance_number')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def full_name(self, obj):
        return obj.__str__()
    full_name.short_description = 'Nom complet'

    def age(self, obj):
        return obj.age()
    age.short_description = 'Âge'

@admin.register(Médecin)
class MédecinAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty', 'license_number', 'hôpital', 'patient_count', 'created_at')
    list_filter = ('specialty', 'hôpital', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'license_number', 'hôpital__nom')
    date_hierarchy = 'created_at'
    filter_horizontal = ('patients',)

    fieldsets = (
        ('Informations professionnelles', {
            'fields': ('user', 'specialty', 'license_number', 'hôpital', 'bio')
        }),
        ('Patients', {
            'fields': ('patients',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def full_name(self, obj):
        return obj.__str__()
    full_name.short_description = 'Nom complet'

    def patient_count(self, obj):
        return obj.patients.count()
    patient_count.short_description = 'Nombre de patients'

@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'hôpital', 'created_at')
    list_filter = ('hôpital', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'hôpital__nom')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Informations', {
            'fields': ('user', 'hôpital')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def full_name(self, obj):
        return obj.__str__()
    full_name.short_description = 'Nom complet'

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'médecin', 'date', 'reason', 'created_at')
    list_filter = ('date', 'médecin__specialty', 'created_at')
    search_fields = (
        'patient__user__first_name', 'patient__user__last_name',
        'médecin__user__first_name', 'médecin__user__last_name',
        'reason'
    )
    date_hierarchy = 'date'
    ordering = ('-date',)

    fieldsets = (
        ('Détails du rendez-vous', {
            'fields': ('patient', 'médecin', 'date', 'reason')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')