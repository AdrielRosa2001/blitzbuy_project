// console.log('main_load');
// const toastTrigger = document.getElementById('adicionarProdutoBtn');
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


// ------------------------------ METODOS:

const setListaRotinas = (statusId) => {
    QsAll('.status-btn-selector').forEach((el) => el.classList.remove('active'));
    QsAll('.status-btn-selector').forEach((el) => el.classList.remove('fw-semibold'));
    QsAll('.status-btn-selector').forEach((el) => el.classList.remove('text-primary'));
    Qs(`#status-btn-selector-${statusId}`).classList.add("active");
    Qs(`#status-btn-selector-${statusId}`).classList.add("fw-semibold");
    Qs(`#status-btn-selector-${statusId}`).classList.add("text-primary");
    
    QsAll('.display-rotinas-list').forEach((el) => el.classList.remove('d-none'));
    QsAll('.display-rotinas-list').forEach((el) => el.classList.add('d-none'));
    Qs(`#status-rotina-id-${statusId}`).classList.remove("d-none");
};


const criarRotinaBack = async (data) => {
    // console.log(data);
    const response = await fetch(`/app/criar_nova_rotina/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": data.csrfmiddlewaretoken,
        },
        body: JSON.stringify(data)
    });
    const html = await response.text();
    const $nenhumaRotinaDiv = Qs(".nenhuma-rotina");
    const $displayDeRotinasContainer = Qs(".rotinas-display");
    if (response.status == 200){
        $nenhumaRotinaDiv.remove();
        $displayDeRotinasContainer.insertAdjacentHTML('beforeend', html);
        Qs(".form-criar-rotina").reset();
        createNewToast("Lista de compras criada com sucesso!", emoji_success);
    } else {
        createNewToast("Houve um erro ao tentar criar a lista de compras!", emoji_failed);
    }

};

// -------------------------------------------------- EVENTS:
// Criar Rotina
Qs(".form-criar-rotina").addEventListener('submit', (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    criarRotinaBack(data);
});
