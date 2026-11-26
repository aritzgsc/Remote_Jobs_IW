# Despliegue de Remote Jobs en Render

La configuración local sigue utilizando SQLite y el servidor de desarrollo de Django. En Render se utiliza PostgreSQL, Gunicorn y WhiteNoise. No se incluyen credenciales reales.

## 1. Crear la base de datos y el servicio

1. En https://dashboard.render.com/ crea una base de datos PostgreSQL. Para la demostración puedes elegir Free. Guarda su URL interna en las variables del servicio, no en Git.
2. Crea un Web Service Python conectado al repositorio `Remote_Jobs_IW`, rama `main`, en la misma región que PostgreSQL. Deja Root Directory vacío si `manage.py` está en la raíz.
3. Configura Build Command: `bash build.sh`.
4. Configura Start Command: `gunicorn Remote_Jobs.wsgi:application --bind 0.0.0.0:$PORT --workers 2`.
5. En Environment añade `DATABASE_URL` (URL interna), `DJANGO_SECRET_KEY` (Generate), `DJANGO_DEBUG=False`. Render proporciona `RENDER` y `RENDER_EXTERNAL_HOSTNAME`; el dominio se añade automáticamente a ALLOWED_HOSTS y CSRF_TRUSTED_ORIGINS. Para otro dominio configura `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS` (orígenes HTTPS).
6. No introduzcas el `.env` local en Git. No copies tu SQLite: la base nueva comienza vacía y se migra con `build.sh`.

## 2. Google OAuth

En Google Cloud, en el cliente OAuth de tipo aplicación web, añade el dominio HTTPS real de Render como origen autorizado y `https://TU-DOMINIO.onrender.com/accounts/google/login/callback/` como URI de redirección autorizada. Mantén también las URI locales si las necesitas. Añade `GOOGLE_OAUTH_CLIENT_ID` y `GOOGLE_OAUTH_CLIENT_SECRET` en Render. Si la pantalla de consentimiento está en modo pruebas, autoriza las cuentas necesarias.

## 3. Datos iniciales y administración

La carga de datos demo se hace una sola vez; el comando puede actualizar las ofertas de ejemplo, no conviene ejecutarlo en cada despliegue. Si tienes Shell, ejecuta `python manage.py cargar_datos_demo` y `python manage.py createsuperuser`. En un servicio gratuito sin Shell puedes cambiar temporalmente el Build Command a `bash build.sh && python manage.py cargar_datos_demo` y desplegar una vez. Para crear el administrador, configura temporalmente las variables `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` (contraseña fuerte y privada) y utiliza `bash build.sh && python manage.py createsuperuser --noinput` en un único despliegue. Después devuelve el Build Command a `bash build.sh`, elimina esas tres variables y vuelve a desplegar. No ejecutes createsuperuser otra vez con el mismo usuario. No publiques credenciales del administrador; los usuarios demo de la semilla están inactivos.

## 4. Fotos y recuperación de contraseña

En Render Free los avatares se guardan en el disco local temporal. Se pueden subir y visualizar durante la demostración, pero pueden perderse tras reinicios o despliegues. En ese caso la referencia puede seguir en PostgreSQL: elimina o vuelve a subir la foto desde Editar perfil. Las imágenes estáticas y las fotos de Google no dependen de este almacenamiento. No se copian fotos locales automáticamente. Usa imágenes ficticias para la demostración.

Render Free bloquea los puertos SMTP 25, 465 y 587. Para que la recuperación funcione, configura un proveedor de correo por HTTPS: la integración preparada es Brevo, con `BREVO_API_KEY` y `DJANGO_DEFAULT_FROM_EMAIL` (remitente verificado en Brevo). Sin proveedor, la recuperación informa que no está habilitada; no simula que se envía un correo ni imprime tokens en logs. En local se mantiene el backend de consola original.

## 5. Comprobaciones antes de compartir

- Local: `python -m pip install -r requirements.txt`, `python manage.py check`, `python manage.py migrate`, `python manage.py runserver`.
- Render: portada, CSS/JS, ofertas iniciales, registro, login local y Google, vinculación, persistencia después de otro deploy, favoritos, búsquedas, permisos y admin.
- Subir, sustituir y eliminar un avatar en Render; comprobar que las demás funcionalidades mantienen sus datos tras otro deploy. La persistencia del avatar no está garantizada. Si activas correo, recuperar contraseña por un correo de prueba real.
- Revisar logs y `python manage.py check --deploy` con el entorno de producción. No afirmar que las comprobaciones han pasado antes de hacerlas.

La base PostgreSQL Free de Render expira a los 30 días y el servicio puede dormirse tras 15 minutos. Para una entrega duradera, usar una base persistente y realizar copias de seguridad. Las cuentas y datos de prueba del SQLite local no se migran de forma automática.

Documentación: https://render.com/docs/deploy-django · https://render.com/docs/free · https://render.com/articles/can-i-send-email-over-smtp-from-render
