const targetDate = new Date('2026-11-04T20:00:00-03:00').getTime();
const countdownElements = ['days', 'hours', 'minutes', 'seconds'].map(id => document.getElementById(id));

function updateCountdown() {
  const remaining = Math.max(0, targetDate - Date.now());
  const seconds = Math.floor(remaining / 1000);
  const values = [Math.floor(seconds / 86400), Math.floor(seconds / 3600) % 24, Math.floor(seconds / 60) % 60, seconds % 60];
  countdownElements.forEach((element, index) => { element.textContent = String(values[index]).padStart(2, '0'); });
}
updateCountdown();
setInterval(updateCountdown, 1000);

const modal = document.getElementById('signup-modal');
const firstInput = document.getElementById('name');
let previousFocus = null;

function openModal() {
  previousFocus = document.activeElement;
  modal.hidden = false;
  document.body.classList.add('modal-open');
  firstInput.focus();
}

function closeModal() {
  modal.hidden = true;
  document.body.classList.remove('modal-open');
  previousFocus?.focus();
}

document.querySelectorAll('[data-open-form]').forEach(button => button.addEventListener('click', openModal));
document.querySelectorAll('[data-close-form]').forEach(button => button.addEventListener('click', closeModal));
document.addEventListener('keydown', event => {
  if (modal.hidden) return;
  if (event.key === 'Escape') closeModal();
  if (event.key !== 'Tab') return;
  const focusable = [...modal.querySelectorAll('button, input')];
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
  if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
});

document.getElementById('signup-form').addEventListener('submit', event => {
  event.preventDefault();
  window.location.href = 'obrigado.html';
});
