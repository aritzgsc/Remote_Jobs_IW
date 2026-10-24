# Remote Jobs

> Encuentra oportunidades de primer empleo y prácticas en modalidad remota o híbrida.

Remote Jobs reúne ofertas organizadas por sector y habilidades para que sea más sencillo descubrir oportunidades relevantes. Cada oferta presenta la información disponible sobre su modalidad, tipo de empleo y condiciones; las cuentas personales permiten mantener un perfil y guardar ofertas para consultarlas más adelante.

## Navegación

[Funcionalidades](#funcionalidades) · [Calidad y mantenimiento](#calidad-y-mantenimiento) · [Instalación](#instalacion) · [Configuración](#configuracion) · [Pruebas](#pruebas-y-comprobaciones) · [Estructura](#estructura) · [Seguridad](#seguridad-local)

## Funcionalidades

- [x] Portada funcional
- [x] Configuración mediante variables de entorno
- [ ] Plantilla base y estilos adaptables
- [ ] Gestión de sectores desde el administrador
- [ ] Habilidades relacionadas con sectores y ofertas
- [ ] Ofertas con modalidad, tipo y datos salariales
- [ ] Datos de demostración reproducibles
- [ ] Portada conectada a la base de datos
- [ ] Listado y detalle de ofertas
- [ ] Búsqueda textual y sugerencias nativas
- [ ] Filtros por sector, habilidad y modalidad
- [ ] Filtros avanzados, ordenación y paginación
- [ ] Catálogos de sectores y habilidades
- [ ] Modelos modulares y perfil de usuario
- [ ] Registro, inicio y cierre de sesión
- [ ] Edición de perfil e imagen de avatar
- [ ] Ofertas guardadas de forma privada por usuario
- [ ] Cambio y recuperación de contraseña
- [ ] Acceso mediante correo o nombre de usuario
- [ ] Preparación de la autenticación con Google
- [ ] Botón de Google y datos del perfil social
- [ ] Plantillas de cuenta y componentes compartidos

## Calidad y mantenimiento

- [ ] Pruebas de integración de las funciones principales
- [ ] Guía de instalación, uso y configuración
- [ ] Comentarios sobre decisiones técnicas no evidentes
- [ ] Pruebas de regresión y control de permisos
- [ ] Documentación de arquitectura y configuración

## Requisitos

- Python 3.11 o posterior.
- `pip`, incluido con las instalaciones habituales de Python.

## Instalación

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS y Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Abre `.env` y sustituye los valores de ejemplo por los ajustes locales que necesites. Define una clave secreta propia para Django; no compartas este archivo ni lo añadas al repositorio.

## Configuración

- `DJANGO_DEBUG`: déjalo activado únicamente mientras desarrollas en local.
- `DJANGO_ALLOWED_HOSTS`: enumera los hosts admitidos, separados por comas.

El archivo `.env.example` contiene nombres de variables y valores de ejemplo, no credenciales reales.

## Ejecutar la aplicación

```bash
python manage.py migrate
python manage.py runserver
```

Abre [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en el navegador. Para administrar los datos, crea una cuenta de administrador con `python manage.py createsuperuser` y entra en `/admin/`.

## Pruebas y comprobaciones

```bash
python manage.py check
python manage.py test
```

## Estructura

```text
Remote_Jobs/
├── App_Remote_Jobs/    # Modelos, vistas, formularios y plantillas
├── Remote_Jobs/        # Configuración y rutas del proyecto Django
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Seguridad local

Los archivos `.env`, `.venv/`, `db.sqlite3`, `media/` y `staticfiles/` son locales y están excluidos de Git. Las migraciones y el comando de demostración permiten reconstruir la base de datos sin compartir datos personales.

El servidor `runserver` está pensado para desarrollo. Antes de publicar la aplicación, configura una clave secreta privada, `DJANGO_DEBUG=False`, los hosts permitidos y HTTPS.
