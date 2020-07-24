# Generated by Django 2.2.7 on 2020-02-29 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_mapa', '0005_auto_20200229_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacao',
            name='usuario',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='agravo_usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='usuario',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='paciente_usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]