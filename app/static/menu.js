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

    // ── MODAL ──
   function abrirModal() {
      document.getElementById('modal').classList.add('open');
    }

    function cerrarModal() {
      document.getElementById('modal').classList.remove('open');
    }

    function cerrarModalFuera(e) {
      if (e.target === document.getElementById('modal')) cerrarModal();
    }

    // Iconos por tipo de cultivo
    const iconos = {
      maiz: '🌽', chile: '🌶️', frijol: '🫘', aguacate: '🥑',
      nopal: '🌵', amaranto: '🌾', jitomate: '🍅', papa: '🥔'
    };

    // ── AGREGAR CULTIVO ──
    function guardarCultivo() {
      const tipo   = document.getElementById('tipo-cultivo').value;
      const nombre = document.getElementById('nombre-parcela').value.trim();
      const muni   = document.getElementById('municipio').value.trim();

      if (!tipo || !nombre) {
        alert('Por favor llena el tipo de cultivo y el nombre de la parcela.');
        return;
      }

      const icono = iconos[tipo] || '🌱';
      const nombreLabel = nombre + (muni ? ` — ${muni}` : '');

      const card = document.createElement('div');
      card.className = 'cultivo-card riesgo-bajo';
      card.innerHTML = `
        <div class="cultivo-icon-wrap bajo">${icono}</div>
        <div class="cultivo-info">
          <div class="cultivo-nombre">${nombreLabel}</div>
          <div class="cultivo-alerta">✅ Recién agregado — calculando riesgo...</div>
        </div>
        <div class="cultivo-right">
          <span class="riesgo-badge badge-bajo">BAJO</span>
          <span class="chevron">›</span>
        </div>
      `;

      document.getElementById('cultivos-list').appendChild(card);

      // Actualizar contador
      const total = document.querySelectorAll('.cultivo-card').length;
      document.getElementById('cultivo-count').textContent = total + ' parcelas';

      // Limpiar y cerrar
      document.getElementById('tipo-cultivo').value = '';
      document.getElementById('nombre-parcela').value = '';
      document.getElementById('municipio').value = '';
      cerrarModal();
    }