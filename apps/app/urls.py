from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('criar_nova_rotina/', views.criar_nova_rotina, name="criar_nova_rotina"),
    path('<int:pk>/show_rotina', views.ver_rotina, name="show_rotina"),
    path('<int:pk>/delete_rotina', views.deletar_rotina, name="delete_rotina"),
    path('criar_novo_fluxo/add', views.criar_novo_fluxo, name="criar_novo_fluxo"),
    path('criar_novo_fluxo/add/buscar_produtos/<str:nome_produto>', views.produtos_localizados, name="buscar_produtos"),
    path('<int:pk_rotina>/<int:pk_fluxo>/apagar_produto_fluxo', views.apagar_produto_fluxo, name="apagar_produto_fluxo"),
    path('<int:pk_rotina>/<str:novo_local>/update_local_rotina', views.update_local_rotina, name="update_local_rotina"),
    path('<int:pk_rotina>/<int:pk_fluxo>/ver_produto_fluxo', views.ver_produto_fluxo, name="ver_produto_fluxo"),
    path('<int:pk_rotina>/finalizar_rotina', views.finalizar_rotina, name="finalizar_rotina"),
    path('<int:pk_fluxo>/atualizar_produto_fluxo', views.atualizar_produto_fluxo, name="atualizar_produto_fluxo"),
    path('<int:pk_fluxo>/<int:pk_rotina>/atualizar_head_rotina', views.atualizar_head_rotina, name="atualizar_head_rotina"),
    path('<int:pk>/checked_fluxo', views.checked_mark_fluxo, name="checked_fluxo"),
    path('<int:pk_rotina>/visualizar_rotina_concluida', views.visualizar_rotina_concluida, name="visualizar_rotina_concluida"),
]