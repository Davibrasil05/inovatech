function createNode(element) {
  return document.createElement(element);
}

function append(parent, el) {
  return parent.appendChild(el);
}

const tabelGeral = document.querySelector('#tbd');

document.getElementById('fetchData').addEventListener('click', () => {
  fetch('http://localhost:3001/data')
      .then(response => response.json())
      .then(data => {
          // Limpa a tabela existente
          tabelGeral.innerHTML = '';

          data.forEach(vaga => {
              // Cria uma nova linha na tabela
              let tr = createNode("tr");

              // Cria a célula do bloco visual
              let visualCell = createNode("td");
              let block = createNode("div");
              block.classList.add("vaga");
              if (vaga.status.toLowerCase() === "livre") {
                  block.classList.add("verde");
              } else if (vaga.status.toLowerCase() === "ocupada") {
                  block.classList.add("vermelho");
              }
              append(visualCell, block);

              // Preenche as outras células da linha
              tr.innerHTML = `
                  <td>${vaga.id}</td>
                  <td>${vaga.spot_number}</td>
                  <td>${vaga.status}</td>
              `;
              append(tr, visualCell); // Adiciona a célula com o bloco
              append(tabelGeral, tr); // Adiciona a linha à tabela
          });
      })
      .catch(error => console.error('Erro ao buscar os dados:', error));
});
