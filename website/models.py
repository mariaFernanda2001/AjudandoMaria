from django.db import models

class Perfil(models.Model):
    
    avatar = models.FileField(upload_to='avatar/')
    user = models.CharField(max_length=15, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    nome = models.CharField(max_length=15, null=False)
    sobrenome = models.CharField(max_length=15, null=False)
    mensagem = models.CharField(max_length=50, default='')
    senha = models.CharField(max_length=15, null=False)
    telefone = models.CharField(max_length=14, null=False)
    ativo = models.BooleanField(default=True)
    criacao = models.DateField(auto_now_add=True)

class Like(models.Model):

    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)

class Desafio(models.Model):

    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=False)
    titulo = models.CharField(max_length=30, null=False)
    tema = models.CharField(max_length=15, null=False)
    valor = models.TextField(max_length=240, null=False)
    likes = models.ForeignKey(Like, on_delete=models.CASCADE, null=True)
    total = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    criacao = models.DateTimeField(auto_now_add=True)

class Resposta(models.Model):

    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=False)
    valor = models.TextField(max_length=240, null=False)
    likes = models.ForeignKey(Like, on_delete=models.CASCADE, null=True)
    total = models.PositiveIntegerField(default=0)
    desafio = models.ForeignKey(Desafio, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    criacao = models.DateTimeField(auto_now_add=True)