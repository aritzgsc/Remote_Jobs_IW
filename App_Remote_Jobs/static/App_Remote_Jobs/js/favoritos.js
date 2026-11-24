/* Favoritos AJAX: el formulario sigue funcionando si JavaScript está desactivado. */
const ofertasPendientes = new Set();
document.addEventListener('submit', async (event) => {
  const form = event.target.closest('form.favorite-form');
  if (!form) return;
  event.preventDefault();
  const ofertaId = Number(form.dataset.ofertaId);
  if (form.dataset.enviando === 'si' || ofertasPendientes.has(ofertaId)) return;
  ofertasPendientes.add(ofertaId);
  form.dataset.enviando = 'si';
  const button = form.querySelector('button');
  if (button) button.disabled = true;
  try {
    const response = await fetch(form.action, {
      method: 'POST', body: new FormData(form), credentials: 'same-origin',
      headers: { Accept: 'application/json' }, redirect: 'follow'
    });
    if (response.redirected && !response.url.includes('/alternar/')) {
      window.location.assign(response.url);
      return;
    }
    if (!response.ok || !(response.headers.get('content-type') || '').includes('application/json')) {
      throw new Error('No se ha podido actualizar. Vuelve a intentarlo.');
    }
    const data = await response.json();
    document.querySelectorAll('form.favorite-form').forEach((other) => {
      if (Number(other.dataset.ofertaId) !== data.oferta_id) return;
      const control = other.querySelector('button');
      if (!control) return;
      control.classList.toggle('is-saved', data.guardada);
      control.setAttribute('aria-pressed', String(data.guardada));
      control.setAttribute('aria-label', `${data.guardada ? 'Quitar' : 'Guardar'} ${other.dataset.ofertaTitulo}${data.guardada ? ' de ofertas guardadas' : ''}`);
      control.replaceChildren();
      const symbol = document.createElement('span');
      symbol.setAttribute('aria-hidden', 'true');
      symbol.textContent = data.guardada ? '♥' : '♡';
      control.append(symbol, document.createTextNode(data.guardada ? ' Guardada' : ' Guardar'));
    });
    document.querySelectorAll('[data-favorite-count]').forEach((counter) => {
      counter.textContent = String(data.total_guardadas);
    });
    // En la vista de favoritos, quitar la tarjeta y actualizar el estado vacío.
    const grid = document.querySelector('[data-favorite-grid]');
    if (grid && !data.guardada) {
      form.closest('.job-card')?.remove();
      const total = document.querySelector('[data-favorite-total]');
      if (total) total.textContent = String(data.total_guardadas);
      if (!grid.querySelector('.job-card')) {
        const empty = document.createElement('p');
        empty.className = 'empty-state';
        empty.textContent = 'No quedan ofertas guardadas. Explora nuevas oportunidades.';
        grid.replaceWith(empty);
      }
    }
    const status = document.getElementById('favorite-feedback');
    if (status) status.textContent = data.guardada ? 'Oferta guardada.' : 'Oferta eliminada de guardadas.';
  } catch (error) {
    const status = document.getElementById('favorite-feedback');
    if (status) status.textContent = error.message || 'Error de conexión.';
  } finally {
    ofertasPendientes.delete(ofertaId);
    form.dataset.enviando = 'no';
    if (button) button.disabled = false;
  }
});
