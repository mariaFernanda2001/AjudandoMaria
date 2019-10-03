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
    path('home/<int:id>/<str:user>/', views.home),
    path('home/<int:id>/<str:user>/desafiar/', views.desafiar),
    path('home/<int:id>/<str:user>/responder/<int:id_desafio>/', views.responder),
    path('desafio/<int:id>/<int:user>/<str:titulo>/', views.desafio),
    path('<str:user>', views.usuario),
    path('like/<int:id>/<str:titulo>/<int:user>/d', views.like_desafio),
    path('like/<int:id>/<str:titulo>/<int:user>/r', views.like_resposta)
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
