from django import forms
from website.models import *
from django.forms.widgets import ClearableFileInput

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome','email','senha','telefone')

class  LoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'senha')

class DesafioForm(forms.ModelForm):
    class Meta:
        model = Desafio
        fields = ('titulo', 'tema', 'valor')