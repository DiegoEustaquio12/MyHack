// ── NAVEGACIÓN ──
function cambiarScreen(screen) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('screen-' + screen).classList.add('active');
  document.getElementById('nav-' + screen).classList.add('active');
}

// ── FAQ ──
function toggleFaq(el) {
  el.classList.toggle('open');
}

// ELIMINAMOS abrirModal, cerrarModal y guardarCultivo de aquí