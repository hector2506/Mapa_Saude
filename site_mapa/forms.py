from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class UserLoginForm(forms.Form):
    cpf = forms.CharField(label="CPF", max_length=11, min_length=11)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        cpf = self.cleaned_data.get('cpf')
        password = self.cleaned_data.get('password')

        if cpf and password:
            user = authenticate(username=cpf, password=password)
            if not user:
                raise forms.ValidationError('Usuário ou senha incorretos.')
            if not user.check_password(password):
                raise forms.ValidationError('Senha incorreta.')
            if not user.is_active:
                raise forms.ValidationError('Usuário não está ativo.')

        return super(UserLoginForm, self).clean(*args,**kwargs)


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Senha:", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Senha:", widget=forms.PasswordInput)
    

    class Meta:
        model = User
        fields = ['cpf', 'nome', 'categoria', 'vinculo']
    
    def clean(self, *args, **kwargs):
        cpf = self.cleaned_data['cpf']
        if len(cpf) != 11:
            raise forms.ValidationError("O CPF deve conter 11 digitos.")
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não são compatíveis.")
        cpf_qs = User.objects.filter(cpf=cpf)
        if cpf_qs.exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return super(UserRegisterForm, self).clean(*args,**kwargs)

class PacienteRegisterForm(forms.ModelForm):
    
    class Meta:
        model = Paciente
        fields = ['cns','nome','sexo','data_nascimento','ocupacao','gestacao','uf','municipio','cep']
        widgets = {
            'data_nascimento': DateInput()
        }
    
    def clean(self, *args, **kwargs):
        return super(PacienteRegisterForm, self).clean(*args,**kwargs)

class NotificacaoForm(forms.ModelForm):
    
    class Meta:
        model = Notificacao
        fields = ['paciente','agravo','unidade_saude','data_primeiros_sintomas','sinais_clinicos','doencas_pre_existentes']
        widgets = {
            'data_primeiros_sintomas': DateInput()
        }
    
    def clean(self, *args, **kwargs):
        return super(NotificacaoForm, self).clean(*args,**kwargs)