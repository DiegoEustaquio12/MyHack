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

function registrar() {
    // 1. Obtener los valores de los campos
    const nombre = document.getElementById('reg-nombre').value;
    const usuario = document.getElementById('reg-usuario').value;
    const contrasena = document.getElementById('reg-contrasena').value;

    // 2. Validar que no estén vacíos
    if (!nombre || !usuario || !contrasena) {
        alert("Por favor, llena todos los campos para registrarte.");
        return;
    }

    // 3. Enviar los datos al backend de Flask
    fetch('/registrar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nombre: nombre,
            usuario: usuario,
            contrasena: contrasena
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            alert("¡Registro exitoso! Ahora puedes iniciar sesión.");
            cerrarModalRegistro(); // Oculta el modal de registro
            abrirModal();          // Muestra el modal de login
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error('Error en el registro:', error));
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

