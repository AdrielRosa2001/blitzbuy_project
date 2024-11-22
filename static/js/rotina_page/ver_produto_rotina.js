// Metods:

const getHeadRotina = async (id_rotina) => {
  const response = await fetch(`${id_rotina}/atualizar_head_rotina`)
  const html = await response.text();
  GbID("conteudo-head-rotina").innerHTML = html;
};

const editarProduto = async (data) => {
    // console.log(data);
    const response = await fetch(`/app/${data['fluxo-id']}/atualizar_produto_fluxo`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": data.csrfmiddlewaretoken,
        },
        body: JSON.stringify(data)
    });
    const html = await response.text();
    
    Qs(".form-edit-produto-list").reset();
  
    if (response.status == 200){
      produto_display = document.getElementById(`display-item-${data['fluxo-id']}`);
      produto_display.insertAdjacentHTML('beforebegin', html);
      produto_display.remove();
      getHeadRotina(data['rotina-id']);
      checkedItem(id_rotina=data['fluxo-id'], categoria_id=data['select-categoria']);
      createNewToast("O produto foi atualizado com sucesso!", emoji_success);
    } else {
      createNewToast("Houve um erro ao tentar atualizar o produto!", emoji_failed);
    }
    
};

function updateDonutChart(categoria_id, current, max) {
  const percentage = (current / max) * 100;
  const circle = document.querySelector(`.donut-segment-${categoria_id}`);
  
  // Atualiza a proporção do donut
  circle.style.strokeDasharray = `${percentage} ${100 - percentage}`;
  if (percentage == 100){
    circle.style.stroke = "#198754";
  } else {
    circle.style.stroke = "#0D6EFD";
  };

}

function updateFeedbackNumber(categoria_id){
  let numeros_totais = 0;
  let numeros_marcados = 0;
  QsAll(`.accordion-body-${categoria_id} .rotina-unica`).forEach((el) => {
    numeros_totais = numeros_totais + 1;
    if (el.classList.contains('checked-item-list')){ 
      numeros_marcados = numeros_marcados + 1;
    };
  });
  GbID(`count-prod-rotina-${categoria_id}`).innerHTML = `${numeros_marcados}/${numeros_totais}`;
  updateDonutChart(categoria_id, numeros_marcados, numeros_totais);
}

function verificarEColapsarCategoria(categoria_id){
  let click_colaps = true;
  QsAll(`.accordion-body-${categoria_id} .rotina-unica`).forEach((el) => {
    if (!el.classList.contains('checked-item-list')){ 
      click_colaps = false
    };
  });
  if (click_colaps == true){
    GbID(`btn-categoria-collapse-${categoria_id}`).click();
  };
};

const checkedItem = async (id_rotina, categoria_id) => {
    const response = await fetch(`/app/${id_rotina}/checked_fluxo`);
    const response_text = await response.text();
    if (response_text === "True"){
      document.getElementById(`display-item-${id_rotina}`).classList.add('checked-item-list');
      document.getElementById(`checkbox-item-${id_rotina}`).setAttribute('checked', '');
      verificarEColapsarCategoria(categoria_id);
    } else if (response_text === "False"){
      document.getElementById(`display-item-${id_rotina}`).classList.remove('checked-item-list');
      document.getElementById(`checkbox-item-${id_rotina}`).removeAttribute('checked');
    };
    updateFeedbackNumber(categoria_id);
   
};
  
const verProdutoLista = async (id_fluxo) => {
    const response = await fetch(`${id_fluxo}/ver_produto_fluxo`);
    const html = await response.text();
    const modalVerProduto = document.getElementById("info-produto");
    modalVerProduto.innerHTML = "";
    modalVerProduto.insertAdjacentHTML('beforeend', html);
   
};

const apagarProduto = async (id_fluxo) => {
  const response = await fetch(`${id_fluxo}/apagar_produto_fluxo`);
  const html = await response.text();

  if (response.status == 200){
    Qs('.fluxo-display').innerHTML = '';
    Qs('.fluxo-display').innerHTML = html;
    createNewToast("O produto foi apagado com sucesso!", emoji_success);
  } else {
    createNewToast("Houve um erro ao apagar o produto!", emoji_failed);
  };

};

function setAllDonauts() {
  QsAll('.block-category').forEach((el) => {
    categoria_id = el.querySelector("#id-categoria-dropp").value;
      updateFeedbackNumber(categoria_id);
  });
};

// EVENTS:

document.querySelector(".verProduto").addEventListener('submit', (e) => {
    // Preparando dicionário com os dados do forms
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
  
    // Chamando função para criar os dados
    editarProduto(data);
  });