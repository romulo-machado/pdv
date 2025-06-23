from django.db import models

from django.db import models

class Produto(models.Model):
    CATEGORIAS = (
        ('combo', 'Combo'),
        ('pizza', 'Pizza'),
        ('lanche', 'Lanche'),
        ('bebida', 'Bebida'),
    )

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)

    def __str__(self):
        return self.nome



class Pedido(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f"Pedido #{self.id}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def subtotal(self):
        return self.quantidade * self.produto.preco

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
