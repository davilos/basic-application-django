from django.urls import path
from .views import cadastro, index, contato, produto, logar

urlpatterns = [
    path('', index, name='index'),
    path('contato/', contato, name='contato'),
    path('produto/', produto, name='produto'),
    path('cadastro/', cadastro, name='cadastro'),
    path('logar/', logar, name='logar'),
]
