from django import forms
from website.models import *

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('user', 'nome', 'sobrenome', 'mensagem', 'email','senha','telefone')

class  LoginForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('email', 'senha')

class DesafioForm(forms.ModelForm):
    class Meta:
        model = Desafio
        fields = ('titulo', 'tema', 'valor')

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ('valor',)