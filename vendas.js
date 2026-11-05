// Link do checkout (Hotmart). Se ficar vazio, os botões levam até o bloco de preço.
const checkoutUrl = 'https://pay.hotmart.com/W108101263E?off=xq0rmqiq';

// Fim da oferta (horário de Brasília). Ajustar quando a data for definida.
const offerEnd = new Date('2026-11-30T23:59:59-03:00').getTime();

const units = ['days', 'hours', 'minutes', 'seconds'];

function updateCountdown() {
  const total = Math.floor(Math.max(0, offerEnd - Date.now()) / 1000);
  const values = {
    days: Math.floor(total / 86400),
    hours: Math.floor(total / 3600) % 24,
    minutes: Math.floor(total / 60) % 60,
    seconds: total % 60,
  };
  units.forEach(unit => {
    document.querySelectorAll(`[data-unit="${unit}"]`).forEach(el => {
      el.textContent = String(values[unit]).padStart(2, '0');
    });
  });
}
updateCountdown();
setInterval(updateCountdown, 1000);

document.querySelectorAll('[data-checkout]').forEach(link => {
  if (checkoutUrl) {
    link.href = checkoutUrl;
    return;
  }
  link.addEventListener('click', event => {
    event.preventDefault();
    document.getElementById('oferta').scrollIntoView({ behavior: 'smooth' });
  });
});
