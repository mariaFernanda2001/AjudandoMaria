from django.shortcuts import render, redirect
from website.forms import *
from website.models import *

def cadastrar(request):
    form = UsuarioForm()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        form_de_cadastro = UsuarioForm(request.POST)

        if form_de_cadastro.is_valid():

                usuario = form_de_cadastro.save()
                usuario.save()

                return redirect('/home/{}/{}'.format(usuario.id, usuario.nome))
        else:
            
            if Usuario.objects.filter(nome=nome).first() is not None:

                return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Nome já está sendo usado, tente outro..'})

            elif Usuario.objects.filter(email=email).first() is not None:

                return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Email já cadastrado'})

            elif Usuario.objects.filter(telefone=telefone).first() is not None:

                return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Telefone já cadastrado'})
    
    return render(request, 'cadastro.html', {'cadastro':form})

def login(request):
    
    form = LoginForm()

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        usuario = Usuario.objects.filter(email=email, senha=senha).first()

        if usuario is not None:
            identificacao = str(usuario.id)
            nome = str(usuario.nome)

            return redirect('home/{}/{}'.format(identificacao,nome))

        else:

            return render(request, 'index.html', {'msg':'*Email ou senha inválidos', 'login':form})

    return render(request, 'index.html', {'login':form})

def home(request, id, nome):
    usuario = Usuario.objects.filter(id=id, nome=nome).first()
    desafios = Desafio.objects.filter(autor=usuario.id, ativo=True)
    desafios_gerais = Desafio.objects.exclude(autor=usuario.id)

    if desafios.first() is None:
        context = {
            'nome':usuario.nome,
            'msg':'Você não criou nenhum desafio ainda, tente criar algum!!!!',
            'gerais':desafios_gerais
        }

        return render(request, 'home.html', context)

    else:
        context = {
            'nome':usuario.nome,
            'desafios':desafios,
            'gerais':desafios_gerais
        }
        return render(request, 'home.html', context)

def desafiar(request, id, nome):

    form = DesafioForm()

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        tema = request.POST.get('tema')
        valor = request.POST.get('valor')
        autor = Usuario.objects.filter(id=id, nome=nome).first()

        desafio = Desafio(autor=autor, titulo=titulo, tema=tema, valor=valor)
        desafio.save()

        return redirect('/home/{}/{}'.format(id,nome))

    return render(request, 'desafiar.html', {'desafio':form})