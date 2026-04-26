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

function login() {
    const usuario = document.getElementById("usuario").value;
    const contrasena = document.getElementById("contrasena").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            usuario: usuario,
            contrasena: contrasena
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.ok) {
            window.location.href = data.redirect;
        } else {
            alert(data.error);
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error en la conexión");
    });
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

