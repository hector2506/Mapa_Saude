# Generated by Django 2.2.12 on 2020-08-11 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_mapa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificacao',
            name='agravo',
        ),
        migrations.RemoveField(
            model_name='notificacao',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='notificacao',
            name='unidade_saude',
        ),
        migrations.RemoveField(
            model_name='user',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='user',
            name='notificacoes',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pacientes',
        ),
        migrations.RemoveField(
            model_name='user',
            name='vinculo',
        ),
        migrations.DeleteModel(
            name='Agravo',
        ),
        migrations.DeleteModel(
            name='CategoriaProfissional',
        ),
        migrations.DeleteModel(
            name='Estabelecimento',
        ),
        migrations.DeleteModel(
            name='Notificacao',
        ),
        migrations.DeleteModel(
            name='Paciente',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
