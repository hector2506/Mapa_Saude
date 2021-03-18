# Generated by Django 2.2.12 on 2020-07-24 00:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('patient', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agravo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_primeiros_sintomas', models.DateField(default=None)),
                ('data_notificacao', models.DateField(default=datetime.date.today)),
                ('sinais_clinicos', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Febre'), (2, 'Mialgia'), (3, 'Cefaleia'), (4, 'Exantema'), (5, 'Vomito'), (6, 'Nauseas'), (7, 'Dor Nas Costas'), (8, 'Conjuntivite'), (9, 'Artrite'), (10, 'Artralgia Intensa'), (11, 'Petequias'), (12, 'Leucopenia'), (13, 'Prova do Laço Positiva'), (14, 'Dor Retroorbital')], default=None, max_length=32)),
                ('doencas_pre_existentes', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Diabetes'), (2, 'Doencas Hematologicas'), (3, 'Hepatopatias'), (4, 'Doenca Renal Cronica'), (5, 'Hipertensao Arterial'), (6, 'Doenca Acido Peptica')], default=None, max_length=11)),
                ('situacao_atual', models.CharField(choices=[('Notificado', 'Notificado'), ('Confirmado', 'Confirmado'), ('Alta', 'Alta'), ('Óbito', 'Óbito')], default='Notificado', max_length=25)),
                ('agravo', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='agravo_notificacao', to='notification.Agravo')),
                ('paciente', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='paciente_notificacao', to='patient.Paciente')),
                ('unidade_saude', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='unidade_saude', to='accounts.Estabelecimento')),
                ('usuario', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='agravo_usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
