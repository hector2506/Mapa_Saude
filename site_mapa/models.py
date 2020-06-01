from multiselectfield import MultiSelectField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date

class Agravo(models.Model):
    nome = models.CharField(max_length=255) 

    def __str__(self):
        return self.nome

class CategoriaProfissional(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Estabelecimento(models.Model):
    nome = models.CharField(max_length=255)
    coordenadas = models.CharField(max_length=10000,default=None)

    def __str__(self):
        return self.nome

class UserManager(BaseUserManager):
    def create_user(self, cpf, nome, categoria, vinculo, password=None, is_active=True, is_staff=False,is_admin=False):
        if not cpf:
            raise ValueError("Usuários precisam possuir CPF")
        if not password:
            raise ValueError("Usuários precisam possuir senha")
        user = self.model(cpf = cpf)
        user.nome = nome
        user.categoria = categoria
        user.vinculo = vinculo
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, cpf, nome, categoria, vinculo, password=None):
        user = self.create_user(cpf, nome, categoria, vinculo, password=password,is_staff=True)
        return user

    def create_superuser(self, cpf, nome=None, categoria=None, vinculo=None, password=None):
        user = self.create_user(cpf, nome=nome, categoria=categoria, 
        vinculo=vinculo, password=password,is_staff=True, is_admin=True)
        return user

class User(AbstractBaseUser):
    cpf = models.CharField('CPF', unique=True, max_length=11)
    nome = models.CharField('Nome Completo', max_length=100, null=True)
    categoria = models.ForeignKey(CategoriaProfissional, related_name='categoria',on_delete=models.CASCADE, null=True)
    vinculo = models.ForeignKey(Estabelecimento, related_name='vinculo', on_delete=models.CASCADE, null=True)
    active = models.BooleanField(blank=True, default=True)
    staff = models.BooleanField(blank=True, default=False)
    admin = models.BooleanField(blank=True, default=False)
    #date_joined = models.DateTimeField('Data de Criação', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.cpf

    def get_full_name(self):
        return self.cpf
    
    def get_short_name(self):
        return self.cpf
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

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