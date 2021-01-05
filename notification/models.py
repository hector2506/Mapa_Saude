from multiselectfield import MultiSelectField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date
from accounts.models import *
from patient.models import *

class SinaisClinicos(models.Model):
    nome = models.CharField(max_length=255, null=True,blank=True, default=None)

    def __str__(self):
        return self.nome

class DoencasPreExistentes(models.Model):
    nome = models.CharField(max_length=255, null=True,blank=True, default=None) 

    def __str__(self):
        return self.nome

class Agravo(models.Model):
    nome = models.CharField(max_length=255)
    sinais_clinicos = models.ManyToManyField(SinaisClinicos, related_name="agravo_sinais", blank=True, default=None)
    doencas_pre_existentes = models.ManyToManyField(DoencasPreExistentes, related_name="agravo_doencas", blank=True, default=None)

    def __str__(self):
        return self.nome

class Notificacao(models.Model):
    situacao = [
        ("Notificado", "Notificado"),
        ("Confirmado", "Confirmado"),
        ("Alta", "Alta"),
        ("Óbito", "Óbito")
    ]
    usuario = models.ForeignKey(User, related_name='agravo_usuario', on_delete=models.CASCADE, default=None)
    paciente = models.ForeignKey(Paciente, related_name='paciente_notificacao', on_delete=models.CASCADE, default=None)
    agravo = models.ForeignKey(Agravo, related_name='agravo_notificacao', on_delete=models.CASCADE, default=None)
    unidade_saude = models.ForeignKey(Estabelecimento, related_name='unidade_saude', on_delete=models.CASCADE, default=None)
    data_primeiros_sintomas = models.DateField(default=None)
    data_notificacao = models.DateField(default=date.today)
    sinais_clinicos = models.ManyToManyField(SinaisClinicos, related_name="notificacao_sinais", blank=True, default=None)
    doencas_pre_existentes = models.ManyToManyField(DoencasPreExistentes, related_name="notificacao_doencas", blank=True, default=None)
    situacao_atual = models.CharField(max_length=25, choices=situacao, default='Notificado')

    def __str__(self):
        return ("Notificação " + str(self.id))