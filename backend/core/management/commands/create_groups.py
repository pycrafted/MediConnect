from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Patient, Médecin, RendezVous

class Command(BaseCommand):
    help = 'Crée les groupes et permissions par défaut'

    def handle(self, *args, **options):
        # Contenu des groupes
        groupes = {
            'Médecin': [
                ('view_patient', 'Peut voir les patients'),
                ('add_rendezvous', 'Peut créer un rendez-vous'),
                ('change_rendezvous', 'Peut modifier un rendez-vous'),
            ],
            'Assistant': [
                ('add_patient', 'Peut ajouter un patient'),
                ('view_patient', 'Peut voir les patients'),
                ('add_rendezvous', 'Peut créer un rendez-vous'),
            ],
            'Patient': [
                ('view_own_profile', 'Peut voir son propre profil'),
            ]
        }

        for nom_groupe, permissions in groupes.items():
            groupe, created = Group.objects.get_or_create(name=nom_groupe)
            for codename, name in permissions:
                # Pour les permissions custom (comme view_own_profile), on les crée
                if not Permission.objects.filter(codename=codename).exists():
                    content_type = ContentType.objects.get_for_model(Patient)
                    Permission.objects.create(
                        codename=codename,
                        name=name,
                        content_type=content_type,
                    )
                permission = Permission.objects.get(codename=codename)
                groupe.permissions.add(permission)
            self.stdout.write(self.style.SUCCESS(f'Groupe "{nom_groupe}" configuré'))