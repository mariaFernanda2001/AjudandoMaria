from django.shortcuts import render, redirect
from website.forms import *
from website.models import *

def cadastrar(request):

    #Entregar o form como contexto
    form = UsuarioForm()

    if request.method == 'POST':

        #Pegar Valores do forms
        user = request.POST.get('user')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        telefone = request.POST.get('telefone')
        mensagem = request.POST.get('mensagem')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')

        #Verificação de usuário já existente
        if Perfil.objects.filter(user=user).exists():

            return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Nome já está sendo usado, tente outro..'})

        elif Perfil.objects.filter(email=email).exists():

            return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Email já cadastrado'})

        elif Perfil.objects.filter(telefone=telefone).exists():

            return render(request, 'cadastro.html', {'cadastro':form, 'msg':'*Telefone já cadastrado'})
        
        else:

            #Cadastra e acessa home
            perfil = Perfil(user=user, sobrenome=sobrenome, mensagem=mensagem, nome=nome, email=email, telefone=telefone, senha=senha)
            perfil.save()
            
            return redirect('/home/{}'.format(perfil.id))

    return render(request, 'cadastro.html', {'cadastro':form})

def login(request):
    
    #Entregar form como contexto
    form = LoginForm()

    if request.method == 'POST':

        #Pegar valores do formulário
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        perfil = Perfil.objects.filter(email=email, senha=senha, ativo=True).first()

        #Verificação do cadastro no banco
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
    criados = []
    gerais_filtrados = []
    respostas_likes = []

    #Entregar infos de likes de respostas criadas
    for resposta in respostas:
        likes = Like.objects.filter(correspondente=resposta.id)

        #Entregar uma lista de dicionários como contexto
        if len(likes) != 0:
            ultimo = likes.first()
            respostas_likes.append({
                'resposta':resposta,
                'like':ultimo.perfil.user,
                'likes': len(likes)
                })
        else:
            respostas_likes.append({ 
                'resposta':resposta,
                'like':'Sem likes!!'
                })

    #Entregar apenas desafios não respondidos
    for desafio in desafios_gerais:
        if Resposta.objects.filter(desafio__id=desafio.id, autor=perfil).first() is None:
            likes = Like.objects.filter(correspondente=desafio.id)
            seu_like = Like.objects.filter(correspondente=desafio.id, perfil=id).first()

            #Entregar uma lista de dicionários como contexto
            if seu_like is None:
                gerais_filtrados.append({
                    'desafio':desafio,
                    'vc':None,
                    'likes': len(likes)
                    })
            else:
                gerais_filtrados.append({
                    'desafio':desafio,
                    'vc':'Você e mais ',
                    'likes':len(likes)
                    })

    #Entregar infos de likes de desafios criados
    for desafio in desafios:
        respostas = Resposta.objects.filter(desafio=desafio)
        likes = Like.objects.filter(correspondente=desafio.id)

        #Entregar uma lista de dicionários como contexto
        if len(likes) != 0:
            ultimo = likes.first()
            criados.append({
                'desafio':desafio,
                'respostas': len(respostas),
                'like':ultimo.perfil.user,
                'likes': len(likes)
                })
        else:
            criados.append({ 
                'desafio':desafio,
                'respostas': len(respostas),
                'like':'Sem likes!!'
                })

    #Entregar mensagem de 0 desafios criados
    if desafios.first() is None:
        context = {
            'perfil':perfil,
            'msg':'Você não criou nenhum desafio ainda, tente criar algum!!!!',
            'respostas':respostas_likes,
            'gerais':gerais_filtrados
        }

        return render(request, 'home.html', context)

    else:
        context = {
            'perfil':perfil,
            'criados':criados,
            'respostas':respostas_likes,
            'gerais':gerais_filtrados
        }

        return render(request, 'home.html', context)

def desafiar(request, id):

    #Entregar formulário
    form = DesafioForm()

    #Para fazer um 'toogle' e verificar se desafio idêntico existente
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

        #Verifica se Usuario já criou desafio idêntico
        if filtro is None:
            desafio = Desafio(autor=autor, titulo=titulo, tema=tema, valor=valor)
            desafio.save()

            return redirect('/home/{}'.format(id))


    return render(request, 'desafiar.html', context)

def responder(request, id, id_desafio):

    #Entrega formulário
    form = RespostaForm()
    
    #Fazer um 'toogle' pra verificação de resposta indêntica
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

        #Verificação de Resposta indêntica
        if filtro is None:
            resposta = Resposta(valor=valor, autor=autor, desafio=desafio)
            resposta.save()

            return redirect('/home/{}'.format(id))

    return render(request, 'responder.html', context)

#Página de um desafio
def desafio(request, id):
    desafio = Desafio.objects.filter(id=id, ativo=True).first()
    respostas = Resposta.objects.filter(desafio__id=id, ativo=True)
    likes = Like.objects.filter(correspondente=id)
    ultimo = likes.first()

    #Entrega o contexto do desafio
    context = {

        'desafio':desafio,
        'respostas':respostas,
        'likes':len(likes),
        'like':ultimo.perfil.user
    }

    return render(request, 'desafio.html', context)

#Página de um Perfil
def usuario(request, user):
    perfil = Perfil.objects.filter(user=user, ativo=True).first()
    respostas = Resposta.objects.filter(autor__user=user, ativo=True)
    desafios = Desafio.objects.filter(autor__user=user, ativo=True)


    #Entregar contexto do Perfil
    if perfil is not None:
        context = {

            'perfil':perfil,
            'respostas':respostas,
            'desafios':desafios
        }

        return render(request, 'usuario.html', context)

    return render(request, 'error.html', {'msg':'Oops.. Rota inválida'})

#Fazer um like em um desafio
def like_desafio(request, id, id_desafio):
    
    filtro = Like.objects.filter(correspondente=id_desafio, perfil__id=id).first()

    #Verificar se Usuário já deu like
    if filtro is None:
        perfil = Perfil.objects.filter(id=id).first()
        like = Like(correspondente=id_desafio, perfil=perfil)
        like.save()

    return redirect('/home/{}'.format(id))

def like_resposta(request, id, titulo, user):
    resposta = Resposta.objects.filter(id=id, ativo=True).first()
    filtro = Resposta.objects.filter(id=id, likes__perfil__id=user).first()

    if filtro is None:
        perfil = Perfil.objects.filter(id=user).first()
        like = Like(perfil=perfil, correspondente=resposta.id)
        like.save()

        return redirect('/desafio/{}'.format(resposta.desafio.id))

    return render(request, 'error.html', {'msg':'Oops.. Essa ação é inválida :('})

def delete_desafio(request, id, id_desafio):

    desafio = Desafio.objects.filter(id=id_desafio, ativo=True).first()

    #Verificar a existencia do desafio
    if desafio is not None:

        desafio.ativo = False
        desafio.save()

        return redirect('/home/{}'.format(id))

    return render(request, 'error.html', {'msg':'Oops.. Essa ação é inválida :('})