# Generated by Django 2.2.12 on 2020-08-11 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoencasPreExistentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SinaisClinicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, default=None, max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='notificacao',
            name='doencas_pre_existentes',
        ),
        migrations.RemoveField(
            model_name='notificacao',
            name='sinais_clinicos',
        ),
        migrations.AddField(
            model_name='agravo',
            name='doencas_pre_existentes',
            field=models.ManyToManyField(blank=True, default=None, to='notification.DoencasPreExistentes'),
        ),
        migrations.AddField(
            model_name='agravo',
            name='sinais_clinicos',
            field=models.ManyToManyField(blank=True, default=None, to='notification.SinaisClinicos'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='doencas_pre_existentes',
            field=models.ManyToManyField(blank=True, default=None, to='notification.DoencasPreExistentes'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='sinais_clinicos',
            field=models.ManyToManyField(blank=True, default=None, to='notification.SinaisClinicos'),
        ),
    ]