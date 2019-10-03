from django.shortcuts import render, redirect
from website.forms import *
from website.models import *

def cadastrar(request):

    form = UsuarioForm()

    if request.method == 'POST':
        user = request.POST.get('user')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        telefone = request.POST.get('telefone')
        mensagem = request.POST.get('mensagem')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')

        if Perfil.objects.filter(user=user).first() is not None:

            return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Nome já está sendo usado, tente outro..'})

        elif Perfil.objects.filter(email=email).first() is not None:

            return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Email já cadastrado'})

        elif Perfil.objects.filter(telefone=telefone).first() is not None:

            return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Telefone já cadastrado'})
        
        else:
            perfil = Perfil(user=user, sobrenome=sobrenome, mensagem=mensagem, nome=nome, email=email, telefone=telefone, senha=senha)
            perfil.save()
            
            return redirect('/home/{}{}/{}'.format(perfil.criacao, perfil.id, perfil.user))

    return render(request, 'cadastro.html', {'cadastro':form})

def login(request):
    
    form = LoginForm()

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        perfil = Perfil.objects.filter(email=email, senha=senha).first()

        if perfil is not None:

            return redirect('home/{}{}/{}'.format(perfil.criacao, perfil.id, perfil.user))

        else:

            return render(request, 'index.html', {'msg':'*Email ou senha inválidos', 'login':form})

    return render(request, 'index.html', {'login':form})

def home(request, criacao, id, user):
    perfil = Perfil.objects.filter(id=id, user=user).first()
    desafios = Desafio.objects.filter(autor=perfil.id, ativo=True)
    desafios_gerais = Desafio.objects.exclude(autor=perfil.id)
    respostas = Resposta.objects.filter(autor=perfil.id, ativo=True)

    if desafios.first() is None:
        context = {
            'perfil':perfil,
            'msg':'Você não criou nenhum desafio ainda, tente criar algum!!!!',
            'respostas':respostas,
            'gerais':desafios_gerais
        }

        return render(request, 'home.html', context)

    else:
        context = {
            'perfil':perfil,
            'desafios':desafios,
            'respostas':respostas,
            'gerais':desafios_gerais
        }

        return render(request, 'home.html', context)

def desafiar(request, criacao, id, user):

    form = DesafioForm()

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        tema = request.POST.get('tema')
        valor = request.POST.get('valor')
        autor = Perfil.objects.filter(id=id, user=user).first()

        desafio = Desafio(autor=autor, titulo=titulo, tema=tema, valor=valor)
        desafio.save()

        return redirect('/home/{}{}/{}'.format(criacao, id, user))

    return render(request, 'desafiar.html', {'desafio':form})

def responder(request, criacao, id, user, id_desafio):

    form = RespostaForm()
    
    if request.method == 'POST':
        valor = request.POST.get('valor')
        autor = Perfil.objects.filter(id=id, user=user).first()
        desafio = Desafio.objects.filter(id=id_desafio, ativo=True).first()
        resposta = Resposta(valor=valor, autor=autor, desafio=desafio)
        resposta.save()

        return redirect('/home/{}{}/{}'.format(criacao, id, user))

    return render(request, 'responder.html', {'resposta':form})

def desafio(request, id, user, titulo):
    desafio = Desafio.objects.filter(id=id, titulo=titulo, ativo=True).first()
    respostas = Resposta.objects.filter(desafio__id=id, desafio__titulo=titulo, ativo=True)
    perfil = user
    context = {

        'desafio':desafio,
        'respostas':respostas,
        'user':perfil
    }

    return render(request, 'desafio.html', context)

def usuario(request, user):
    perfil = Perfil.objects.filter(user=user).first()
    respostas = Resposta.objects.filter(autor__user=user, ativo=True)
    desafios = Desafio.objects.filter(autor__user=user, ativo=True)

    if perfil is not None:
        context = {

            'perfil':perfil,
            'respostas':respostas,
            'desafios':desafios
        }

        return render(request, 'usuario.html', context)

    return render(request, 'error.html', {'msg':'Oops.. Rota inválida'})

def like_desafio(request, id, titulo, user):
    desafio = Desafio.objects.filter(id=id, titulo=titulo, ativo=True).first()
    like = Desafio.objects.filter(id=id, titulo=titulo, likes__perfil__id=user, ativo=True).first()

    if like is None:
        perfil = Perfil.objects.filter(id=user).first()
        like = Like(perfil=perfil)
        like.save()
        desafio.likes = like
        desafio.total += 1
        desafio.save()


        return redirect('/desafio/{}/{}/{}'.format(id, user, titulo))

    return render(request, 'error.html', {'msg':'Oops.. Essa ação é inválida :('})

def like_resposta(request, id, titulo, user):
    resposta = Resposta.objects.filter(id=id, ativo=True).first()
    like = Resposta.objects.filter(id=id, likes__perfil__id=user).first()

    if like is None:
        perfil = Perfil.objects.filter(id=user).first()
        like = Like(perfil=perfil)
        like.save()
        resposta.likes = like
        resposta.total += 1
        resposta.save()

        return redirect('/desafio/{}/{}/{}'.format(resposta.desafio.id, user, titulo))

    return render(request, 'error.html', {'msg':'Oops.. Essa ação é inválida :('})

def delete_desafio(request, criacao, id, user, id_desafio):

    desafio = Desafio.objects.filter(id=id_desafio, ativo=True).first()

    if desafio is not None:

        desafio.ativo = False
        desafio.save()

        return redirect('/home/{}{}/{}'.format(criacao, id, user))

    return render(request, 'error.html', {'msg':'Oops.. Essa ação é inválida :('})