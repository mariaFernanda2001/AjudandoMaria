from django import forms
from website.models import *

class  LoginForm(forms.Form):

    #Formulário de login
    email = forms.EmailField(label='Email', widget=forms.widgets.EmailInput(), required=True,)
    senha = forms.CharField(label='Senha', widget=forms.widgets.PasswordInput(), required=True, max_length=15)

class UsuarioForm(LoginForm): #Herda campos de LoginForm

    #Formulário de cadastro
    avatar = forms.ImageField(label='Avatar', widget=forms.widgets.ClearableFileInput)
    user = forms.CharField(label='User', required=True, max_length=15)
    nome = forms.CharField(label='Nome', required=True, max_length=15)
    sobrenome = forms.CharField(label='Sobrenome', required=True, max_length=15)
    mensagem = forms.CharField(label='Sobre', max_length=50)
    telefone = forms.CharField(label='Telefone', widget=forms.widgets.NumberInput(), required=True, max_length=15)

class DesafioForm(forms.ModelForm): #Usa uma model para criar campos
    class Meta:
        model = Desafio
        fields = ('titulo', 'tema', 'valor')

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ('valor',)