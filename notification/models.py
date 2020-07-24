from multiselectfield import MultiSelectField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date
from accounts.models import *
from patient.models import *

class Agravo(models.Model):
    nome = models.CharField(max_length=255) 

    def __str__(self):
        return self.nome

class Notificacao(models.Model):
    SINAIS_CLÍNICOS = ((1, 'Febre'),
               (2, 'Mialgia'),
               (3, 'Cefaleia'),
               (4, 'Exantema'),
               (5, 'Vomito'),
               (6, 'Nauseas'),
               (7, 'Dor Nas Costas'),
               (8, 'Conjuntivite'),
               (9, 'Artrite'),
               (10, 'Artralgia Intensa'),
               (11, 'Petequias'),
               (12, 'Leucopenia'),
               (13, 'Prova do Laço Positiva'),
               (14, 'Dor Retroorbital'))
               
    DOENCAS_PRE_EXISTENTES = ((1, 'Diabetes'),
               (2, 'Doencas Hematologicas'),
               (3, 'Hepatopatias'),
               (4, 'Doenca Renal Cronica'),
               (5, 'Hipertensao Arterial'),
               (6, 'Doenca Acido Peptica'))

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
    sinais_clinicos = MultiSelectField(choices=SINAIS_CLÍNICOS, default=None)
    doencas_pre_existentes = MultiSelectField(choices=DOENCAS_PRE_EXISTENTES, default=None)
    situacao_atual = models.CharField(max_length=25, choices=situacao, default='Notificado')

    def __str__(self):
        return ("Notificação " + str(self.id))