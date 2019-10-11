"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', views.cadastrar),
    path('', views.login),
    path('home/<str:id>', views.home),
    path('home/desafiar/<str:id>', views.desafiar),
    path('delete/<str:id>/<str:id_desafio>/', views.delete_desafio),
    path('desafio/<str:id>/<str:id_desafio>/', views.desafio),
    path('<str:user>', views.usuario),
    path('like/d/<str:id>/<str:id_desafio>', views.like_desafio),
    path('like/r/<str:id>/<str:id_desafio>', views.like_resposta)
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
