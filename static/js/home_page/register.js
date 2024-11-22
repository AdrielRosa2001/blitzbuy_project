// METHODS:
function set_invalid_inputs(message){
    // const email_input = GbID('email_input');
    // const password_input = GbID('password_input');
    // validationLoginFeedback.innerHTML = '';
    // email_input.classList.remove('is-invalid');
    // password_input.classList.remove('is-invalid');
    // email_input.classList.add('is-invalid');
    // password_input.classList.add('is-invalid');
    const validationLoginFeedback = GbID('feedback-register');
    validationLoginFeedback.innerHTML = message;
};

function redirect_on_click(url){
    window.location.href = url;
};
const realizarCadastro = async (data) => {
    console.log(data);
    const response = await fetch(`/make_register_default/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": data.csrfmiddlewaretoken,
        },
        body: JSON.stringify(data)
    });
    const html = await response.text();
    if (response.status == 200){
        Qs(".register-form").reset();
        show_modal();
    } else {
        set_invalid_inputs(html);
    };
};

// EVENTS:

Qs(".register-form").addEventListener('submit', (e) => {
    // Preparando dicionário com os dados do forms
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
  
    // Chamando função para criar os dados
    realizarCadastro(data);
});

function set_default_inputs(id_element){
    GbID(id_element).classList.remove('is-invalid');
    GbID('feedback-register').innerHTML = "";
};

GbID("username_input").addEventListener('focus', (e) => {
    set_default_inputs("username_input");
});

GbID("email_input").addEventListener('focus', (e) => {
    set_default_inputs("email_input");
});




