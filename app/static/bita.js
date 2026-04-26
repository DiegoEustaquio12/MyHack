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