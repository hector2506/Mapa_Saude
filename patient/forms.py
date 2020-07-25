from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class PacienteRegisterForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = ['cns', 'nome', 'sexo', 'data_nascimento', 'ocupacao',
                  'gestacao', 'uf', 'municipio', 'latitude', 'longitude']
        labels = {
            'data_nascimento': 'Data de Nascimento',
            'ocupacao': "Ocupação",
            'gestacao': "Gestação",
            'uf': 'UF',
            'municipio': "Município"
        }
        widgets = {
            'data_nascimento': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(PacienteRegisterForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget.attrs['class'] = "d-none"
        self.fields['longitude'].widget.attrs['class'] = "d-none"

    def clean(self, *args, **kwargs):
        return super(PacienteRegisterForm, self).clean(*args, **kwargs)
