import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import CategoriaProduto, RotinaDeCompra, StatusRotina, Produto, FluxoDeRotina

# -------------------- Rotinas --------------------
# VIEW - RENDERIZA PÁGINA PRINCIPAL DE EXIBIÇÃO
@login_required
def main(request):
    # status_rotina = StatusRotina.objects.get(nome_status="PENDENTE")
    rotinas = RotinaDeCompra.objects.filter(user=request.user).order_by("-iniciada_em")
    status_retornados = StatusRotina.objects.all()
    status_rotinas = []
    for status in status_retornados:
        quant_rotina = 0
        for rotina in rotinas:
            if rotina.status_rotina.nome_status == status.nome_status:
                quant_rotina = quant_rotina + 1
        status_rotinas.append({"status": status, "quant_rotinas": quant_rotina})
    context = {"rotinas": rotinas, "status_rotinas": status_rotinas}
    return render(request, "app/main.html", context)

# CREATE - CRIA UMA NOVA ROTINA
@login_required
def criar_nova_rotina(request):
    data = json.loads(request.body)
    status_nova_rotina = StatusRotina.objects.get(nome_status="PENDENTE")
    nova_rotina = RotinaDeCompra.objects.create(user=request.user, status_rotina=status_nova_rotina, local_de_compra=data['localDeCompras'])
    context = {"rotina": nova_rotina}
    return render(request, "app/components/main_page/elements/rotina_unica.html", context)

# READE - VER UMA ROTINA JÁ CRIADA
@login_required
def ver_rotina(request, pk):
    rotina = RotinaDeCompra.objects.get(id=int(pk))
    context = atualizar_lista_content(rotina.id)
    context['rotina'] = rotina
    # context = {"rotina": rotina, "fluxo_de_rotinas": fluxo_de_rotinas, "categorias": categorias_produto, "categorias_contidas": categorias_contidas}
    return render(request, "app/rotina_page.html", context)

# UPDATE - ATUALIZA UMA ROTINA JÁ CRIADA
@login_required
def update_local_rotina(request, pk_rotina, novo_local):
    try:
        rotina = RotinaDeCompra.objects.get(id=int(pk_rotina))
        rotina.local_de_compra = novo_local
        rotina.save()
        return HttpResponse("Local de rotina alterada com sucesso!", status=200)
    except Exception as error:
        return HttpResponse("Houve um erro ao salvar o local da rotina!", status=500)

# DELETE - DELETA UMA ROTINA JÁ CRIADA
@login_required
def deletar_rotina(request, pk):
    rotina = RotinaDeCompra.objects.get(id=int(pk))
    rotina.delete()
    return HttpResponse("Rotina deletada com sucesso!")

# READE_ALL - LISTA VARIAS ROTINAS
@login_required
def listar_rotinas(request):
    rotinas = RotinaDeCompra.objects.filter(user=request.user)
    context = {"rotinas": rotinas}
    return render(request, "app/components/main_page/elements/display_de_rotinas.html", context)

# METHOD - DEFINE COMO CONCLUÍDA UMA ROTINA EXISTENTE
@login_required
def finalizar_rotina(request, pk_rotina):
    novo_satus = StatusRotina.objects.get(nome_status="CONCLUIDA")
    rotina = RotinaDeCompra.objects.get(id=int(pk_rotina))
    rotina.status_rotina = novo_satus
    rotina.save()
    return HttpResponse(f"Rotina finalizada com sucesso!: {pk_rotina}")

# METHOD - ATUALIZA O CONTAINER HEADER DA PÁGINA DA ROTINA
@login_required
def atualizar_head_rotina(request, pk_fluxo, pk_rotina):
    rotina = RotinaDeCompra.objects.get(id=int(pk_rotina))
    fluxos_de_rotina = FluxoDeRotina.objects.filter(rotina=rotina)
    valor_total_rotina = 0.00
    for produto in fluxos_de_rotina:
        valor_total_rotina = valor_total_rotina + produto.valor_total_produto
    rotina.valor_total = valor_total_rotina
    rotina.save()
    context = {"rotina": rotina}
    return render(request, "app/components/rotina_page/elements/conteudo_head_rotina.html", context)

# -------------------- Produtos --------------------

# CREATE - CRIA UM NOVO PRODUTO NO BANCO DE DADOS
@login_required
def criar_novo_produto(request):
    data = json.loads(request.body)
    categoria_produto = CategoriaProduto.objects.get(id=int(data['select-categoria']))
    produto = Produto.objects.create(nome_produto=data['nome-produto'], categoria=categoria_produto)
    context = {"produto": produto}
    return render(request, "app/components/main_page/elements/rotina_unica.html", context)

# READE - LOCALIZA E EXIBE UM PRODUTO JÁ EXISTENTE
@login_required
def produtos_localizados(request, nome_produto):
    produtos_localizados = Produto.objects.filter(nome_produto__icontains=nome_produto)
    if produtos_localizados:
        return render(request, "app/components/rotina_page/elements/lista_de_produtos_consulta.html", {"produtos_localizados": produtos_localizados})
    else:
        return HttpResponse("Produto não encontrado!", status=404)

# -------------------- Fluxo de rotina --------------------
# METHOD - ATUALIZA INFORMAÇÕES REFERENTES A UM FLUXO DE ROTINA EXISTENTE
def atualizar_lista_content(id_rotina):
    rotina = RotinaDeCompra.objects.get(id=int(id_rotina))
    fluxo_de_rotinas = FluxoDeRotina.objects.filter(rotina=rotina)
    categorias_produto = CategoriaProduto.objects.all().order_by("nome_categoria")
    categorias_contidas = []
    categorias_contidas_referencia = []
    valor_total_rotina = 0.00
    for fluxo in fluxo_de_rotinas:  
        valor_total_rotina = valor_total_rotina + fluxo.valor_total_produto
        if not fluxo.produto.categoria.nome_categoria in categorias_contidas_referencia:
            categoria = CategoriaProduto.objects.get(nome_categoria=fluxo.produto.categoria.nome_categoria)
            categorias_contidas_referencia.append(categoria.nome_categoria)
            if fluxo.checked == False:
                categorias_contidas.append({"categoria": categoria, "colapse_categoria": True})
            else:
                categorias_contidas.append({"categoria": categoria, "colapse_categoria": False})

        else:
            for categoria in categorias_contidas:
                if categoria['categoria'].nome_categoria == fluxo.produto.categoria.nome_categoria:
                    if fluxo.checked == False:
                        categoria['colapse_categoria'] = True

    rotina.valor_total = valor_total_rotina
    rotina.save()
    context = {"fluxo_de_rotinas": fluxo_de_rotinas, "categorias": categorias_produto, "categorias_contidas": categorias_contidas}
    return context

# CREATE - CRIA UM NOVO FLUXO DE ROTINA
@login_required
def criar_novo_fluxo(request):
    data = json.loads(request.body)

    rotina = RotinaDeCompra.objects.get(id=int(data['rotina-id']))
    categoria_produto = CategoriaProduto.objects.get(id=int(data['select-categoria']))
    produto = None
    try:
        produto = Produto.objects.get(nome_produto=data['nome-produto'])
        produto.categoria = categoria_produto
        produto.save()
    except:
        pass
    if not produto:
        descricao = data['descricao-produto']
        produto = Produto.objects.create(nome_produto=data['nome-produto'], categoria=categoria_produto, descricao=descricao)
    quant_produto = 0.0
    valor_produto = 0.0
    try:
        quant_produto = float(data['quant-produto'])
    except:
        pass
    try:
        valor_produto = float(data['valor-produto'])
    except:
        pass
    valor_total_produto = quant_produto * valor_produto
    FluxoDeRotina.objects.create(rotina=rotina, produto=produto, quant_produto=quant_produto, valor_produto=valor_produto, valor_total_produto=valor_total_produto)
    
    context = atualizar_lista_content(rotina.id)

    # context = {"fluxo_de_rotinas": fluxo_de_rotinas, "categorias": categorias_produto, "categorias_contidas": categorias_contidas}
    return render(request, "app/components/rotina_page/elements/display_produtos_rotina.html", context)

# READE - VISUALIZA UM FLUXO DE ROTINA JÁ CRIADO
@login_required
def ver_produto_fluxo(request, pk_rotina, pk_fluxo):
    fluxo_de_rotina = FluxoDeRotina.objects.get(id=int(pk_fluxo))
    quantidade = str(fluxo_de_rotina.quant_produto).replace(",", ".")
    valor_produto = str(fluxo_de_rotina.valor_produto).replace(",", ".")
    categorias = CategoriaProduto.objects.all().order_by("nome_categoria")
    context = {"produto": fluxo_de_rotina, "quantidade": quantidade, "valor_produto": valor_produto, "categorias": categorias}
    return render(request, "app/components/rotina_page/modals/modal_ver_produto_conteudo.html", context)

# UPDATE - ATUALIZA UM FLUXO DE ROTINA JÁ CRIADO
@login_required
def atualizar_produto_fluxo(request, pk_fluxo):
    fluxo_de_rotina = FluxoDeRotina.objects.get(id=int(pk_fluxo))
    data = json.loads(request.body)
    fluxo_de_rotina.quant_produto = float(data['quant-produto-view'])
    fluxo_de_rotina.valor_produto = float(data['valor-produto-view'])
    fluxo_de_rotina.valor_total_produto = float(data['quant-produto-view']) * float(data['valor-produto-view'])
    fluxo_de_rotina.save()
    if fluxo_de_rotina.produto.categoria.id != int(data['select-categoria']):
        produto = Produto.objects.get(id=fluxo_de_rotina.produto.id)
        nova_categoria = CategoriaProduto.objects.get(id=int(data['select-categoria']))
        produto.categoria = nova_categoria
        produto.save()
    context = {"produto": fluxo_de_rotina}
    return render(request, "app/components/rotina_page/elements/produto_unico_rotina.html", context)

# DELETE - APAGA UM FLUXO DE ROTINA JÁ CRIADO
@login_required
def apagar_produto_fluxo(request, pk_rotina, pk_fluxo):
    fluxo_de_rotina = FluxoDeRotina.objects.get(id=int(pk_fluxo))
    id_rotina = fluxo_de_rotina.rotina.id
    fluxo_de_rotina.delete()
    context = atualizar_lista_content(id_rotina)
    return render(request, "app/components/rotina_page/elements/display_produtos_rotina.html", context)

# METHOD - MARCA UM FLUXO COMO REALIZADO OU PENDENTE REALIZAÇÃO
@login_required
def checked_mark_fluxo(request, pk):
    fluxo_de_rotina = FluxoDeRotina.objects.get(id=int(pk))
    new_status_check = None
    if fluxo_de_rotina.checked == False:
        fluxo_de_rotina.checked = True
        fluxo_de_rotina.save()
    else:
        fluxo_de_rotina.checked = False
        fluxo_de_rotina.save()
        
    new_status_check = fluxo_de_rotina.checked
    return HttpResponse(new_status_check)

# -------------------- Rotina concluídas --------------------

@login_required
def visualizar_rotina_concluida(request, pk_rotina  ):
    rotina = RotinaDeCompra.objects.get(id=pk_rotina)
    lista_de_produtos = FluxoDeRotina.objects.filter(rotina=pk_rotina).order_by("criada_em")
    context = {"lista_de_produtos": lista_de_produtos, "rotina": rotina}
    return render(request, "app/rotina_concluida_page.html", context)