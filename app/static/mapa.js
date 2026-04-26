/* ============================================================
   PEGA ESTO justo ANTES de:
   <script src="../static/menu.js"></script>
   ============================================================ */

// ── Variables del mapa ──
let mapaLeaflet    = null;
let marcador       = null;
let coordsActuales = { lat: null, lon: null, lugar: null };

// ── Icono verde reutilizable ──
function crearIcono() {
  return L.divIcon({
    className: '',
    html: `<div style="
      width:28px;height:28px;
      background:#2D6A4F;
      border-radius:50% 50% 50% 0;
      transform:rotate(-45deg);
      border:3px solid white;
      box-shadow:0 2px 8px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 28]
  });
}

// ── Inicializar Leaflet (solo la primera vez) ──
function iniciarMapa() {
  if (mapaLeaflet) {
    setTimeout(() => mapaLeaflet.invalidateSize(), 150);
    return;
  }

  mapaLeaflet = L.map('mapa-leaflet', {
    center: [18.9242, -98.4195], // Puebla
    zoom: 9,
    zoomControl: true
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap',
    maxZoom: 18
  }).addTo(mapaLeaflet);

  // Clic en mapa → marcador + geocodificación inversa
  mapaLeaflet.on('click', async (e) => {
    ponerMarcador(e.latlng.lat, e.latlng.lng);
    document.getElementById('mapa-hint').style.opacity = '0';
    await geocodificacionInversa(e.latlng.lat, e.latlng.lng);
  });

  setTimeout(() => mapaLeaflet.invalidateSize(), 200);
}

// ── Poner o mover marcador ──
function ponerMarcador(lat, lng) {
  if (marcador) {
    marcador.setLatLng([lat, lng]);
  } else {
    marcador = L.marker([lat, lng], {
      icon: crearIcono(),
      draggable: true
    }).addTo(mapaLeaflet);

    marcador.on('dragend', async (ev) => {
      const p = ev.target.getLatLng();
      await geocodificacionInversa(p.lat, p.lng);
    });
  }
}

// ── Buscar municipio → Open-Meteo Geocoding (gratis, sin API key) ──
async function buscarUbicacion() {
  const texto = document.getElementById('municipio').value.trim();
  if (!texto) return;

  const btn = document.getElementById('mapa-btn');
  btn.textContent = '⏳';
  btn.disabled = true;

  try {
    const url = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(texto + ', Puebla, México')}&count=1&language=es&format=json`;
    const res  = await fetch(url);
    const data = await res.json();

    if (data.results && data.results.length > 0) {
      const r      = data.results[0];
      const nombre = r.name + (r.admin1 ? ', ' + r.admin1 : '');
      mapaLeaflet.setView([r.latitude, r.longitude], 13);
      ponerMarcador(r.latitude, r.longitude);
      document.getElementById('mapa-hint').style.opacity = '0';
      mostrarCoordenadas(r.latitude, r.longitude, nombre);
    } else {
      alert('No encontré ese municipio. Prueba con: "Tehuacán, Puebla"');
    }
  } catch (e) {
    alert('Error de conexión al buscar.');
    console.error(e);
  } finally {
    btn.textContent = '🔍';
    btn.disabled = false;
  }
}

// ── Geocodificación inversa: coords → nombre (Nominatim) ──
async function geocodificacionInversa(lat, lon) {
  try {
    const url  = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&accept-language=es`;
    const res  = await fetch(url, { headers: { 'Accept-Language': 'es' } });
    const data = await res.json();
    const a    = data.address || {};
    const nombre = a.village || a.town || a.city || a.municipality || a.county || 'Ubicación seleccionada';
    mostrarCoordenadas(lat, lon, nombre + (a.state ? ', ' + a.state : ''));
  } catch (e) {
    mostrarCoordenadas(lat, lon, 'Ubicación seleccionada');
  }
}

// ── Mostrar coordenadas en el UI ──
function mostrarCoordenadas(lat, lon, lugar) {
  coordsActuales = { lat, lon, lugar };
  document.getElementById('coord-lat').textContent   = lat.toFixed(4) + '°';
  document.getElementById('coord-lon').textContent   = lon.toFixed(4) + '°';
  document.getElementById('coord-lugar').textContent = lugar;
  document.getElementById('coords-row').style.display = 'grid';
}

// ── Abrir modal ──
function abrirModal() {
  document.getElementById('modal').classList.add('open');
  setTimeout(iniciarMapa, 150);
}

// ── Cerrar modal ──
function cerrarModal() {
  document.getElementById('modal').classList.remove('open');
}

function cerrarModalFuera(e) {
  if (e.target === document.getElementById('modal')) cerrarModal();
}

// ── Iconos por tipo de cultivo ──
const _iconosCultivo = {
  maiz:'🌽', chile:'🌶️', frijol:'🫘', aguacate:'🥑',
  nopal:'🌵', amaranto:'🌾', jitomate:'🍅', papa:'🥔', cana:'🌿' 
};

// ── Guardar cultivo → Flask → BD → redirigir a bitácora ──────────────────────
async function guardarCultivo() {
  const tipo   = document.getElementById('tipo-cultivo').value;
  const nombre = document.getElementById('nombre-parcela').value.trim();

  if (!tipo || !nombre) {
    alert('Por favor selecciona el tipo de cultivo y escribe el nombre de la parcela.');
    return;
  }

  const btnGuardar = document.querySelector('.btn-save');
  btnGuardar.textContent = 'Guardando...';
  btnGuardar.disabled    = true;

  try {
    // 1. Guardar en la BD vía Flask
    const res = await fetch('/api/parcelas', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tipo,
        nombre,
        lugar: coordsActuales.lugar || '',
        lat:   coordsActuales.lat,
        lon:   coordsActuales.lon,
      })
    });

    const result = await res.json();

    if (!result.ok) {
      alert('Error al guardar: ' + (result.error || 'intenta de nuevo'));
      return;
    }

    // 2. Crear la card en el dashboard con el id real de BD
    const parcela_id = result.parcela_id;
    _agregarCardDashboard(tipo, nombre, coordsActuales, parcela_id);

    // 3. Limpiar formulario y cerrar modal
    _limpiarModal();
    cerrarModal();

  } catch (e) {
    console.error(e);
    alert('Sin conexión. No se pudo guardar el cultivo.');
  } finally {
    btnGuardar.textContent = 'Guardar cultivo';
    btnGuardar.disabled    = false;
  }
}

// ── Agrega una card con semáforo en tiempo real ──
function _agregarCardDashboard(tipo, nombre, coords, parcela_id) {
  const icono  = _iconosCultivo[tipo] || '🌱';
  const lat    = coords.lat;
  const lon    = coords.lon;

  const card = document.createElement('div');
  // Iniciamos con una clase de carga
  card.className = `cultivo-card riesgo-cargando`;
  card.id = `card-${parcela_id}`;

  card.innerHTML = `
    <div class="cultivo-icon-wrap" id="icon-bg-${parcela_id}">${icono}</div>
    <div class="cultivo-info">
      <div class="cultivo-nombre">${nombre}</div>
      <div class="cultivo-alerta" id="alerta-${parcela_id}">⏳ Analizando clima...</div>
    </div>
    <div class="cultivo-right">
      <span class="riesgo-badge" id="badge-${parcela_id}">...</span>
      <span class="chevron">›</span>
    </div>
  `;

  card.style.cursor = 'pointer';
  card.onclick = () => {
    window.location.href = `/bitacora/${parcela_id}`; // Mantiene funcionalidad original
  };

  document.getElementById('cultivos-list').appendChild(card);

  // Si hay coordenadas, consultamos el clima real
  if (lat && lon) {
    obtenerRiesgoReal(lat, lon, parcela_id);
  }

  const total = document.querySelectorAll('.cultivo-card').length;
  document.getElementById('cultivo-count').textContent = total + ' parcelas';
}

// ── Función para consultar clima y actualizar semáforo ──
async function obtenerRiesgoReal(lat, lon, id) {
  try {
    // Usamos el pronóstico de hoy (daily) para ser más precisos con lo que ve el usuario
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto`;
    const res = await fetch(url);
    const data = await res.json();

    const tempMax = data.daily.temperature_2m_max[0];
    const tempMin = data.daily.temperature_2m_min[0];
    const lluvia  = data.daily.precipitation_sum[0];

    let nivel = 'bajo';
    let mensaje = '✅ Estado Óptimo';

    // AJUSTA ESTOS VALORES según lo que consideres "Alerta" en tu programa
    // Por ejemplo, solo marcar Rojo si la temperatura es realmente extrema
    if (tempMax > 38 || tempMin < 2 || lluvia > 40) {
      nivel = 'alto';
      mensaje = '🔴 Riesgo Crítico';
    }
    else if (tempMax > 32 || tempMin < 7 || lluvia > 15) {
      nivel = 'medio';
      mensaje = '🟡 Riesgo Moderado';
    }

    // Actualizar la interfaz
    const card = document.getElementById(`card-${id}`);
    const badge = document.getElementById(`badge-${id}`);
    const alerta = document.getElementById(`alerta-${id}`);
    const iconBg = document.getElementById(`icon-bg-${id}`);

    if (card) {
      card.classList.remove('riesgo-cargando', 'riesgo-bajo', 'riesgo-medio', 'riesgo-alto');
      card.classList.add(`riesgo-${nivel}`);

      badge.textContent = nivel.toUpperCase();
      badge.className = `riesgo-badge badge-${nivel}`;

      alerta.textContent = mensaje;

      if (iconBg) {
        iconBg.classList.remove('bajo', 'medio', 'alto');
        iconBg.classList.add(nivel);
      }
    }

  } catch (e) {
    console.error("Error en semáforo:", e);
    document.getElementById(`alerta-${id}`).textContent = "📍 Clima no disponible";
  }
}
// ── Limpiar campos del modal ──
function _limpiarModal() {
  document.getElementById('tipo-cultivo').value        = '';
  document.getElementById('nombre-parcela').value      = '';
  document.getElementById('municipio').value           = '';
  document.getElementById('coords-row').style.display  = 'none';
  document.getElementById('mapa-hint').style.opacity   = '1';
  coordsActuales = { lat: null, lon: null, lugar: null };
  if (marcador) { mapaLeaflet.removeLayer(marcador); marcador = null; }
}

// ── Cargar parcelas del usuario al abrir el dashboard ───────────────────────
async function cargarParcelasDashboard() {
  try {
    const res     = await fetch('/api/parcelas');
    const parcelas = await res.json();

    if (!Array.isArray(parcelas) || parcelas.length === 0) return;

    // Limpiar los cultivos de ejemplo hardcodeados
    document.getElementById('cultivos-list').innerHTML = '';

    parcelas.forEach(p => {
      _agregarCardDashboard(
        p.tipo,
        p.nombre,
        { lat: p.lat, lon: p.lon, lugar: p.lugar },
        p.id
      );
    });
  } catch (e) {
    console.warn('No se pudieron cargar las parcelas:', e);
  }
}

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', cargarParcelasDashboard);