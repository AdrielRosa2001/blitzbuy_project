from django.db import models
from django.conf import settings

class CategoriaProduto(models.Model):
    nome_categoria = models.CharField(max_length=100, unique=True)
    cor_categoria = models.CharField(max_length=7, default="#FFFFFF")
    imagem = models.CharField(max_length=250, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    deletavel = models.BooleanField(default=True)
    editavel = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.nome_categoria}"

class StatusRotina(models.Model):
    nome_status = models.CharField(max_length=100, unique=True)
    cor_status = models.CharField(max_length=7, default="#FFFFFF")
    deletavel = models.BooleanField(default=True)
    editavel = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.nome_status}"
    
class Produto(models.Model):
    nome_produto = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(CategoriaProduto, default="SEM_CATEGORIA", on_delete=models.SET_DEFAULT)
    imagem = models.CharField(max_length=250, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.nome_produto}"

class RotinaDeCompra(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status_rotina = models.ForeignKey(StatusRotina, on_delete=models.SET_NULL, null=True, blank=True)
    local_de_compra = models.CharField(max_length=250, null=True, blank=True)
    iniciada_em = models.DateTimeField(auto_now_add=True)
    finalizada_em = models.DateTimeField(null=True, blank=True)
    valor_total = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f"{self.iniciada_em} - {self.user.username}"

class FluxoDeRotina(models.Model):
    criada_em = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)
    rotina = models.ForeignKey(RotinaDeCompra, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, default="PRODUTO_DELETADO", on_delete=models.SET_DEFAULT)
    quant_produto = models.FloatField(default=0.0)
    valor_produto = models.FloatField(default=0.0)
    valor_total_produto = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f"{self.criada_em} - {self.rotina}"

