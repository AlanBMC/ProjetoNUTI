document.addEventListener("DOMContentLoaded", function () {

    // Inserir dados da empresa
    document.getElementById("cnpj-orgao").textContent = dadosEmpresa.cnpj;
    document.getElementById("nome-orgao").textContent = dadosEmpresa.nome;
    document.getElementById("valor-total").textContent = dadosEmpresa.valorTotal;
  
    // Inserir contratos
    const listaContratos = document.getElementById("lista-contratos");
    contratos.forEach(contrato => {
      const contratoDiv = document.createElement("div");
      contratoDiv.classList.add("contrato");
  
      contratoDiv.innerHTML = `
        <p><strong>Data de Vigência:</strong> ${contrato.dataInicio} a ${contrato.dataFim}</p>
        <p><strong>Fornecedor:</strong> ${contrato.fornecedor}</p>
        <p><strong>Objeto:</strong> ${contrato.objeto}</p>
        <p><strong>Valor:</strong> R$ ${contrato.valor}</p>
      `;
  
      listaContratos.appendChild(contratoDiv);
    });
  });
  // INICIO: DOM que temporiza a mensagem de erro e success
  document.addEventListener("DOMContentLoaded", function () {
    // Suponha que as mensagens de sucesso ou erro estejam disponíveis
    const logElements = document.querySelectorAll('.error-log, .success-log');
  
    logElements.forEach((log) => {
      // Remover o log após 3 segundos
      setTimeout(() => {
        log.classList.add('hide-log');
      }, 2000);
    });
  
  });
    // FIM: DOM que temporiza a mensagem de erro e success

// INICIO : Filtro de busca - procura dentro dos resultados -> contratos -> retornando constantes os resultados com base nas entradas do usuário
document.addEventListener("DOMContentLoaded", function () {
  // Renderizar todos os contratos inicialmente
  renderContratos(contratos);

  // Implementação da busca em tempo real
  const searchInput = document.getElementById("search-input");
  searchInput.addEventListener("input", function () {
      // Captura o termo de busca digitado pelo usuário, convertendo para letras minúsculas
      const searchTerm = searchInput.value.toLowerCase();

      // Filtra os contratos com base no termo de busca, verificando fornecedor ou objeto
      const contratosFiltrados = contratos.filter(contrato => {
          return contrato.fornecedor.toLowerCase().includes(searchTerm) ||
                 contrato.objeto.toLowerCase().includes(searchTerm);
      });

      // Renderiza os contratos filtrados com base na busca
      renderContratos(contratosFiltrados);
  });
});

// Filtro de busca alternativo, trabalhando diretamente com os elementos da página
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("search-input");
  const contratos = Array.from(document.getElementsByClassName("contrato"));

  searchInput.addEventListener("input", function () {
      // Captura o termo de busca digitado pelo usuário, convertendo para letras minúsculas
      const searchTerm = searchInput.value.toLowerCase();

      // Itera sobre os contratos para verificar se o termo de busca está presente no fornecedor ou objeto
      contratos.forEach(contrato => {
          const fornecedor = contrato.querySelector("p:nth-child(2)").textContent.toLowerCase();
          const objeto = contrato.querySelector("p:nth-child(3) .objeto-text").textContent.toLowerCase();

          // Exibe ou oculta o contrato com base no termo de busca
          if (fornecedor.includes(searchTerm) || objeto.includes(searchTerm)) {
              contrato.style.display = ""; // Mostra o contrato
          } else {
              contrato.style.display = "none"; // Oculta o contrato
          }
      });
  });
});


//INICIO: funcao para fazer um scroll na pagina quando acha os resultados, leva o usuario direto para seção de resultados.
window.onload = function() {
    const section = document.querySelector('#dados-contratos');
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
};
//FIM: funcao para fazer um scroll na pagina quando acha os resultados, leva o usuario direto para seção de resultados.
