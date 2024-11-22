const editableText = Qs(".local-rotina-editar");
const editableInput = Qs(".local-rotina-input-editar");

// console.log('main_load');

function teste_alert(){
  alert('Teste')
};

// const toastTrigger = document.getElementById('adicionarProdutoBtn')
const toastLiveExample = document.getElementById('liveToast');
const emoji_success = "&#x2705;";
const emoji_failed = "&#x26D4;";

function createNewToast(mensagem, emoji){
  const toastText = document.getElementById("toast-text");
  const toastEmoji = document.getElementById("toast-emoji");
  toastText.innerHTML = mensagem;
  toastEmoji.innerHTML = emoji;
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
  toastBootstrap.show();
}


// Metods:

function editarRotina(id_rotina){
  GbID(`local-rotina-${id_rotina}`);
};

function editarLocalClick(){
  editableText.click()
}

const salvarEdicaoRotina = async (data) => {
  const response = await fetch(`${data['novo_local']}/update_local_rotina`);
  const html = await response.text();

  if (response.status == 200){
    createNewToast("Local de compras alterado com sucesso!", emoji_success);
  } else {
    createNewToast("Houve um erro ao atualizar o local de compras!", emoji_failed);
  };
};


// EVENTS:

Qs(".form-excluir-rotina").addEventListener('submit', (e) => {
  // Preparando dicionário com os dados do forms
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target).entries());
  
  // Chamando função para criar os dados
  excluirRotina(data);
});


// Quando clica no texto, exibe o input e esconde o texto
editableText.addEventListener('click', function () {
    editableText.style.display = 'none';
    editableInput.style.display = 'block';
    editableInput.focus(); // Dá foco no input
});

// Quando o input perde o foco, atualiza o texto e volta para o modo de visualização
editableInput.addEventListener('blur', function () {
    salvarEdicaoRotina({"id_rotina": GbID("id_rotina_head").value, "novo_local": editableInput.value})
    editableText.textContent = editableInput.value;
    editableText.style.display = 'inline';
    editableInput.style.display = 'none';
});

// Permitir que o Enter também finalize a edição
editableInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        editableInput.blur(); // Aciona o evento de 'blur'
    }
});