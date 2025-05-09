# Generated by Django 5.2 on 2025-04-20 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_patient_options_médecin_bio_médecin_hospital_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hôpital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name="Nom de l'hôpital")),
                ('adresse', models.CharField(max_length=255, verbose_name='Adresse')),
                ('ville', models.CharField(max_length=100, verbose_name='Ville')),
                ('code_postal', models.CharField(max_length=10, verbose_name='Code postal')),
                ('téléphone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
            ],
            options={
                'verbose_name': 'Hôpital',
                'verbose_name_plural': 'Hôpitaux',
                'ordering': ['nom'],
            },
        ),
        migrations.RemoveField(
            model_name='médecin',
            name='hospital',
        ),
        migrations.AddConstraint(
            model_name='rendezvous',
            constraint=models.UniqueConstraint(fields=('médecin', 'date'), name='unique_rendezvous_medecin_date'),
        ),
        migrations.AddConstraint(
            model_name='rendezvous',
            constraint=models.UniqueConstraint(fields=('patient', 'date'), name='unique_rendezvous_patient_date'),
        ),
        migrations.AddField(
            model_name='assistant',
            name='hôpital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.hôpital', verbose_name="Hôpital d'affiliation"),
        ),
        migrations.AddField(
            model_name='médecin',
            name='hôpital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.hôpital', verbose_name="Hôpital d'affiliation"),
        ),
    ]
