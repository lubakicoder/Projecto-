const adminCard = document.getElementById('admin-card');
        const adminIdContainer = document.getElementById('admin-id-container');
        const verifyBtn = document.getElementById('verify-btn');
        const adminResponse = document.getElementById('admin-response');

        const formContainer = document.getElementById('form-container');
        const submitBtn = document.getElementById('submit-btn');
        const response = document.getElementById('response');

        // Simulação de nave ID (exemplo: o código esperado)
        const validAdminID = "12345";

        // Ao clicar no card do admin, exibe o campo de nave ID
        adminCard.addEventListener('click', () => {
            adminIdContainer.style.display = 'flex';
        });

        // Verifica a Nave ID ao clicar no botão
        verifyBtn.addEventListener('click', () => {
            const adminId = document.getElementById('admin-id').value;
            if (adminId === validAdminID) {
                // Se a ID for válida, mostra o formulário de cadastro
                adminIdContainer.style.display = 'none';
                formContainer.style.display = 'flex';
            } else {
                adminResponse.textContent = 'ID inválida. Tente novamente.';
                adminResponse.style.color = 'red';
            }
        });

        // Simulação do envio do cadastro do aluno
        submitBtn.addEventListener('click', () => {
            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;
            const curso = document.getElementById('curso').value;

            if (nome && email && curso) {
                response.textContent = 'Aluno cadastrado com sucesso!';
                response.style.color = 'green';
                formContainer.reset();
            } else {
                response.textContent = 'Por favor, preencha todos os campos.';
                response.style.color = 'red';
            }
        });