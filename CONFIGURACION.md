# Configuración · Remote Jobs

Guía para ejecutar el proyecto en local, configurar los roles administrativos, activar el inicio de sesión con Google y el correo, y tener en cuenta qué cambiar si se quisiera publicar.

## Instalación

Necesitas Python 3.11 o superior. Desde la carpeta que contiene `manage.py`:

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Si PowerShell bloquea la activación: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

El archivo `.env` va junto a `manage.py` y **no se sube a Git**.

## Variables de entorno

| Variable | Uso | En local |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Clave secreta de Django | Cualquier valor propio |
| `DJANGO_DEBUG` | Modo depuración | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por comas | `localhost,127.0.0.1,testserver` |
| `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_CLIENT_SECRET` | Credenciales de Google | Vacías hasta configurarlas |
| `DJANGO_EMAIL_BACKEND` | Cómo se envía el correo | Backend de consola (por defecto) |
| `DJANGO_EMAIL_HOST`, `_PORT`, `_HOST_USER`, `_HOST_PASSWORD`, `_USE_TLS` | Datos SMTP | Solo si usas SMTP |
| `DJANGO_DEFAULT_FROM_EMAIL` | Remitente de los correos | `Remote Jobs <no-reply@remotejobs.local>` |

Para generar una clave secreta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Arrancar la aplicación

```bash
python manage.py migrate
python manage.py configurar_roles
python manage.py cargar_datos_demo
python manage.py createsuperuser
python manage.py runserver
```

| URL | Contenido |
| --- | --- |
| `/` | Portada |
| `/ofertas/` · `/sectores/` · `/habilidades/` | Listados y detalle |
| `/cuenta/entrar/` · `/cuenta/registro/` | Acceso y registro |
| `/perfil/` | Perfil personal (requiere sesión) |
| `/favoritos/` | Ofertas guardadas (requiere sesión) |
| `/mi-espacio/` | Panel personal (requiere sesión) |
| `/mis-busquedas/` | Gestión de búsquedas guardadas (requiere sesión) |
| `/admin/` | Administración de Django |

`/accounts/` pertenece a `django-allauth` y se utiliza para el flujo de autenticación con Google.

## Datos de demostración

El comando `cargar_datos_demo` genera datos de ejemplo para las entidades propias de la aplicación:

- Sectores y habilidades.
- Ofertas de empleo y prácticas.
- Usuarios y perfiles.
- Ofertas guardadas.
- Búsquedas guardadas.

El comando se puede ejecutar varias veces sin duplicar los registros de demostración. Los usuarios de ejemplo están desactivados y no disponen de contraseñas utilizables.

Para probar las funcionalidades personales, crea una cuenta desde la página de registro.

## Roles administrativos

El comando `configurar_roles` crea dos grupos con diferentes permisos para gestionar el portal.

| Permisos | Editor de ofertas | Gestor de catálogo |
| --- | --- | --- |
| Consultar ofertas | Sí | Sí |
| Crear y modificar ofertas | Sí | No |
| Consultar sectores y habilidades | Sí | Sí |
| Crear y modificar sectores y habilidades | No | Sí |
| Eliminar registros | No | No |
| Gestionar usuarios y datos personales | No | No |

Para asignar un rol a un usuario:

1. Accede al panel de administración con un superusuario.
2. Selecciona el usuario al que quieres asignar el rol.
3. Activa su condición de personal (`is_staff`).
4. Asígnale el grupo correspondiente.
5. Guarda los cambios.

Los permisos de la tabla corresponden a los concedidos por cada grupo. Un usuario puede disponer de permisos adicionales si se le asignan individualmente o pertenece a otros grupos.

El superusuario conserva todos los permisos de administración. Los usuarios normales no tienen acceso al panel administrativo.

Los usuarios que forman parte del personal autorizado disponen de un acceso directo al administrador desde «Mi espacio».

## Inicio de sesión con Google

Sin credenciales, el botón «Continuar con Google» muestra una página con instrucciones y el acceso normal sigue funcionando.

1. En [Google Cloud Console](https://console.cloud.google.com/), crea un proyecto y configura la pantalla de consentimiento. Si está en modo de pruebas, añade tu cuenta como usuario de prueba.
2. Crea un cliente OAuth de tipo **Aplicación web**.
3. Añade esta URI de redireccionamiento autorizada, exactamente igual:

   ```text
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```

4. Copia el ID y el secreto a `.env` y reinicia el servidor:

   ```dotenv
   GOOGLE_OAUTH_CLIENT_ID=tu-client-id
   GOOGLE_OAUTH_CLIENT_SECRET=tu-client-secret
   ```

5. Abre <http://127.0.0.1:8000/cuenta/entrar/> y prueba el botón.

Si aparece `redirect_uri_mismatch`, compara la URI del error con la autorizada. Hay que abrir la web con `127.0.0.1`: `localhost` no vale como equivalente. El secreto no debe aparecer en capturas, commits ni mensajes.

Documentación: [Google OAuth](https://developers.google.com/identity/protocols/oauth2/web-server) y [proveedor Google de allauth](https://docs.allauth.org/en/latest/socialaccount/providers/google.html).

## Correo de recuperación de contraseña

Por defecto el correo no se envía: Django escribe el mensaje, con el enlace de recuperación, en la terminal donde corre `runserver`. Para probarlo, usa «He olvidado mi contraseña» en `/cuenta/entrar/` y copia el enlace de la terminal.

Para SMTP real, cambia estas variables con los datos de tu proveedor:

```dotenv
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DJANGO_EMAIL_HOST=smtp.ejemplo.com
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_HOST_USER=usuario
DJANGO_EMAIL_HOST_PASSWORD=credencial
DJANGO_EMAIL_USE_TLS=True
```

## JavaScript y AJAX

La gestión de ofertas guardadas y la eliminación de búsquedas guardadas utilizan JavaScript y `fetch()` para realizar peticiones al servidor sin recargar la página.

Los archivos correspondientes se encuentran en `App_Remote_Jobs/static/App_Remote_Jobs/js/`:

- `favoritos.js`: gestión de favoritos, actualización de contadores y del listado de ofertas guardadas.
- `busquedas.js`: eliminación de búsquedas guardadas y actualización del listado.

No es necesario instalar ninguna dependencia adicional para utilizar estas funcionalidades.

Las operaciones mantienen la protección CSRF de Django y disponen de una alternativa mediante formularios tradicionales cuando JavaScript está desactivado.

## Despliegue

El proyecto está pensado para desarrollo local. Si se quisiera publicar, habría que revisar al menos:

- `DJANGO_SECRET_KEY` única, `DJANGO_DEBUG=False` y `DJANGO_ALLOWED_HOSTS` con el dominio real.
- HTTPS y la configuración de proxy del proveedor. Al desactivar `DEBUG`, se activan las cookies seguras de sesión y CSRF, se rechaza la clave secreta predeterminada y se refuerzan determinadas cabeceras de seguridad.
- Configuración de la redirección a HTTPS y revisión de los ajustes de seguridad mediante `python manage.py check --deploy`.
- `python manage.py collectstatic --noinput` y un servidor que sirva `STATIC_ROOT`. No hay un servidor de estáticos incluido.
- Las fotos subidas van a `media/`, que Django solo sirve en modo `DEBUG`. Hace falta almacenamiento persistente y una forma de servirlo.
- Una base de datos con copias de seguridad en lugar del `db.sqlite3` local.
- Correo real y credenciales de Google para el dominio publicado. Convendría además activar la verificación de correo (`ACCOUNT_EMAIL_VERIFICATION`), hoy desactivada.
- Un servidor WSGI/ASGI de producción. `runserver` es solo para desarrollo.

Al actualizar una instalación, ejecuta siempre `python manage.py migrate`.

## Problemas frecuentes

| Síntoma | Qué mirar |
| --- | --- |
| `ModuleNotFoundError` | Activa `.venv` e instala `requirements.txt`. |
| «Host no permitido» | Añade el host a `DJANGO_ALLOWED_HOSTS`. |
| Listado vacío | Ejecuta `python manage.py cargar_datos_demo`. |
| No aparecen los grupos administrativos | Ejecuta `python manage.py configurar_roles`. |
| Un usuario no puede entrar al administrador | Comprueba que está activo y tiene habilitada su condición de personal. |
| Un usuario no puede gestionar una entidad | Revisa los permisos de su grupo administrativo. |
| El botón de Google enseña instrucciones | Faltan las dos variables de Google o no se reinició el servidor. |
| No llega el correo | Con el backend de consola, mira la terminal. Con SMTP, revisa host, puerto, credenciales y TLS. |
| No se ve el avatar | Comprueba formato (JPG, PNG, WebP), tamaño (máx. 3 MB) y que `DEBUG` esté activo en local. |
| Los favoritos o búsquedas recargan la página | Comprueba que JavaScript está habilitado y revisa la consola del navegador. |
| No se aplican los estilos del administrador | Recarga la página sin caché (`Ctrl + F5`) y comprueba que se está sirviendo `admin.css`. |