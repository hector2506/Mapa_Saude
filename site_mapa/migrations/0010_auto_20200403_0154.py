# Generated by Django 2.2.7 on 2020-04-03 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_mapa', '0009_paciente_cns'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacao',
            name='data_notificacao',
            field=models.DateField(auto_now_add=True),
        ),
    ]
