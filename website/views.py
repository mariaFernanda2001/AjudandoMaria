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

        if Perfil.objects.filter(user=user).exists():

            return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Nome já está sendo usado, tente outro..'})

        elif Perfil.objects.filter(email=email).exists():

            return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Email já cadastrado'})

        elif Perfil.objects.filter(telefone=telefone).exists():

            return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Telefone já cadastrado'})
        
        else:
            perfil = Perfil(user=user, sobrenome=sobrenome, mensagem=mensagem, nome=nome, email=email, telefone=telefone, senha=senha)
            perfil.save()
            
            return redirect('/home/{}'.format(perfil.id))

    return render(request, 'cadastro.html', {'cadastro':form})

def login(request):
    
    form = LoginForm()

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        perfil = Perfil.objects.filter(email=email, senha=senha, ativo=True).first()

        if perfil is not None:

            return redirect('home/{}'.format(perfil.id))

        else:

            return render(request, 'index.html', {'msg':'*Email ou senha inválidos', 'login':form})

    return render(request, 'index.html', {'login':form})

def home(request, id):
    perfil = Perfil.objects.filter(id=id, ativo=True).first()
    desafios = Desafio.objects.filter(autor=perfil.id, ativo=True)
    desafios_gerais = Desafio.objects.exclude(autor=perfil.id).filter(ativo=True)
    respostas = Resposta.objects.filter(autor=perfil.id, ativo=True, desafio__ativo=True)

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

def desafiar(request, id):

    form = DesafioForm()

    context = {'desafio':form}

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        tema = request.POST.get('tema')
        valor = request.POST.get('valor')
        autor = Perfil.objects.filter(id=id, ativo=True).first()
        filtro = Desafio.objects.filter(autor=autor, titulo=titulo, tema=tema, valor=valor, ativo=True).first()

        context = {

            'desafio':form,
            'msg':'*Esse desafio já foi criado!!!'
        }

        if filtro is None:
            desafio = Desafio(autor=autor, titulo=titulo, tema=tema, valor=valor)
            desafio.save()

            return redirect('/home/{}'.format(id))


    return render(request, 'desafiar.html', context)

def responder(request, id, id_desafio):

    form = RespostaForm()
    
    context = {'resposta':form}

    if request.method == 'POST':
        valor = request.POST.get('valor')
        autor = Perfil.objects.filter(id=id, ativo=True).first()
        desafio = Desafio.objects.filter(id=id_desafio, ativo=True).first()
        filtro = Resposta.objects.filter(valor=valor, autor=autor, desafio=desafio, ativo=True).first()
        
        context = {
            'resposta':form,
            'msg':'*Essa resposta já foi criada!!!'
        }

        if filtro is None:
            resposta = Resposta(valor=valor, autor=autor, desafio=desafio)
            resposta.save()

            return redirect('/home/{}'.format(id))

    return render(request, 'responder.html', context)

def desafio(request, id):
    desafio = Desafio.objects.filter(id=id, ativo=True).first()
    respostas = Resposta.objects.filter(desafio__id=id, ativo=True)

    context = {

        'desafio':desafio,
        'respostas':respostas,
    }

    return render(request, 'desafio.html', context)

def usuario(request, user):
    perfil = Perfil.objects.filter(user=user, ativo=True).first()
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

def like_desafio(request, id, id_desafio):
    
    filtro = Like.objects.filter(correspondente=id_desafio, perfil__id=id).first()

    if filtro is None:
        perfil = Perfil.objects.filter(id=id).first()
        like = Like(correspondente=id_desafio, perfil=perfil)
        like.save()
        desafio = Desafio.objects.filter(id=id_desafio).first()
        desafio.likes += 1
        desafio.save()

    return redirect('/home/{}'.format(id))

def like_resposta(request, id, titulo, user):
    resposta = Resposta.objects.filter(id=id, ativo=True).first()
    filtro = Resposta.objects.filter(id=id, likes__perfil__id=user).first()

    if filtro is None:
        perfil = Perfil.objects.filter(id=user).first()
        like = Like(perfil=perfil)
        like.save()
        resposta.likes = like
        resposta.total += 1
        resposta.save()

        return redirect('/desafio/{}'.format(resposta.desafio.id))

    return render(request, 'error.html', {'msg':'Oops.. Essa ação é inválida :('})

def delete_desafio(request, id, id_desafio):

    desafio = Desafio.objects.filter(id=id_desafio, ativo=True).first()

    if desafio is not None:

        desafio.ativo = False
        desafio.save()

        return redirect('/home/{}'.format(id))

    return render(request, 'error.html', {'msg':'Oops.. Essa ação é inválida :('})