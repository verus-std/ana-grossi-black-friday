const whatsappGroupUrl = 'https://chat.whatsapp.com/Itsinsh80ULEvTaYAughkx?s=cl&p=a&mlu=4&ilr=4';
const redirectCountdown = document.querySelector('[data-redirect-countdown]');

function goToWhatsApp() {
  window.location.assign(whatsappGroupUrl);
}

document.querySelectorAll('[data-whatsapp-group]').forEach(button => {
  button.addEventListener('click', goToWhatsApp);
});

let remaining = 5;
const redirectTimer = setInterval(() => {
  remaining -= 1;
  if (redirectCountdown) redirectCountdown.textContent = String(Math.max(remaining, 0));
  if (remaining > 0) return;
  clearInterval(redirectTimer);
  goToWhatsApp();
}, 1000);
