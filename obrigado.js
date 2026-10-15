// Insira aqui o convite oficial quando o grupo estiver disponível.
const whatsappGroupUrl = 'https://chat.whatsapp.com/Itsinsh80ULEvTaYAughkx?s=cl&p=a&mlu=4&ilr=4';
const groupDialog = document.getElementById('group-dialog');

document.querySelectorAll('[data-whatsapp-group]').forEach(button => {
  button.addEventListener('click', () => {
    if (whatsappGroupUrl) {
      window.location.assign(whatsappGroupUrl);
      return;
    }
    groupDialog.showModal();
  });
});
