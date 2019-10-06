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

        #Verificação de campos únicos já existentes
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
        perfil = Perfil.objects.filter(email=email, senha=senha, ativo=True).first() #Filtro para buscar usuário no banco

        #Verificação do cadastro no banco
        if perfil is not None:

            return redirect('home/{}'.format(perfil.id))

        else:

            return render(request, 'index.html', {'msg':'*Email ou senha inválidos', 'login':form})

    return render(request, 'index.html', {'login':form})

def home(request, id):
    perfil = Perfil.objects.filter(id=id, ativo=True).first() #Busca de infos do perfil
    desafios = Desafio.objects.filter(autor=perfil.id, ativo=True) #Busca de desafios criados pelo perfil
    desafios_gerais = Desafio.objects.exclude(autor=perfil.id).filter(ativo=True) #Busca excluindo desafios criados pelo perfil
    respostas = Resposta.objects.filter(autor=perfil.id, ativo=True, desafio__ativo=True) #Busca de resposta feitas pelo perfil

    #Lista vaziaz para montar contexto
    criados = []
    gerais_filtrados = []
    respostas_likes = []

    #Entregar infos de likes de respostas criadas
    for resposta in respostas:
        likes = Like.objects.filter(correspondente=resposta.id) #Busca de likes da resposta

        #Entregar uma lista de dicionários como contexto
        if len(likes) != 0: #Se tiver likes
            ultimo = likes.first() #Ultimo perfil que deu like

            #Adicionar um dicionário ao array
            respostas_likes.append({
                'resposta':resposta,
                'like':ultimo.perfil.user,
                'likes': len(likes) #Quantidade de likes
                })

        else:  #Senão

            #Entrega de contexto sem likes
            respostas_likes.append({ 
                'resposta':resposta,
                'like':'Sem likes!!'
                })

    #Entregar apenas desafios não respondidos
    for desafio in desafios_gerais:
        if Resposta.objects.filter(desafio__id=desafio.id, autor=perfil).first() is None: #Se não houver resposta do perfil
            likes = Like.objects.filter(correspondente=desafio.id) #Buscar likes do desafio
            seu_like = Like.objects.filter(correspondente=desafio.id, perfil=id).first() #Buscar se perfil já deu like

            #Entregar uma lista de dicionários como contexto
            if seu_like is None: #Se seu like não existir

                #Adicionar um dicionário ao Array
                gerais_filtrados.append({
                    'desafio':desafio,
                    'vc':None,
                    'likes': len(likes) #Quantidade de likes
                    })

            else: #Senão

                #Adicionar contexto de like com o perfil
                gerais_filtrados.append({
                    'desafio':desafio,
                    'vc':'Você e mais ',
                    'likes':len(likes)
                    })

    #Entregar infos de likes de desafios criados
    for desafio in desafios:
        respostas = Resposta.objects.filter(desafio=desafio) #Buscar respostas do desafio
        likes = Like.objects.filter(correspondente=desafio.id) #Buscar likes do desafio

        #Entregar uma lista de dicionários como contexto
        if len(likes) != 0: #Se houver likes
            ultimo = likes.first() #Ultimo perfil a dar like

            #Adicionar ao Array pra ser entregue como contexto
            criados.append({
                'desafio':desafio,
                'respostas': len(respostas), #Quantidade de respostas
                'like':ultimo.perfil.user,
                'likes': len(likes) #Quantidade de likes
                })

        else: #Senão

            #Contexto sem likes
            criados.append({ 
                'desafio':desafio,
                'respostas': len(respostas),
                'like':'Sem likes!!'
                })

    #Entregar mensagem de 0 desafios criados
    if desafios.first() is None: #Se primeiro desafio não existir

        #Contexto sem desafios
        context = {
            'perfil':perfil, #Perfil do usuário
            'msg':'Você não criou nenhum desafio ainda, tente criar algum!!!!',
            'respostas':respostas_likes, #Array de respostas com infos
            'gerais':gerais_filtrados #Array de desafios não respondidos com infos
        }

        return render(request, 'home.html', context)

    else: #Senão

        #Contexto com desafios
        context = {
            'perfil':perfil,
            'criados':criados, #Arrays com desafios criados e infos
            'respostas':respostas_likes,
            'gerais':gerais_filtrados
        }

        return render(request, 'home.html', context)

def desafiar(request, id):

    #Entregar formulário
    form = DesafioForm()

    #Para verificar se desafio idêntico existente
    context = {'desafio':form}

    if request.method == 'POST': #Se mátodo da requisição for post
        titulo = request.POST.get('titulo')
        tema = request.POST.get('tema')
        valor = request.POST.get('valor')
        autor = Perfil.objects.filter(id=id, ativo=True).first() #Buscar perfil do autor
        filtro = Desafio.objects.filter(autor=autor, titulo=titulo, tema=tema, valor=valor, ativo=True).first() #Buscar se existe desafio idêntico

        context = {

            'desafio':form,
            'msg':'*Esse desafio já foi criado!!!'
        }

        #Verifica se Usuario já criou desafio idêntico
        if filtro is None:

            #Criação de um desafio no banco
            desafio = Desafio(autor=autor, titulo=titulo, tema=tema, valor=valor)
            desafio.save()

            return redirect('/home/{}'.format(id))


    return render(request, 'desafiar.html', context)

def responder(request, id, id_desafio):

    #Entrega formulário
    form = RespostaForm()
    
    #Para verificação de resposta idêntica
    context = {'resposta':form}

    if request.method == 'POST':
        valor = request.POST.get('valor')
        autor = Perfil.objects.filter(id=id, ativo=True).first() #Buscar perfil do autor
        desafio = Desafio.objects.filter(id=id_desafio, ativo=True).first() #Buscar desafio correspondente
        filtro = Resposta.objects.filter(valor=valor, autor=autor, desafio=desafio, ativo=True).first() #Filtrar existencia de resposta idêntica
        
        context = {
            'resposta':form,
            'msg':'*Essa resposta já foi criada!!!'
        }

        #Verificação de Resposta indêntica
        if filtro is None:

            #Criação de uma resposta no banco
            resposta = Resposta(valor=valor, autor=autor, desafio=desafio)
            resposta.save()

            return redirect('/home/{}'.format(id))

    return render(request, 'responder.html', context)

#Página de um desafio
def desafio(request, id):
    desafio = Desafio.objects.filter(id=id, ativo=True).first() #Buscar desafio
    respostas = Resposta.objects.filter(desafio__id=id, ativo=True) #Buscar respostas do desafio
    likes = Like.objects.filter(correspondente=id) #Buscar likes
    ultimo = likes.first() #Ultimo perfil a dar like

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
    perfil = Perfil.objects.filter(user=user, ativo=True).first() #Buscar perfil
    respostas = Resposta.objects.filter(autor__user=user, ativo=True) #Buscar respostas do perfil
    desafios = Desafio.objects.filter(autor__user=user, ativo=True) #Buscar desafios criados pelo perfil


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
    
    filtro = Like.objects.filter(correspondente=id_desafio, perfil__id=id).first() #Buscar like já existente

    #Verificar se Usuário já deu like
    if filtro is None:
        perfil = Perfil.objects.filter(id=id).first() #Buscar perfil do like

        #Salvar like no banco
        like = Like(correspondente=id_desafio, perfil=perfil)
        like.save()

    return redirect('/home/{}'.format(id))

def like_resposta(request, id, titulo, user):
    resposta = Resposta.objects.filter(id=id, ativo=True).first() #Buscar resposta
    filtro = Resposta.objects.filter(id=id, likes__perfil__id=user).first() #Buscar like já existente

    if filtro is None:
        perfil = Perfil.objects.filter(id=user).first() #Buscar perfil do like

        #Salvar like no banco
        like = Like(perfil=perfil, correspondente=resposta.id)
        like.save()

        return redirect('/desafio/{}'.format(resposta.desafio.id))

    return render(request, 'error.html', {'msg':'Oops.. Essa ação é inválida :('})

def delete_desafio(request, id, id_desafio):

    desafio = Desafio.objects.filter(id=id_desafio, ativo=True).first() #Buscar desafio

    #Verificar a existencia do desafio
    if desafio is not None:

        #Alterar para inativo
        desafio.ativo = False
        desafio.save()

        return redirect('/home/{}'.format(id))

    return render(request, 'error.html', {'msg':'Oops.. Essa ação é inválida :('})