// Telefone Estilo
const celularInput = document.getElementById('celular');

celularInput.addEventListener('input', function(e) {
  let val = this.value;

  // Remove tudo que não for número
  val = val.replace(/\D/g, '');

  // Formata com parênteses no DDD e espaço
  if(val.length > 2){
    val = `(${val.slice(0,2)}) ${val.slice(2,11)}`;
  } else if(val.length > 0){
    val = `(${val}`;
  }

  this.value = val;
});


// Validar o campo de tamanho para aceitar apenas números
const tamanhoInput = document.getElementById('tamanho');

tamanhoInput.addEventListener('input', () => {
  tamanhoInput.value = tamanhoInput.value.replace(/[^0-9]/g, '');
});