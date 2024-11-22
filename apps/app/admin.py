from django.contrib import admin
from .models import CategoriaProduto, StatusRotina, Produto, RotinaDeCompra, FluxoDeRotina

admin.site.register(CategoriaProduto)
admin.site.register(StatusRotina)
admin.site.register(Produto)
admin.site.register(RotinaDeCompra)
admin.site.register(FluxoDeRotina)
