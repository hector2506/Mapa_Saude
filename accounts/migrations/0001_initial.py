# Generated by Django 2.2.12 on 2020-07-24 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProfissional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Estabelecimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('coordenadas', models.CharField(default=None, max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('cpf', models.CharField(max_length=11, unique=True, verbose_name='CPF')),
                ('nome', models.CharField(max_length=100, null=True, verbose_name='Nome Completo')),
                ('active', models.BooleanField(blank=True, default=True)),
                ('staff', models.BooleanField(blank=True, default=False)),
                ('admin', models.BooleanField(blank=True, default=False)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categoria', to='accounts.CategoriaProfissional')),
                ('vinculo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vinculo', to='accounts.Estabelecimento')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
