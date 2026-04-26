// static/bita.js
// CULTIVO_ID y STORAGE_KEY vienen inyectados por Flask en el HTML

let calOffset = 0
let datosActuales = null

// ── INICIALIZACIÓN ────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  mostrarFecha()
  cargarDatos()
  cargarEventos()
  renderCalendario()

  // Actualización automática cada 30 minutos
  setInterval(cargarDatos, 30 * 60 * 1000)
})

// ── FECHA EN TOPBAR ───────────────────────────────────────────
function mostrarFecha() {
  const hoy = new Date()
  document.getElementById('fecha-hoy').textContent =
    hoy.toLocaleDateString('es-MX', {
      weekday: 'long', day: 'numeric', month: 'long'
    })
}

// ── CARGAR DATOS DESDE FLASK + Open-Meteo ────────────────────
async function cargarDatos() {
  const btn = document.getElementById('btn-refresh')
  if (btn) btn.style.opacity = '0.4'

  // Intentar obtener coordenadas del dispositivo
  let lat = 19.04, lon = -98.20
  try {
    const pos = await obtenerGPS()
    lat = pos.coords.latitude
    lon = pos.coords.longitude
  } catch (_) {
    // Sin GPS: usa coordenadas por defecto de Puebla
  }

  try {
    const res  = await fetch(`/api/bitacora/${CULTIVO_ID}?lat=${lat}&lon=${lon}`)
    const data = await res.json()

    if (data.error) {
      mostrarError(data.error)
      return
    }

    datosActuales = data
    actualizarUI(data)

  } catch (e) {
    mostrarError('Sin conexión. Los datos pueden estar desactualizados.')
  } finally {
    if (btn) btn.style.opacity = '1'
  }
}

function obtenerGPS() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) return reject('Sin soporte GPS')
    navigator.geolocation.getCurrentPosition(resolve, reject, {
      timeout: 5000,
      maximumAge: 300000   // cache 5 min
    })
  })
}

// ── ACTUALIZAR TODA LA UI ─────────────────────────────────────
function actualizarUI(data) {
  // Nombre del cultivo en topbar
  document.getElementById('nombre-cultivo').textContent =
    data.cultivo.nombre

  // Semáforo
  actualizarSemaforo(data.nivel_riesgo, data.urgencia)

  // Cards de clima
  document.getElementById('val-temp').textContent =
    data.clima_actual.temp.toFixed(1) + '°C'
  document.getElementById('val-humedad').textContent =
    data.clima_actual.humedad.toFixed(0) + '%'
  document.getElementById('val-lluvia').textContent =
    data.clima_actual.lluvia.toFixed(1) + ' mm'
  document.getElementById('val-etapa').textContent =
    data.cultivo.etapa.etapa

  // Diagnóstico
  const consejo = document.getElementById('consejo-box')
  document.getElementById('consejo-texto').textContent = data.diagnostico
  consejo.style.display = 'flex'

  // Soluciones
  renderSoluciones(data.soluciones)

  // Pronóstico 7 días
  renderTimeline(data.pronostico_7d)
}

// ── SEMÁFORO ──────────────────────────────────────────────────
function actualizarSemaforo(nivel, urgencia) {
  const sem    = document.getElementById('semaforo')
  const luz    = document.getElementById('semaforo-luz')
  const estado = document.getElementById('semaforo-estado')
  const frase  = document.getElementById('semaforo-frase')

  const config = {
    Alto:  { clase: 'rojo',     emoji: '🔴', texto: 'Riesgo ALTO' },
    Medio: { clase: 'amarillo', emoji: '🟡', texto: 'Riesgo MEDIO' },
    Bajo:  { clase: 'verde',    emoji: '🟢', texto: 'Todo en orden' },
  }
  const c = config[nivel] || config['Bajo']

  sem.className    = `semaforo-section ${c.clase}`
  luz.textContent  = c.emoji
  estado.textContent = c.texto
  frase.textContent  = urgencia
}

// ── SOLUCIONES ────────────────────────────────────────────────
function renderSoluciones(soluciones) {
  const sec  = document.getElementById('soluciones-section')
  const lista = document.getElementById('soluciones-list')

  if (!soluciones || soluciones.length === 0) {
    sec.style.display = 'none'
    return
  }

  sec.style.display = 'block'
  lista.innerHTML = soluciones.map(s => `
    <div class="solucion-card urgencia-${s.urgencia.toLowerCase()}">
      <div class="solucion-header">
        <span class="solucion-evento">${s.evento}</span>
        <span class="solucion-badge">${s.urgencia}</span>
      </div>
      <p class="solucion-diagnostico">${s.diagnostico}</p>
      <ul class="solucion-acciones">
        ${s.acciones.map(a => `<li>${a}</li>`).join('')}
      </ul>
      <p class="solucion-ref">📚 ${s.referencia}</p>
    </div>
  `).join('')
}

// ── TIMELINE 7 DÍAS ───────────────────────────────────────────
function renderTimeline(pronostico) {
  const track = document.getElementById('timeline-track')
  if (!pronostico || pronostico.length === 0) return

  const dias = ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb']

  track.innerHTML = pronostico.map((dia, i) => {
    const fecha  = new Date(dia.fecha + 'T12:00:00')
    const nombre = i === 0 ? 'Hoy' : dias[fecha.getDay()]
    const lluvia = dia.lluvia > 0
      ? `<div class="tl-lluvia">🌧 ${dia.lluvia.toFixed(0)}mm</div>`
      : ''
    return `
      <div class="timeline-dia ${i === 0 ? 'hoy' : ''}">
        <div class="tl-nombre">${nombre}</div>
        <div class="tl-temps">
          <span class="tl-max">${dia.temp_max.toFixed(0)}°</span>
          <span class="tl-min">${dia.temp_min.toFixed(0)}°</span>
        </div>
        ${lluvia}
      </div>
    `
  }).join('')
}

// ── EVENTOS (localStorage por cultivo) ───────────────────────
function cargarEventos() {
  const lista  = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  const el     = document.getElementById('eventos-list')

  if (lista.length === 0) {
    el.innerHTML = '<div class="eventos-vacio">Aún no has registrado nada. ¡Anota tu primera actividad!</div>'
    return
  }

  const iconos = {
    riego: '💧', fertilizacion: '🌿', nota: '📝', alerta: '⚠️'
  }

  el.innerHTML = lista.slice(0, 20).map(evt => {
    const fecha = new Date(evt.fecha)
    const hace  = tiempoRelativo(fecha)
    return `
      <div class="evento-item tipo-${evt.tipo}">
        <div class="evento-icono">${iconos[evt.tipo] || '📝'}</div>
        <div class="evento-cuerpo">
          <div class="evento-titulo">${evt.titulo}</div>
          ${evt.desc ? `<div class="evento-desc">${evt.desc}</div>` : ''}
          <div class="evento-fecha">${hace}</div>
        </div>
      </div>
    `
  }).join('')
}

function tiempoRelativo(fecha) {
  const diff = Math.floor((Date.now() - fecha.getTime()) / 1000)
  if (diff < 60)   return 'Hace un momento'
  if (diff < 3600) return `Hace ${Math.floor(diff/60)} min`
  if (diff < 86400) return `Hace ${Math.floor(diff/3600)} h`
  return fecha.toLocaleDateString('es-MX', { day:'numeric', month:'short' })
}

// ── GUARDAR EVENTO ────────────────────────────────────────────
function guardarEvento() {
  const titulo = document.getElementById('evt-titulo').value.trim()
  if (!titulo) return

  const tipo  = document.querySelector('.tipo-btn.selected')?.dataset.tipo || 'nota'
  const desc  = document.getElementById('evt-desc').value.trim()

  const evento = {
    id:    Date.now(),
    tipo,
    titulo,
    desc,
    fecha: new Date().toISOString(),
  }

  const lista = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  lista.unshift(evento)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(lista))

  cerrarModal()
  cargarEventos()
  renderCalendario()   // actualiza el calendario si fue un riego
}

// ── MODAL ─────────────────────────────────────────────────────
function abrirModal() {
  document.getElementById('modal').classList.add('open')
  document.getElementById('evt-titulo').value = ''
  document.getElementById('evt-desc').value   = ''
}
function cerrarModal() {
  document.getElementById('modal').classList.remove('open')
}
function cerrarFuera(e) {
  if (e.target.id === 'modal') cerrarModal()
}
function selTipo(btn) {
  document.querySelectorAll('.tipo-btn').forEach(b => b.classList.remove('selected'))
  btn.classList.add('selected')
}

// ── CALENDARIO DE RIEGOS ──────────────────────────────────────
function obtenerDiasRegados() {
  const lista = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  const dias  = new Set()
  lista.forEach(evt => {
    if (evt.tipo === 'riego' && evt.fecha) {
      dias.add(evt.fecha.split('T')[0])
    }
  })
  return dias
}

function renderCalendario() {
  const hoy      = new Date()
  const objetivo = new Date(hoy.getFullYear(), hoy.getMonth() + calOffset, 1)
  const anio     = objetivo.getFullYear()
  const mes      = objetivo.getMonth()

  document.getElementById('cal-mes-label').textContent =
    objetivo.toLocaleDateString('es-MX', { month: 'long', year: 'numeric' })

  document.getElementById('cal-next')
    .classList.toggle('oculto', calOffset >= 0)

  const diasRegados = obtenerDiasRegados()

  let primerDia = new Date(anio, mes, 1).getDay()
  primerDia = (primerDia + 6) % 7

  const totalDias = new Date(anio, mes + 1, 0).getDate()
  const grid = document.getElementById('cal-grid')
  grid.innerHTML = ''

  for (let i = 0; i < primerDia; i++) {
    const v = document.createElement('div')
    v.className = 'cal-dia vacio'
    grid.appendChild(v)
  }

  for (let d = 1; d <= totalDias; d++) {
    const celda    = document.createElement('div')
    const fechaStr = `${anio}-${String(mes+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`
    const esteD    = new Date(anio, mes, d)
    const esHoy    = d === hoy.getDate() && mes === hoy.getMonth() && anio === hoy.getFullYear()
    const esFuturo = esteD > hoy && !esHoy
    const esRegado = diasRegados.has(fechaStr)

    let cls = 'cal-dia'
    if (esFuturo)       cls += ' futuro'
    else if (esHoy)     cls += esRegado ? ' hoy regado' : ' hoy'
    else if (esRegado)  cls += ' regado'
    else                cls += ' normal'

    celda.className   = cls
    celda.textContent = d
    grid.appendChild(celda)
  }
}

function calMover(delta) {
  calOffset = Math.min(0, calOffset + delta)
  renderCalendario()
}

// ── ERROR ─────────────────────────────────────────────────────
function mostrarError(msg) {
  const sem = document.getElementById('semaforo')
  sem.className = 'semaforo-section gris'
  document.getElementById('semaforo-luz').textContent    = '⚠️'
  document.getElementById('semaforo-estado').textContent = 'Sin datos'
  document.getElementById('semaforo-frase').textContent  = msg
}