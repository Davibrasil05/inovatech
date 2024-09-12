function createNode(element) {
    return document.createElement(element);
  }
  
  function append(parent, el) {
  return parent.appendChild(el);
  }

  const tabelGeral = document.querySelector('#tbd');

document.getElementById('fetchData').addEventListener('click',()=>{
    fetch('http://localhost:3000/data')
    .then(response => response.json())
    .then(data =>{
     let vagas = data;
      vagas.map(vaga=>{
        let tr = createNode("tr")
         
        tr.innerHTML = `
        <td>${vaga.id}</td>
         <td>${vaga.spot_number}</td>
         <td>${vaga.status}</td>
        
        `
        append(tabelGeral, tr)

      })


    })
    .catch(error => console.error('Error',error));
});