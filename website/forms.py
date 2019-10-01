from django import forms
from website.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome','email','senha','telefone')