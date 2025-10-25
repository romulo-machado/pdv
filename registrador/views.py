from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Produto, Pedido, ItemPedido, TamanhoPizza
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import datetime
# Importações removidas para compatibilidade com Linux

def espeto(request):
    query = request.GET.get('q')  # busca o valor do campo 'q' na URL

    if query:
        produtos = Produto.objects.filter(categoria='espeto', nome__icontains=query)
        produtos_refeicao = Produto.objects.filter(categoria='pf_refeicao', nome__icontains=query)
        produtos_espeto = Produto.objects.filter(categoria='porcoes', nome__icontains=query)
    else:
        produtos = Produto.objects.filter(categoria='espeto')
        produtos_refeicao = Produto.objects.filter(categoria='pf_refeicao')
        produtos_espeto = Produto.objects.filter(categoria='porcoes')

    pedido_id = request.session.get('pedido_id')
    if pedido_id:
        pedido = Pedido.objects.get(id=pedido_id)
    else:
        pedido = None

    return render(request, 'registrador/espeto.html', {
        'produtos_espeto': produtos_espeto,
        'produtos_refeicao': produtos_refeicao,
        'produtos': produtos,
        'pedido': pedido,
        'query': query  # envia a query de volta pro template (opcional)
    })

def menu(request):
    query = request.GET.get('q')  # busca o valor do campo 'q' na URL

    if query:
        produtos = Produto.objects.filter(categoria='pizza', nome__icontains=query)
    else:
        produtos = Produto.objects.filter(categoria='pizza')

    pedido_id = request.session.get('pedido_id')
    if pedido_id:
        pedido = Pedido.objects.get(id=pedido_id)
    else:
        pedido = None

    return render(request, 'registrador/menu.html', {
        'produtos': produtos,
        'pedido': pedido,
        'query': query  # envia a query de volta pro template (opcional)
    })

def entrada(request):
    query = request.GET.get('q')  # busca o valor do campo 'q' na URL

    if query:
        produtos = Produto.objects.filter(categoria='entrada', nome__icontains=query)
    else:
        produtos = Produto.objects.filter(categoria='entrada')

    pedido_id = request.session.get('pedido_id')
    if pedido_id:
        pedido = Pedido.objects.get(id=pedido_id)
    else:
        pedido = None

    return render(request, 'registrador/entrada.html', {
        'produtos': produtos,
        'pedido': pedido,
        'query': query  # envia a query de volta pro template (opcional)
    })

def combos(request):
    tamanhos = TamanhoPizza.objects.all()
    return render(request, 'registrador/combos.html', {'tamanhos': tamanhos})

def combos_sabores(request, tamanho, preco):
    sabores = Produto.objects.filter(categoria='sabor_promocao')  # ou outro filtro que represente os sabores disponíveis
    return render(request, 'registrador/combos_sabores.html', {
        'tamanho': tamanho,
        'sabores': sabores,
        'preco': preco,
    })

def lanches(request):
    query = request.GET.get('q')  # GET com G maiúsculo, mas .get com g minúsculo
    if query:
        produtos = Produto.objects.filter(categoria='lanche', nome__icontains=query)
    else:
        produtos = Produto.objects.filter(categoria='lanche')

    return render(request, 'registrador/lanches.html', {
        'produtos': produtos,
        'query': query,
    })

def bebidas(request):
    query = request.GET.get('q')

    if query:
        produtos = Produto.objects.filter(categoria='bebida', nome__icontains=query)
    else:
        produtos = Produto.objects.filter(categoria='bebida')
    return render(request, 'registrador/bebidas.html', {
        'produtos': produtos,
        'query': query
        })

def artesanais(request):
    query = request.GET.get('q')
    if query:
        produtos = Produto.objects.filter(categoria='artesanal',nome__icontains=query)
    else:
        produtos = Produto.objects.filter(categoria='artesanal')
    return render(request, 'registrador/artesanal.html', {
        'produtos': produtos,
        'query': query,
        })

def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))  # 🟢 Pega a quantidade enviada

    pedido_id = request.session.get('pedido_id')
    if pedido_id:
        pedido = Pedido.objects.get(id=pedido_id)
    else:
        pedido = Pedido.objects.create()
        request.session['pedido_id'] = pedido.id

    item, created = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)
    if created:
        item.quantidade = quantidade
    else:
        item.quantidade += quantidade
    item.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))  # 🔁 Retorna para a mesma página

def ver_carrinho(request):
    pedido_id = request.session.get('pedido_id')
    if not pedido_id:
        pedido = None
    else:
        pedido = Pedido.objects.get(id=pedido_id)

    return render(request, 'registrador/carrinho.html', {'pedido': pedido})

@require_POST
def finalizar_pedido(request):
    pedido_id = request.session.get('pedido_id')
    if not pedido_id:
        return redirect('menu')

    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Salvar os campos do formulário
    pedido.nome_cliente = request.POST.get('nome_cliente')
    pedido.local_consumo = request.POST.get('local_consumo')
    
    # Processar múltiplas formas de pagamento com valores
    formas_pagamento = request.POST.getlist('forma_pagamento')
    detalhes_pagamento = []
    
    for forma in formas_pagamento:
        valor_campo = f'valor_{forma.lower()}'
        valor = request.POST.get(valor_campo, '0')
        if valor and float(valor) > 0:
            detalhes_pagamento.append(f'{forma}: R$ {float(valor):.2f}')
    
    pedido.forma_pagamento = ' | '.join(detalhes_pagamento) if detalhes_pagamento else ''
    
    pedido.finalizado = True
    pedido.save()

    # Renderizar página de impressão com os dados do pedido
    context = {
        'pedido': pedido,
        'imprimir': True
    }

    # Limpar o carrinho da sessão
    del request.session['pedido_id']

    return render(request, 'registrador/cupom_impressao.html', context)

def excluir_item(request, id):
    item = get_object_or_404(ItemPedido, id=id)
    item.delete()
    return redirect('carrinho')

@csrf_exempt
def adicionar_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        produto_id = data.get('produto_id')
        quantidade = int(data.get('quantidade', 1))

        produto = get_object_or_404(Produto, id=produto_id)

        pedido_id = request.session.get('pedido_id')
        if pedido_id:
            pedido = Pedido.objects.get(id=pedido_id)
        else:
            pedido = Pedido.objects.create()
            request.session['pedido_id'] = pedido.id

        item, created = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)
        if created:
            item.quantidade = quantidade
        else:
            item.quantidade += quantidade
        item.save()

        return JsonResponse({'sucesso': True})
    
    return JsonResponse({'sucesso': False}, status=400)

@csrf_exempt
def adicionar_pizza_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        produto_id = data.get('produto_id')
        quantidade = int(data.get('quantidade', 1))
        tamanho = data.get('tamanho')
        sabor2_id = data.get('sabor2_id')

        produto = get_object_or_404(Produto, id=produto_id)
        sabor2 = None
        
        if sabor2_id:
            sabor2 = get_object_or_404(Produto, id=sabor2_id)

        # Calcular preço baseado no tamanho e sabores
        from decimal import Decimal
        
        # Definir multiplicadores por tamanho
        multiplicadores = {
            'Pequena': Decimal('1.0'),
            'Média': Decimal('1.0'),
            'Grande': Decimal('1.0'),
            'Gigante': Decimal('1.0')
        }
        
        # Sempre usar o maior preço entre os sabores (se houver segundo sabor)
        preco_sabor1 = produto.preco or Decimal('0')
        if sabor2:
            preco_sabor2 = sabor2.preco or Decimal('0')
            # Para pizza de dois sabores: usar sempre o MAIOR preço SEM multiplicador
            preco_final = max(preco_sabor1, preco_sabor2)
        else:
            # Para pizza de um sabor: aplicar o multiplicador de tamanho
            preco_base = preco_sabor1
            preco_final = preco_base * multiplicadores.get(tamanho, Decimal('1.0'))

        # Criar descrição do produto
        if sabor2:
            descricao = f"Pizza {tamanho} - 1/2 {produto.nome} + 1/2 {sabor2.nome}"
        else:
            descricao = f"Pizza {tamanho} - {produto.nome}"

        pedido_id = request.session.get('pedido_id')
        if pedido_id:
            pedido = Pedido.objects.get(id=pedido_id)
        else:
            pedido = Pedido.objects.create()
            request.session['pedido_id'] = pedido.id

        # Criar novo item sempre (não somar com existente para permitir diferentes tamanhos)
        item = ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=preco_final,
            descricao_produto=descricao,
            sabor2=sabor2
        )

        return JsonResponse({'sucesso': True})
    
    return JsonResponse({'sucesso': False}, status=400)

@require_POST
def adicionar_combo(request):
    tamanho = request.POST.get('tamanho')
    preco_combo = request.POST.get('preco')

    sabor1 = get_object_or_404(Produto, id=request.POST.get('sabor1'))

    if tamanho in ['Média' , 'Pequena']:
        sabor2 = get_object_or_404(Produto, id=request.POST.get('sabor1'))
    else:
        sabor2 = get_object_or_404(Produto, id=request.POST.get('sabor2'))

    # Produto genérico para combos personalizados
    produto_base = get_object_or_404(Produto, nome='Pizza Combo Personalizado')

    # Descrição detalhada do combo
    descricao_combo = f"Pizza {tamanho} - 1/2 {sabor1.nome} + 1/2 {sabor2.nome}"

    # Obter ou criar o pedido da sessão
    pedido_id = request.session.get('pedido_id')
    if not pedido_id:
        pedido = Pedido.objects.create()
        request.session['pedido_id'] = pedido.id
    else:
        pedido = Pedido.objects.get(id=pedido_id)

    # Criar item no carrinho com preço e descrição personalizada
    ItemPedido.objects.create(
        pedido=pedido,
        produto=produto_base,
        quantidade=1,
        preco_unitario=preco_combo,
        descricao_produto = descricao_combo
    )

    return redirect('menu')

def atualizar_observacao(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id)
    if request.method == "POST":
        observacao = request.POST.get("observacao", "").strip()
        item.observacao = observacao
        item.save()
    return redirect("carrinho")

def relatorio_vendas(request):
    pedidos = Pedido.objects.filter(finalizado=True).order_by('-criado_em')
    
    # Filtros por data/hora
    data_inicio = request.GET.get('data_inicio')
    hora_inicio = request.GET.get('hora_inicio', '00:00')
    data_fim = request.GET.get('data_fim')
    hora_fim = request.GET.get('hora_fim', '23:59')
    
    if data_inicio and data_fim:
        from datetime import datetime
        # Combinar data e hora
        datetime_inicio = datetime.strptime(f"{data_inicio} {hora_inicio}", '%Y-%m-%d %H:%M')
        datetime_fim = datetime.strptime(f"{data_fim} {hora_fim}", '%Y-%m-%d %H:%M')
        
        pedidos = pedidos.filter(
            criado_em__gte=datetime_inicio,
            criado_em__lte=datetime_fim
        )
    
    # Calcular totais por forma de pagamento
    totais_pagamento = {
        'Dinheiro': 0,
        'Credito': 0,
        'Debito': 0,
        'Pix': 0
    }
    
    total_geral = 0
    
    for pedido in pedidos:
        total_geral += pedido.total()
        
        if pedido.forma_pagamento:
            # Processar múltiplas formas de pagamento
            formas = pedido.forma_pagamento.split(' | ')
            for forma in formas:
                if ':' in forma:
                    nome_forma, valor_str = forma.split(': R$ ')
                    try:
                        valor = float(valor_str)
                        nome_forma = nome_forma.strip()
                        if nome_forma in totais_pagamento:
                            totais_pagamento[nome_forma] += valor
                    except ValueError:
                        continue
    
    # Calcular ticket médio
    num_pedidos = pedidos.count()
    ticket_medio = total_geral / num_pedidos if num_pedidos > 0 else 0
    
    context = {
        'pedidos': pedidos,
        'totais_pagamento': totais_pagamento,
        'total_geral': total_geral,
        'num_pedidos': num_pedidos,
        'ticket_medio': ticket_medio,
        'data_inicio': data_inicio,
        'hora_inicio': hora_inicio,
        'data_fim': data_fim,
        'hora_fim': hora_fim,
    }
    
    return render(request, 'registrador/relatorio.html', context)


