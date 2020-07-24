from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class PacienteRegisterForm(forms.ModelForm):
    
    class Meta:
        model = Paciente
        fields = ['cns','nome','sexo','data_nascimento','ocupacao','gestacao','uf','municipio','cep']
        widgets = {
            'data_nascimento': DateInput()
        }
    
    def clean(self, *args, **kwargs):
        return super(PacienteRegisterForm, self).clean(*args,**kwargs)