from django.shortcuts import render, redirect
from website.forms import *
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

def login(request):
    
    form = LoginForm()

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        usuario = Usuario.objects.filter(email=email, senha=senha).first()

        if usuario is not None:
            identificacao = usuario.id

            return redirect('home/' + str(identificacao))


    return render(request, 'index.html', {'login':form})

def home(request, id):

    return render(request, 'home.html')