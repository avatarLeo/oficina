document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contactForm');

    contactForm.addEventListener('submit', function(event) {
        // Previne o recarregamento da página
        event.preventDefault();

        // Captura os dados (apenas para demonstração)
        const nome = document.getElementById('nome').value;
        
        // Simula o envio
        alert(`Obrigado, ${nome}! Sua mensagem foi recebida pela Metalúrgica Itaparica. Entraremos em contato em breve.`);
        
        // Limpa o formulário
        contactForm.reset();
    });
});