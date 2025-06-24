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

import win32print
import win32ui

def imprimir_pedido(pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)

    nome_impressora = "POS-80 (copy 1)"  # Verifique o nome correto da sua impressora no Windows

    # Comandos ESC/POS
    texto_grande = b'\x1b!\x38'  # Dobro altura e largura
    reset_texto = b'\x1b!\x00'   # Voltar ao texto normal
    centralizar = b'\x1b\x61\x01'  # Centralizar texto
    alinhar_esquerda = b'\x1b\x61\x00'  # Alinhar à esquerda
    corte = b'\x1dV\x00'  # Corte total de papel

    hPrinter = win32print.OpenPrinter(nome_impressora)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Pedido", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)

        # Cabeçalho
        win32print.WritePrinter(hPrinter, centralizar)
        win32print.WritePrinter(hPrinter, texto_grande)
        win32print.WritePrinter(hPrinter, b"PIZZARIA TOP\n")
        win32print.WritePrinter(hPrinter, reset_texto)

        # Número do pedido destacado
        win32print.WritePrinter(hPrinter, texto_grande)
        win32print.WritePrinter(hPrinter, f"Pedido #{pedido.id}\n".encode('utf-8'))
        win32print.WritePrinter(hPrinter, reset_texto)

        win32print.WritePrinter(hPrinter, b"==========================\n")

        # Itens do pedido em tamanho grande
        win32print.WritePrinter(hPrinter, alinhar_esquerda)
        win32print.WritePrinter(hPrinter, texto_grande)
        for item in pedido.itens.all():
            linha = f"{item.quantidade}x {item.produto.nome}\n"
            win32print.WritePrinter(hPrinter, linha.encode('utf-8'))
        win32print.WritePrinter(hPrinter, reset_texto)

        win32print.WritePrinter(hPrinter, b"==========================\n")
        win32print.WritePrinter(hPrinter, centralizar)
        win32print.WritePrinter(hPrinter, b"\nObrigado pela preferencia!\n\n")
        win32print.WritePrinter(hPrinter, b"==========================\n")

        # Corte de papel
        win32print.WritePrinter(hPrinter, corte)

        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)

def finalizar_pedido(request):
    pedido_id = request.session.get('pedido_id')

    if pedido_id:
        pedido = Pedido.objects.get(id=pedido_id)

        # Marca como finalizado
        pedido.finalizado = True
        pedido.save()

        # Imprime na impressora térmica
        imprimir_pedido(pedido_id)

        # Limpa o carrinho
        del request.session['pedido_id']

    return redirect('menu')  # Ou outra página como "Pedidos Concluídos"