# Remote Jobs

> Oportunidades de primer empleo y prácticas en modalidad remota o híbrida.

Remote Jobs organiza ofertas por sector y habilidades para ayudar a encontrar oportunidades profesionales relevantes. Cada oferta presenta la información disponible sobre modalidad, tipo de empleo y salario. Las cuentas personales permiten administrar el perfil y guardar ofertas para consultarlas más adelante.

[Funcionalidades](#funcionalidades) · [Instalación](#instalación) · [Configuración](#configuración) · [Uso](#uso) · [Pruebas](#pruebas) · [Estructura](#estructura) · [Seguridad](#seguridad-local)

## Funcionalidades

- [x] Portada funcional
- [x] Configuración local mediante variables de entorno
- [x] Plantilla base y estilos adaptables
- [x] Sectores gestionables desde el administrador
- [x] Habilidades y relaciones entre entidades
- [x] Ofertas con validaciones y datos salariales
- [x] Datos de demostración reproducibles
- [x] Portada conectada con la base de datos
- [x] Listado y detalle de ofertas
- [x] Búsqueda textual con sugerencias nativas
- [x] Filtros combinables por sector, habilidad y modalidad
- [x] Filtros avanzados, ordenación y paginación
- [x] Catálogos de sectores y habilidades
- [x] Modelos modulares y perfil de usuario
- [x] Registro, inicio y cierre de sesión
- [x] Edición de perfil y avatar, con vistas modularizadas
- [x] Ofertas guardadas de forma privada por usuario
- [x] Cambio y recuperación de contraseña
- [x] Inicio de sesión con correo o nombre de usuario
- [x] Preparación de Google OAuth
- [x] Botón de Google y datos básicos del perfil social
- [ ] Plantillas semánticas y componentes compartidos
- [ ] Pruebas de integración de páginas y permisos
- [ ] Guía de instalación y herramientas de arranque local
- [ ] Comentarios que explican decisiones técnicas no evidentes
- [ ] Pruebas de regresión, integridad salarial y comprobaciones
- [ ] Estilos visuales finales aplicados a todas las páginas

## Instalación

Necesitas Python 3.11 o posterior y `pip`. Ejecuta los comandos desde la carpeta que contiene `manage.py`.

### Windows · PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS · Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

## Configuración

El archivo `.env.example` documenta las variables reconocidas por el proyecto. Copia el archivo a `.env` y modifica los valores locales; no guardes credenciales reales en Git.

- `DJANGO_DEBUG`: activa el modo de depuración solo durante el desarrollo local.
- `DJANGO_ALLOWED_HOSTS`: lista de hosts permitidos, separados por comas.
- `DJANGO_EMAIL_BACKEND`: en desarrollo puede utilizarse el backend de consola para mostrar los correos en la terminal.
- `GOOGLE_OAUTH_CLIENT_ID` y `GOOGLE_OAUTH_CLIENT_SECRET`: credenciales locales para habilitar Google OAuth.

## Uso

```bash
python manage.py migrate
python manage.py cargar_datos_demo
python manage.py runserver
```

Abre [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Para gestionar los datos desde Django Admin, crea una cuenta con `python manage.py createsuperuser` y entra en `/admin/`.

El comando `cargar_datos_demo` crea un conjunto inicial reproducible y se puede volver a ejecutar sin duplicar los datos de ejemplo.

## Pruebas

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```


## Estructura

```text
Remote_Jobs/
├── App_Remote_Jobs/
│   ├── migrations/       # Evolución versionada del esquema de datos
│   ├── models/           # Sector, Habilidad, Oferta y perfil
│   ├── views/            # Vistas separadas por responsabilidad
│   ├── templates/        # Plantillas HTML del servidor
│   ├── static/            # Hoja de estilos
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── Remote_Jobs/         # Configuración del proyecto Django
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

Las vistas públicas, de ofertas, sectores, habilidades y cuentas residen en módulos distintos. Las plantillas se mantienen organizadas por página y, a partir de la refactorización de plantillas, reutilizan componentes comunes.

## Seguridad local

`.env`, `.venv/`, `db.sqlite3`, `media/` y `staticfiles/` son archivos o carpetas locales y no se deben versionar. El repositorio conserva las migraciones y los datos de demostración, no las cuentas, imágenes ni bases de datos locales.

El servidor `runserver` está pensado para desarrollo. Antes de publicar la aplicación, configura una clave secreta privada, `DEBUG=False`, los hosts permitidos y HTTPS.
