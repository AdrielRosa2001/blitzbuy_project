// METHODS:
function set_invalid_inputs(message){
    const email_input = GbID('email_input');
    const password_input = GbID('password_input');
    const validationLoginFeedback = GbID('feedback-login');
    validationLoginFeedback.innerHTML = '';
    email_input.classList.remove('is-invalid');
    password_input.classList.remove('is-invalid');
    email_input.classList.add('is-invalid');
    password_input.classList.add('is-invalid');
    validationLoginFeedback.innerHTML = message;
};

function redirect_on_click(url){
    window.location.href = url;
};
const realizarLogin = async (data) => {
    // console.log(data);
    const response = await fetch(`/make_login_default/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": data.csrfmiddlewaretoken,
        },
        body: JSON.stringify(data)
    });
    const html = await response.text();
    if (response.status == 200){
        Qs(".login-form").reset();
        redirect_to_app();
    } else {
        set_invalid_inputs('Usuário ou senha inválido!');
    };
};

// EVENTS:

Qs(".login-form").addEventListener('submit', (e) => {
    // Preparando dicionário com os dados do forms
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
  
    // Chamando função para criar os dados
    realizarLogin(data);
});

function set_default_inputs(){
    GbID('email_input').classList.remove('is-invalid');
    GbID("password_input").classList.remove('is-invalid');
    GbID('feedback-login').innerHTML = "";
};

GbID("email_input").addEventListener('focus', (e) => {
    set_default_inputs()
});

GbID("password_input").addEventListener('focus', (e) => {
    set_default_inputs()
});


