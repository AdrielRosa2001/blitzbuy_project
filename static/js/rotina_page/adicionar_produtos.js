// Metods:

function increment_quant() {
    const input_quant_prod = Qs(".input-quant-produto");
    if (input_quant_prod.value === ""){
      input_quant_prod.value = 1;
    } else {
      new_value = parseInt(input_quant_prod.value, 10) + 1;
      if (new_value < 1 ){
        input_quant_prod.value = 1;
      } else {
        input_quant_prod.value = new_value;
      };
    };
};
  
function decrement_quant() {
    const input_quant_prod = Qs(".input-quant-produto");
    if (input_quant_prod.value === ""){
      input_quant_prod.value = 1;
    } else {
      new_value = parseInt(input_quant_prod.value, 10) - 1
      if (new_value < 1 ){
        input_quant_prod.value = 1;
      } else {
        input_quant_prod.value = new_value;
      };
    };
};
  
const adicionarProduto = async (data) => {
    // console.log(data);
    const elemento_nenhum_produto_localizado = Qs(".nenhum-produto");
    const response = await fetch(`/app/criar_novo_fluxo/add`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": data.csrfmiddlewaretoken,
        },
        body: JSON.stringify(data)
    });
    const html = await response.text();
    if (response.status == 200){
      Qs('.fluxo-display').innerHTML = '';
      Qs('.fluxo-display').innerHTML = html;
      getHeadRotina(data['rotina-id']);
      updateFeedbackNumber(data['select-categoria']);
      // createNewToast("O produto foi adicionado com sucesso!", emoji_success);
    } else {
      createNewToast("Houve um erro ao adicionar o produto!", emoji_failed);
    };
    Qs(".form-add-produto").reset();
};
  
const buscarProdutos = async (lista_produtos_retornados) => {
  const map_data = {"search_produto_name": GbID("nome-produto").value };
  const response = await fetch(`/app/criar_novo_fluxo/add/buscar_produtos/${map_data['search_produto_name']}`);
  const html = await response.text();
  if (response.status == 200){
      lista_produtos_retornados.classList.remove('d-none')
      lista_produtos_retornados.innerHTML = html;
    } else {
      if (!lista_produtos_retornados.classList.contains('d-none')) {
          lista_produtos_retornados.classList.add('d-none')
      };
  };
    
};

function definindoProduto(nome_produto, id_categoria_produto) {
    GbID("nome-produto").value=nome_produto;
    QsAll('.select-categoria option').forEach((el) => {
        if (el.value === id_categoria_produto){
            el.setAttribute('selected', '');
        };
    });
    if (!GbID("lista-escolha-produtos").classList.contains('d-none')) {
        lista_produtos_retornados.classList.add('d-none')
    };
}

// EVENTS:

Qs(".form-add-produto").addEventListener('submit', (e) => {
    // Preparando dicionário com os dados do forms
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
  
    // Chamando função para criar os dados
    adicionarProduto(data);
  });

// GbID("nome-produto").addEventListener('focus', (e) => {
//     GbID("nome-produto").addEventListener('keypress', (el) => {
//         busca = GbID("nome-produto").value
//         lista_produtos_retornados = GbID("lista-escolha-produtos");
//         if (busca.length >= 3){
//             buscarProdutos(lista_produtos_retornados);

//         } else {
//             if (!lista_produtos_retornados.classList.contains('d-none')) {
//                 lista_produtos_retornados.classList.add('d-none')
//             };
//         };
//     });
//     // GbID("nome-produto").addEventListener('blur', (ele) => {
//     //     if (!lista_produtos_retornados.classList.contains('d-none')) {
//     //         lista_produtos_retornados.classList.add('d-none')
//     //     };
//     // });
//  });