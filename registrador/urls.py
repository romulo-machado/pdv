from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('artesanal/', views.artesanais, name='artesanais'),
    path('espeto/', views.espeto, name='espeto'),
    path('combos/', views.combos, name='combos'),
    path('entrada/', views.entrada, name='entrada'),
    path('combos/<str:tamanho>/<str:preco>/', views.combos_sabores, name='combos_sabores'),
    path('combos/adicionar/', views.adicionar_combo, name='adicionar_combo'),
    path('lanches/', views.lanches, name='lanches'),
    path('bebidas/', views.bebidas, name='bebidas'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar'),
    path('carrinho/', views.ver_carrinho, name='carrinho'),
    path('finalizar/', views.finalizar_pedido, name='finalizar'),
    path('excluir/<int:id>/', views.excluir_item, name='excluir_item'),
    path('finalizar_pedido/', views.finalizar_pedido, name='finalizar_pedido'),
    path('adicionar-ajax/', views.adicionar_ajax, name='adicionar_ajax'),
    path('adicionar-pizza-ajax/', views.adicionar_pizza_ajax, name='adicionar_pizza_ajax'),
    path("atualizar-observacao/<int:item_id>/", views.atualizar_observacao, name="atualizar_observacao"),
    path('relatorio/', views.relatorio_vendas, name='relatorio_vendas'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
