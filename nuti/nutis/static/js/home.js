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
  document.addEventListener("DOMContentLoaded", function () {
    // Suponha que as mensagens de sucesso ou erro estejam disponíveis
    const logElements = document.querySelectorAll('.error-log, .success-log');
  
    logElements.forEach((log) => {
      // Remover o log após 3 segundos
      setTimeout(() => {
        log.classList.add('hide-log');
      }, 2000);
    });
  
    // Insira aqui o código para preencher as informações de CNPJ, nome e contratos
  });
  document.addEventListener("DOMContentLoaded", function () {
 
    // Renderizar todos os contratos inicialmente
    renderContratos(contratos);

    // Implementação da busca em tempo real
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("input", function () {
        const searchTerm = searchInput.value.toLowerCase();
        const contratosFiltrados = contratos.filter(contrato => {
            return contrato.fornecedor.toLowerCase().includes(searchTerm) ||
                   contrato.objeto.toLowerCase().includes(searchTerm);
        });
        renderContratos(contratosFiltrados);
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const contratos = Array.from(document.getElementsByClassName("contrato"));

    searchInput.addEventListener("input", function () {
        const searchTerm = searchInput.value.toLowerCase();

        contratos.forEach(contrato => {
            const fornecedor = contrato.querySelector("p:nth-child(2)").textContent.toLowerCase();
            const objeto = contrato.querySelector("p:nth-child(3) .objeto-text").textContent.toLowerCase();

            if (fornecedor.includes(searchTerm) || objeto.includes(searchTerm)) {
                contrato.style.display = "";
            } else {
                contrato.style.display = "none";
            }
        });
    });
});
window.onload = function() {
    const section = document.querySelector('#dados-contratos');
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
};
