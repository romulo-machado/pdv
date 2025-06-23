from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('pizza/', views.menu, name='menu'),
    path('combos/', views.combos, name='combos'),
    path('lanches/', views.lanches, name='lanches'),
    path('bebidas/', views.bebidas, name='bebidas'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar'),
    path('carrinho/', views.ver_carrinho, name='carrinho'),
    path('finalizar/', views.finalizar_pedido, name='finalizar'),
    path('excluir/<int:id>/', views.excluir_item, name='excluir_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)