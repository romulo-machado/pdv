from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Pedido, ItemPedido

def menu(request):
    produtos = Produto.objects.filter(categoria='pizza')

    pedido_id = request.session.get('pedido_id')
    if pedido_id:
        pedido = Pedido.objects.get(id=pedido_id)
    else:
        pedido = None

    return render(request, 'registrador/menu.html', {'produtos': produtos, 'pedido': pedido})

def combos(request):
    produtos = Produto.objects.filter(categoria='combo')
    return render(request, 'registrador/combos.html', {'produtos': produtos})

def lanches(request):
    produtos = Produto.objects.filter(categoria='lanche')
    return render(request, 'registrador/lanches.html', {'produtos': produtos})

def bebidas(request):
    produtos = Produto.objects.filter(categoria='bebida')
    return render(request, 'registrador/bebidas.html', {'produtos': produtos})


def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    pedido_id = request.session.get('pedido_id')
    if pedido_id:
        pedido = Pedido.objects.get(id=pedido_id)
    else:
        pedido = Pedido.objects.create()
        request.session['pedido_id'] = pedido.id

    item, created = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)
    if not created:
        item.quantidade += 1
        item.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def ver_carrinho(request):
    pedido_id = request.session.get('pedido_id')
    if not pedido_id:
        pedido = None
    else:
        pedido = Pedido.objects.get(id=pedido_id)

    return render(request, 'registrador/carrinho.html', {'pedido': pedido})


def finalizar_pedido(request):
    pedido_id = request.session.get('pedido_id')
    if pedido_id:
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.finalizado = True
        pedido.save()
        del request.session['pedido_id']

    return redirect('menu')

def excluir_item(request, id):
    item = get_object_or_404(ItemPedido, id=id)
    item.delete()
    return redirect('carrinho')
