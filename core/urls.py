from django.urls import path

from .views import (cadastro, cadastro_conf, contato, index, index_on, logar,
                    logar_conf, produto, sair)

urlpatterns = [
    path('', index, name='index'),
    path('home/', index_on, name='index-on'),
    path('sair/', sair, name='sair'),
    path('contato/', contato, name='contato'),
    path('produto/', produto, name='produto'),
    path('cadastro/', cadastro, name='cadastro'),
    path('logar/', logar, name='logar'),
    path('cadastro-conf/', cadastro_conf, name='cadastro-conf'),
    path('logar-conf/', logar_conf, name='logar-conf'),
]
