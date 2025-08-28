from django.db import models

from django.db import models

class Produto(models.Model):
    CATEGORIAS = (
        ('combo', 'Combo'),
        ('pizza', 'Pizza'),
        ('lanche', 'Lanche'),
        ('bebida', 'Bebida'),
        ('artesanal', 'Artesanal'),
        ('sabor_promocao', 'Promocao'),
        ('entrada', 'Entrada'),
    )

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)
    nome_cliente = models.CharField(max_length=100, blank=True, null=True)
    local_consumo = models.CharField(max_length=100, blank=True, null=True)
    forma_pagamento = models.CharField(max_length=200, blank=True, null=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f"Pedido #{self.id} - {self.nome_cliente or 'Sem nome'}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    descricao_produto = models.CharField(max_length=150, blank=True, null=True)
    observacao = models.CharField(max_length=255, null=True, blank=True)
    sabor2 = models.ForeignKey(Produto, related_name='itens_sabor2', on_delete=models.CASCADE, null=True, blank=True)

    def subtotal(self):
        if self.preco_unitario:
            return self.quantidade * self.preco_unitario
        elif hasattr(self.produto, 'preco'):
            return self.quantidade * self.produto.preco
        return 0  # ou lançar erro

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

class TamanhoPizza(models.Model):
    nome = models.CharField(max_length=20, unique=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco:.2f}"
