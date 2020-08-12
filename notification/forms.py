from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import *
from django.forms import CheckboxSelectMultiple


class DateInput(forms.DateInput):
    input_type = 'date'


class NotificacaoForm(forms.ModelForm):

    class Meta:
        model = Notificacao
        fields = ['paciente', 'agravo', 'unidade_saude',
                  'data_primeiros_sintomas', 'sinais_clinicos', 'doencas_pre_existentes']
        labels = {
            'unidade_saude': "Unidade de Saúde",
            'data_primeiros_sintomas': "Data dos Primeiros Sintomas",
            'sinais_clinicos': "Sinais Clínicos",
            'doencas_pre_existentes': "Doenças Preexistentes"
        }
        widgets = {
            'data_primeiros_sintomas': DateInput(),
            'sinais_clinicos': CheckboxSelectMultiple(),
            'doencas_pre_existentes': CheckboxSelectMultiple(),
        }

    def clean(self, *args, **kwargs):
        return super(NotificacaoForm, self).clean(*args, **kwargs)
