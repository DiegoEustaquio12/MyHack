 // ============================================================
    // DATOS — reemplaza fetchDatosAPI() con tu fetch() real
    // Estructura esperada por día:
    // { fecha, temperatura, humedad, lluvia, riesgo, es_pronostico }
    // ============================================================
    async function fetchDatosAPI(cultivoId) {
      const hoy = new Date();
      const datos = [];
      const riesgosEjemplo = ['bajo','bajo','bajo','medio','medio','alto','alto','alto','medio','bajo','bajo','medio','medio','bajo'];
      for (let i = -7; i <= 6; i++) {
        const fecha = new Date(hoy);
        fecha.setDate(hoy.getDate() + i);
        datos.push({
          fecha,
          temperatura: Math.round(16 + Math.random() * 14),
          humedad:     Math.round(45 + Math.random() * 40),
          lluvia:      parseFloat((Math.random() * 10).toFixed(1)),
          riesgo:      riesgosEjemplo[i + 7],
          es_pronostico: i > 0
        });
      }
      return datos;
    }

    // ============================================================
    // CONTENIDO ACCESIBLE — semáforo, emojis, consejos
    // ============================================================
    const INFO_RIESGO = {
      bajo: {
        clase:      'verde',
        luz:        '🟢',
        estado:     'Todo bien 👍',
        frase:      'Tu cultivo está en buen estado',
        consejo_icono: '✅',
        consejos: [
          'Sigue con tu rutina normal de riego',
          'Buen momento para revisar las hojas y el suelo',
          'Aprovecha para fertilizar si ya toca',
        ]
      },
      medio: {
        clase:      'amarillo',
        luz:        '🟡',
        estado:     'Atención ⚠️',
        frase:      'Hay algo que revisar hoy',
        consejo_icono: '⚠️',
        consejos: [
          'Riega hoy por la mañana, se pronostica calor',
          'Revisa si las hojas están secas o con manchas',
          'Considera cubrir el suelo para retener humedad',
        ]
      },
      alto: {
        clase:      'rojo',
        luz:        '🔴',
        estado:     'Riesgo ALTO 🚨',
        frase:      'Tu cultivo necesita atención hoy',
        consejo_icono: '🚨',
        consejos: [
          'Riega hoy, se pronostica sequía en los próximos días',
          'Cubre las plantas si se esperan heladas esta noche',
          'Revisa el sistema de riego, la humedad está muy baja',
        ]
      }
    };

    const ICONOS_CLIMA = {
      caliente: '☀️', templado: '⛅', fresco: '🌤️', frio: '🥶',
      lluvia_alta: '🌧️', lluvia_media: '🌦️', seco: '🏜️'
    };

    function iconoTemp(t) {
      if (t >= 30) return '🌡️🔥';
      if (t >= 22) return '☀️';
      if (t >= 15) return '⛅';
      return '🥶';
    }
    function iconoHum(h) {
      if (h >= 70) return '💧💧';
      if (h >= 45) return '💧';
      return '🏜️';
    }
    function iconoLluvia(l) {
      if (l >= 6)  return '🌧️';
      if (l >= 2)  return '🌦️';
      if (l > 0)   return '🌂';
      return '☀️';
    }

    const DIAS_ES   = ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'];
    const MESES_ES  = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];

    // ============================================================
    // ESTADO
    // ============================================================
    let DATOS = [];
    let diaSeleccionado = 7; // hoy
    let tipoEvento = 'riego';

    let eventos = [
      { tipo:'riego',  titulo:'Riego mañanero', desc:'1 hora con manguera', fecha: new Date(Date.now() - 2*86400000) },
      { tipo:'nota',   titulo:'Hojas amarillas en sector B', desc:'Puede ser falta de nitrógeno', fecha: new Date(Date.now() - 4*86400000) },
    ];

    // ============================================================
    // INIT
    // ============================================================
    async function init() {
      DATOS = await fetchDatosAPI('cultivo-123');

      // fecha de hoy en topbar
      const hoy = new Date();
      document.getElementById('fecha-hoy').textContent =
        `${hoy.getDate()} de ${MESES_ES[hoy.getMonth()]} · Bitácora`;

      construirTimeline();
      seleccionarDia(7);
      renderEventos();
    }

    // ============================================================
    // SEMÁFORO + CONSEJO
    // ============================================================
    function actualizarSemaforo(d) {
      const info = INFO_RIESGO[d.riesgo];
      const sec  = document.getElementById('semaforo');
      sec.className = `semaforo-section ${info.clase}`;
      document.getElementById('semaforo-luz').textContent   = info.luz;
      document.getElementById('semaforo-estado').textContent = info.estado;
      document.getElementById('semaforo-frase').textContent  = info.frase;

      // consejo aleatorio del nivel
      const idx = Math.floor(Math.random() * info.consejos.length);
      document.getElementById('consejo-icono').textContent = info.consejo_icono;
      document.getElementById('consejo-texto').textContent = info.consejos[idx];
    }

    // ============================================================
    // DATOS DEL DÍA
    // ============================================================
    function actualizarDatos(d) {
      const esPron = d.es_pronostico;
      const grid = document.getElementById('datos-grid');
      grid.innerHTML = `
        <div class="dato-box${esPron?' pronostico':''}">
          <span class="dato-icono">${iconoTemp(d.temperatura)}</span>
          <span class="dato-val">${d.temperatura}°C</span>
          <div class="dato-lbl">Temperatura</div>
          ${esPron ? '<span class="pronostico-tag">🔮 pronóstico</span>' : ''}
        </div>
        <div class="dato-box${esPron?' pronostico':''}">
          <span class="dato-icono">${iconoHum(d.humedad)}</span>
          <span class="dato-val">${d.humedad}%</span>
          <div class="dato-lbl">Humedad</div>
          ${esPron ? '<span class="pronostico-tag">🔮 pronóstico</span>' : ''}
        </div>
        <div class="dato-box${esPron?' pronostico':''}">
          <span class="dato-icono">${iconoLluvia(d.lluvia)}</span>
          <span class="dato-val">${d.lluvia}mm</span>
          <div class="dato-lbl">Lluvia</div>
          ${esPron ? '<span class="pronostico-tag">🔮 pronóstico</span>' : ''}
        </div>
      `;
    }

    // ============================================================
    // TIMELINE
    // ============================================================
    function construirTimeline() {
      const track = document.getElementById('timeline-track');
      track.innerHTML = '';
      const iconosRiesgo = { bajo:'🟢', medio:'🟡', alto:'🔴' };

      DATOS.forEach((d, i) => {
        const pill = document.createElement('div');
        pill.className = 'day-pill' +
          (i === 7 ? ' today' : '') +
          (d.es_pronostico ? ' future' : '');
        pill.onclick = () => seleccionarDia(i);
        pill.innerHTML = `
          <span class="day-name">${DIAS_ES[d.fecha.getDay()]}</span>
          <span class="day-num">${d.fecha.getDate()}</span>
          <span class="day-icon">${d.es_pronostico ? '🔮' : iconosRiesgo[d.riesgo]}</span>
        `;
        track.appendChild(pill);
      });

      setTimeout(() => {
        const pills = track.querySelectorAll('.day-pill');
        if (pills[7]) pills[7].scrollIntoView({ inline:'center', behavior:'smooth' });
      }, 120);
    }

    function seleccionarDia(idx) {
      diaSeleccionado = idx;
      document.querySelectorAll('.day-pill').forEach((p,i) =>
        p.classList.toggle('selected', i === idx)
      );
      const d = DATOS[idx];
      actualizarSemaforo(d);
      actualizarDatos(d);
    }

    // ============================================================
    // EVENTOS
    // ============================================================
    const ICONOS_TIPO   = { riego:'💧', fertilizacion:'🌿', nota:'📝', alerta:'⚠️' };
    const BURBUJAS_TIPO = { riego:'burbuja-riego', fertilizacion:'burbuja-fertilizacion', nota:'burbuja-nota', alerta:'burbuja-alerta' };

    function renderEventos() {
      const list = document.getElementById('eventos-list');
      list.innerHTML = '';
      if (!eventos.length) {
        list.innerHTML = `
          <div style="text-align:center;padding:28px 20px;color:var(--gris);">
            <div style="font-size:40px;margin-bottom:10px;">📋</div>
            <div style="font-size:14px;font-weight:500;">Aún no hay nada anotado.<br>¡Registra tu primer evento!</div>
          </div>`;
        return;
      }
      [...eventos].reverse().forEach(ev => {
        const el = document.createElement('div');
        el.className = 'evento-item';
        const fechaStr = `${ev.fecha.getDate()} de ${MESES_ES[ev.fecha.getMonth()]}`;
        el.innerHTML = `
          <div class="evento-burbuja ${BURBUJAS_TIPO[ev.tipo]}">${ICONOS_TIPO[ev.tipo]}</div>
          <div class="evento-body">
            <div class="evento-titulo">${ev.titulo}</div>
            ${ev.desc ? `<div class="evento-desc">${ev.desc}</div>` : ''}
            <div class="evento-fecha">📅 ${fechaStr}</div>
          </div>
        `;
        list.appendChild(el);
      });
    }

    // ============================================================
    // MODAL
    // ============================================================
    function abrirModal()  { document.getElementById('modal').classList.add('open'); }
    function cerrarModal() { document.getElementById('modal').classList.remove('open'); }
    function cerrarFuera(e){ if (e.target === document.getElementById('modal')) cerrarModal(); }

    function selTipo(btn) {
      document.querySelectorAll('.tipo-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      tipoEvento = btn.dataset.tipo;
    }

    function guardarEvento() {
      const titulo = document.getElementById('evt-titulo').value.trim();
      const desc   = document.getElementById('evt-desc').value.trim();
      if (!titulo) { alert('Escribe qué pasó'); return; }

      eventos.push({ tipo: tipoEvento, titulo, desc, fecha: new Date() });

      document.getElementById('evt-titulo').value = '';
      document.getElementById('evt-desc').value   = '';
      cerrarModal();
      renderEventos();

      /*
        CONECTAR A API:
        await fetch(`/api/cultivos/${cultivoId}/eventos`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ tipo: tipoEvento, titulo, desc, fecha: new Date() })
        });
      */
    }

    init();

    // ── CALENDARIO DE RIEGOS ─────────────────────────────────────

let calOffset = 0   // 0 = mes actual, -1 = mes anterior, etc.

/**
 * Extrae del localStorage todos los días en que hubo un riego.
 * Devuelve un Set de strings con formato 'YYYY-MM-DD'.
 */
function obtenerDiasRegados() {
  const eventos = JSON.parse(localStorage.getItem('eventos') || '[]')
  const diasRegados = new Set()

  eventos.forEach(evt => {
    // Solo registros de tipo riego
    if (evt.tipo === 'riego' && evt.fecha) {
      // Normalizar: guardar solo la parte YYYY-MM-DD
      const fecha = evt.fecha.split('T')[0]
      diasRegados.add(fecha)
    }
  })

  return diasRegados
}

/**
 * Construye y renderiza el calendario del mes indicado por calOffset.
 * calOffset = 0 → mes actual, -1 → mes anterior, etc.
 */
function renderCalendario() {
  const hoy      = new Date()
  const objetivo = new Date(hoy.getFullYear(), hoy.getMonth() + calOffset, 1)
  const anio     = objetivo.getFullYear()
  const mes      = objetivo.getMonth()   // 0–11

  // Etiqueta del mes
  const label = objetivo.toLocaleDateString('es-MX', { month: 'long', year: 'numeric' })
  document.getElementById('cal-mes-label').textContent = label

  // Ocultar botón "siguiente" si ya estamos en el mes actual
  const btnNext = document.getElementById('cal-next')
  btnNext.classList.toggle('oculto', calOffset >= 0)

  // Días regados
  const diasRegados = obtenerDiasRegados()

  // Día de la semana en que empieza el mes (0=Dom…6=Sáb → ajustar a Lun=0)
  let primerDia = new Date(anio, mes, 1).getDay()
  primerDia = (primerDia + 6) % 7   // convierte Dom=0 a Dom=6

  // Días totales del mes
  const totalDias = new Date(anio, mes + 1, 0).getDate()

  const grid = document.getElementById('cal-grid')
  grid.innerHTML = ''

  // Celdas vacías iniciales
  for (let i = 0; i < primerDia; i++) {
    const vacio = document.createElement('div')
    vacio.className = 'cal-dia vacio'
    grid.appendChild(vacio)
  }

  // Celdas de días
  for (let d = 1; d <= totalDias; d++) {
    const celda  = document.createElement('div')
    const fechaStr = `${anio}-${String(mes + 1).padStart(2,'0')}-${String(d).padStart(2,'0')}`
    const esteD  = new Date(anio, mes, d)
    const esHoy  = (
      d === hoy.getDate() &&
      mes === hoy.getMonth() &&
      anio === hoy.getFullYear()
    )
    const esFuturo = esteD > hoy && !esHoy
    const esRegado = diasRegados.has(fechaStr)

    let clases = 'cal-dia'
    if (esFuturo)      clases += ' futuro'
    else if (esHoy)    clases += esRegado ? ' hoy regado' : ' hoy'
    else if (esRegado) clases += ' regado'
    else               clases += ' normal'

    celda.className = clases
    celda.textContent = d

    // Tooltip accesible en móvil
    if (esRegado && !esFuturo) {
      celda.title = `Riego registrado el ${fechaStr}`
    }

    grid.appendChild(celda)
  }
}

/** Navegar entre meses */
function calMover(delta) {
  calOffset = Math.min(0, calOffset + delta)   // no avanzar más allá del mes actual
  renderCalendario()
}

// ── Integración con guardarEvento() ─────────────────────────
// Si ya tienes esta función, solo agrega renderCalendario()
// al final de ella. Si no la tienes, aquí está la versión completa:

function guardarEvento() {
  const titulo = document.getElementById('evt-titulo').value.trim()
  if (!titulo) return

  const tipo = document.querySelector('.tipo-btn.selected')?.dataset.tipo || 'nota'
  const desc = document.getElementById('evt-desc').value.trim()
  const ahora = new Date().toISOString()

  const evento = {
    id:     Date.now(),
    tipo,
    titulo,
    desc,
    fecha:  ahora,          // ← la fecha ISO se usa para el calendario
  }

  const lista = JSON.parse(localStorage.getItem('eventos') || '[]')
  lista.unshift(evento)
  localStorage.setItem('eventos', JSON.stringify(lista))

  cerrarModal()
  cargarEventos()          // refresca la lista de eventos
  renderCalendario()       // ← actualiza el calendario automáticamente
}

// ── Inicialización ───────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // ... tu código de init existente ...
  renderCalendario()   // ← agregar esta línea al init
})