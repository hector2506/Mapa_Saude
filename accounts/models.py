from multiselectfield import MultiSelectField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date

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