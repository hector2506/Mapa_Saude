# Generated by Django 2.2.7 on 2020-04-03 06:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_mapa', '0014_auto_20200403_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacao',
            name='data_notificacao',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
