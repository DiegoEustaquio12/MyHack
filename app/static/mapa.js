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
 
    /*
      AQUÍ CONECTAS TU FLASK:
      ========================
      const riesgo = await fetch('/api/analisis/riesgo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lat, lon,
          cultivo: document.getElementById('tipo-cultivo').value
        })
      });
      const resultado = await riesgo.json();
      mostrarResultado(resultado);
    */
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
 
// ── Abrir modal (reemplaza la función existente en menu.js si existe) ──
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
 
// ── Guardar cultivo (reemplaza la función existente) ──
const _iconosCultivo = {
  maiz:'🌽', chile:'🌶️', frijol:'🫘', aguacate:'🥑',
  nopal:'🌵', amaranto:'🌾', jitomate:'🍅', papa:'🥔'
};
 
function guardarCultivo() {
  const tipo   = document.getElementById('tipo-cultivo').value;
  const nombre = document.getElementById('nombre-parcela').value.trim();
 
  if (!tipo || !nombre) {
    alert('Por favor selecciona el tipo de cultivo y escribe el nombre de la parcela.');
    return;
  }
 
  const icono  = _iconosCultivo[tipo] || '🌱';
  const lugar  = coordsActuales.lugar || 'Sin ubicación';
  const lat    = coordsActuales.lat;
  const lon    = coordsActuales.lon;
  const alerta = lat
    ? `📍 ${lugar} · ${lat.toFixed(3)}°, ${lon.toFixed(3)}°`
    : `📍 ${lugar}`;
 
  const card = document.createElement('div');
  card.className = 'cultivo-card riesgo-bajo';
  card.innerHTML = `
    <div class="cultivo-icon-wrap bajo">${icono}</div>
    <div class="cultivo-info">
      <div class="cultivo-nombre">${nombre}</div>
      <div class="cultivo-alerta">${alerta}</div>
    </div>
    <div class="cultivo-right">
      <span class="riesgo-badge badge-bajo">BAJO</span>
      <span class="chevron">›</span>
    </div>
  `;
 
  if (lat && lon) {
    card.style.cursor = 'pointer';
    card.onclick = () => {
      window.location.href =
        `bitacora.html?cultivo=${tipo}&nombre=${encodeURIComponent(nombre)}&lat=${lat}&lon=${lon}`;
    };
  }
 
  document.getElementById('cultivos-list').appendChild(card);
 
  const total = document.querySelectorAll('.cultivo-card').length;
  document.getElementById('cultivo-count').textContent = total + ' parcelas';
 
  /*
    CONECTAR A FLASK:
    =================
    await fetch('/api/cultivos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tipo, nombre, lugar, lat, lon })
    });
  */
 
  // Limpiar
  document.getElementById('tipo-cultivo').value   = '';
  document.getElementById('nombre-parcela').value = '';
  document.getElementById('municipio').value       = '';
  document.getElementById('coords-row').style.display = 'none';
  document.getElementById('mapa-hint').style.opacity  = '1';
  coordsActuales = { lat: null, lon: null, lugar: null };
  if (marcador) { mapaLeaflet.removeLayer(marcador); marcador = null; }
 
  cerrarModal();
}