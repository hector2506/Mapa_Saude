from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date
from accounts.models import *

class Paciente(models.Model):
    sexo = [
        ("Masculino", "Masculino"),
        ("Feminino", "Feminino"),
        ("Ignorado", "Ignorado")
    ]
    gestacao = [
        ("1", "1º Trimestre"),
        ("2", "2º Trimestre"),
        ("3", "3º Trimestre"),
        ("4", "Idade gestacional ignorada"),
        ("5", "Não"),
        ("6", "Não se aplica"),
        ("9", "Ignorado")
    ]
    uf = [
        ("RO","Rondônia"),("AC","Acre"),("AM","Amazonas"),("RR","Roraima"),("PA","Pará"),("AP","Amapá"),("TO","Tocantins"),
        ("MA","Maranhão"),("PI","Piauí"),("CE","Ceará"),("RN","Rio Grande do Norte"),("PB","Paraíba"),("PE","Pernambuco"),
        ("AL","Alagoas"),("SE","Sergipe"),("BA","Bahia"),("MG","Minas Gerais"),("ES","Espírito Santo"),("RJ","Rio de Janeiro"),
        ("SP","São Paulo"),("PR","Paraná"),("SC","Santa Catarina"),("RS","Rio Grande do Sul"),("MS","Mato Grosso do Sul"),
        ("MT","Mato Grosso"),("GO","Goiás"),("DF","Distrito Federal"),
    ]
    ubs = models.ForeignKey(Estabelecimento, related_name='paciente_ubs', on_delete=models.CASCADE, default=None,null=True)
    cns = models.CharField('CNS', unique=True, max_length=15, default=None)
    nome = models.CharField(max_length=50)
    sexo = models.CharField(max_length=25, choices=sexo, default="Ignorado")
    data_nascimento = models.DateField(auto_now=False, auto_now_add=False, default=None)
    ocupacao = models.CharField(max_length=50, default=None)
    gestacao = models.CharField(max_length=25, choices=gestacao, default="9")
    uf = models.CharField(max_length=25, choices=uf, default="PI")
    municipio = models.CharField(max_length=25, default=None)
    cep = models.CharField(max_length=8,default=None)
    def __str__(self):
        return self.nome