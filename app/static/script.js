// Seleccionamos ambos modales
const modalLogin = document.getElementById('modal');
const modalRegistro = document.getElementById('modal-registro');

// Funciones para Iniciar Sesión
function abrirModal() {
  modalLogin.style.display = 'flex';
}

function cerrarModal() {
  modalLogin.style.display = 'none';
}

// Funciones para Registrarse
function abrirModalRegistro() {
  modalRegistro.style.display = 'flex';
}

function cerrarModalRegistro() {
  modalRegistro.style.display = 'none';
}

// Cerrar haciendo clic afuera (aplica para ambos)
window.onclick = function(event) {
  if (event.target == modalLogin) {
    cerrarModal();
  }
  if (event.target == modalRegistro) {
    cerrarModalRegistro();
  }
}