from django.shortcuts import render
from website.forms import UsuarioForm
from website.models import *

def cadastrar(request):
    #usuario = Usuario()
    form = UsuarioForm()

    if request.method == 'POST':
        form_de_cadastro = UsuarioForm(request.POST)

        if form_de_cadastro.is_valid():
            usuario = form_de_cadastro.save()
            usuario.save()

            return render(request, 'cadastro.html', {'msg':'Salvo!!!'})
    
    return render(request, 'cadastro.html', {'cadastro':form})