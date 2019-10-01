from django.db import models

class Usuario(models.Model):
    
    nome = models.CharField(max_length=15, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    senha = models.CharField(max_length=15, null=False)
    telefone = models.CharField(max_length=14, null=False)
    ativo = models.BooleanField(default=True)
    criacao = models.DateTimeField(auto_now_add=True)

class Desafio(models.Model):

    autor = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=False)
    titulo = models.CharField(max_length=30, null=False)
    tema = models.CharField(max_length=15, null=False)
    valor = models.TextField(max_length=240, null=False)
    likes = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    criacao = models.DateTimeField(auto_now_add=True)

class Resposta(models.Model):

    autor = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=False)
    valor = models.TextField(max_length=240, null=False)
    likes = models.PositiveIntegerField(default=0)
    desafio = models.ForeignKey(Desafio, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    criacao = models.DateTimeField(auto_now_add=True)

class Conclusao(models.Model):
    
    desafio = models.ForeignKey(Desafio, on_delete=models.CASCADE)
    resposta = models.ForeignKey(Resposta, on_delete=models.CASCADE)