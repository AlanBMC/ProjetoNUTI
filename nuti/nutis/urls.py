from django.urls import path
from . import views

urlpatterns = [
#Rotas - foi criado apenas um rota padrão.
    path('', views.home, name='index'),
]