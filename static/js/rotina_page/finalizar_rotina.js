// Metods:

const finalizarRotina = async (data) => {
    console.log(data);
    const response = await fetch(`/app/${data['rotina_id']}/finalizar_rotina`);
    const html = await response.text();
    if (response.status == 200){
      // createNewToast("Lista finalizada com sucesso!", emoji_success);
      redirect_main();
    } else {
    };
    Qs(".form-add-produto").reset();
};
  

// EVENTS:

Qs(".form-finalizar-rotina").addEventListener('submit', (e) => {
    // Preparando dicionário com os dados do forms
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
  
    // Chamando função para criar os dados
    finalizarRotina(data);
});
