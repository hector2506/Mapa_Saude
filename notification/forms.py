from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class NotificacaoForm(forms.ModelForm):
    
    class Meta:
        model = Notificacao
        fields = ['paciente','agravo','unidade_saude','data_primeiros_sintomas','sinais_clinicos','doencas_pre_existentes']
        widgets = {
            'data_primeiros_sintomas': DateInput()
        }
    
    def clean(self, *args, **kwargs):
        return super(NotificacaoForm, self).clean(*args,**kwargs)