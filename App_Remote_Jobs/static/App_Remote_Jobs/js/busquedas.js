document.addEventListener('submit', async (event) => {
    const form = event.target.closest('.delete-search-form');
    if (!form) return;

    event.preventDefault();

    const button = form.querySelector('button');
    const feedback = document.getElementById('search-feedback');

    if (button.disabled) return;
    button.disabled = true;
    feedback.textContent = '';

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            credentials: 'same-origin',
            headers: { Accept: 'application/json' }
        });

        if (response.redirected) {
            window.location.assign(response.url);
            return;
        }

        if (!response.ok) {
            throw new Error('No se ha podido eliminar la búsqueda.');
        }

        const data = await response.json();

        if (data.eliminada) {
            form.closest('.saved-search-row').remove();

            if (!document.querySelector('.saved-search-row')) {
                document.querySelector('.saved-search-list').remove();
                document.getElementById('search-empty').hidden = false;
            }

            feedback.textContent = 'Búsqueda eliminada correctamente.';
        }
    } catch (error) {
        feedback.textContent = 'No se ha podido eliminar la búsqueda.';
    } finally {
        button.disabled = false;
    }
});