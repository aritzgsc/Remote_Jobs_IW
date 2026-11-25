# 💼 Remote Jobs

> **Ofertas de primer empleo y prácticas en remoto o híbrido, en un solo sitio.**

[Funcionalidades](#-funcionalidades) · [Puesta en marcha](#-puesta-en-marcha) · [Modelo de datos](#-modelo-de-datos) · [Estructura](#-estructura) · [Estado](#-estado-del-proyecto)

---

Remote Jobs es una aplicación web hecha con **Django** para encontrar ofertas junior y prácticas que se pueden hacer a distancia. Se puede explorar sin cuenta; al registrarse, cada persona tiene su perfil, su propia lista de ofertas guardadas y un espacio donde organizar sus búsquedas.

## ✨ Funcionalidades

| | Qué permite hacer |
| --- | --- |
| 🔎 **Búsqueda** | Palabras clave y filtros combinables: sector, habilidad, modalidad, tipo de empleo, ubicación, salario y fechas. |
| ↕️ **Orden y paginación** | Ordenar por fecha, título o salario. Los filtros se mantienen al cambiar de página. |
| 🗂️ **Sectores y habilidades** | Directorios con página propia que enlazan a las ofertas relacionadas. |
| 👤 **Cuentas** | Registro, acceso con correo o usuario, cambio y recuperación de contraseña. |
| 🔐 **Google** | Inicio de sesión con Google mediante `django-allauth` (opcional, con credenciales propias). |
| 🧑‍💼 **Perfil** | Nombre, titular, ubicación, biografía, portfolio y foto, subida o tomada de Google. |
| ⭐ **Guardadas** | Lista privada de ofertas por cuenta, actualizada sin recargar la página. |
| 🔖 **Búsquedas guardadas** | Guardar, recuperar y eliminar combinaciones de filtros de búsqueda. |
| 🏠 **Mi espacio** | Panel personal desde el que consultar ofertas y búsquedas guardadas. |
| 🛠️ **Administración** | Panel personalizado con gestión de entidades y diferentes roles administrativos. |
| 🧪 **Datos de demo** | Generación de sectores, habilidades, ofertas, usuarios, perfiles, favoritos y búsquedas guardadas. |

La interfaz se genera en el servidor con plantillas de Django. La búsqueda y los filtros utilizan formularios normales, mientras que la gestión de favoritos y la eliminación de búsquedas guardadas utilizan JavaScript y AJAX para evitar recargas innecesarias. Los estilos son adaptables a diferentes tamaños de pantalla.

<details>
  <summary><h2>Cambios y añadidos respecto al enunciado</h2></summary>

  ### Decisiones de diseño

  - **Portada:** se muestran las ofertas más recientes y un resumen de los sectores disponibles, incluyendo una oferta representativa de cada sector que dispone de ofertas publicadas.
  - **Navegación:** las opciones personales, como Mi espacio y Guardadas, únicamente aparecen cuando el usuario ha iniciado sesión.
  - **Administración:** el panel mantiene la identidad visual del resto de la aplicación y utiliza un tema claro uniforme.

  ### Funcionalidades adicionales

  - **Búsqueda avanzada:** filtros combinables por sector, habilidad, modalidad, tipo de empleo, ubicación, salario y fecha de publicación. También permite buscar por palabras clave y ordenar los resultados.
  - **Paginación:** los listados de ofertas se dividen en páginas y mantienen los filtros aplicados al navegar.
  - **Cuentas de usuario:** registro e inicio de sesión mediante correo electrónico o nombre de usuario.
  - **Autenticación con Google:** posibilidad de iniciar sesión mediante Google OAuth, previa configuración de las credenciales correspondientes.
  - **Perfiles personales:** cada usuario puede personalizar su perfil con nombre público, titular profesional, ubicación, biografía, portfolio e imagen de perfil.
  - **Gestión de contraseñas:** cambio y recuperación de contraseña mediante los mecanismos de Django.
  - **Ofertas guardadas:** gestión de favoritos mediante AJAX, con actualización automática del contador y del listado.
  - **Búsquedas guardadas:** almacenamiento de filtros mediante un modelo y un ModelForm propios. Cada usuario únicamente puede gestionar sus búsquedas.
  - **Mi espacio:** acceso centralizado a la actividad personal y, para usuarios autorizados, al panel de administración.
  - **Administración personalizada:** adaptación visual del administrador y creación de grupos con distintos permisos de gestión.
  - **Información adicional de las ofertas:** empresa, modalidad, tipo de empleo, ubicación, rango salarial, requisitos, beneficios y fecha de publicación.
  - **Directorios mejorados:** los sectores y habilidades muestran información adicional y el número de ofertas relacionadas.
  - **Rendimiento y seguridad:** optimización de las consultas de los contadores administrativos y refuerzo de los ajustes de seguridad para producción.
  - **Accesibilidad:** asociación de los campos de los formularios con sus correspondientes textos de ayuda.

</details>

## 🚀 Puesta en marcha

Desde la carpeta que contiene `manage.py`:

```bash
python -m venv .venv
# activa el entorno virtual (ver CONFIGURACION.md) y luego:
python -m pip install -r requirements.txt
cp .env.example .env          # en PowerShell: Copy-Item .env.example .env
python manage.py migrate
python manage.py configurar_roles
python manage.py cargar_datos_demo
python manage.py runserver
```

La web queda en <http://127.0.0.1:8000/>. Para entrar en `/admin/` crea antes un administrador con `python manage.py createsuperuser`.

Las variables de entorno, los roles administrativos, Google OAuth, el correo y las notas de despliegue están en **[CONFIGURACION.md](CONFIGURACION.md)**.

## 🧩 Modelo de datos

La **oferta** es el centro del modelo: pertenece a un sector, pide varias habilidades y puede ser guardada por muchas personas. Cada usuario de Django tiene además un perfil y puede almacenar sus propios filtros de búsqueda.

```mermaid
flowchart LR
    Sector ---|"1"| r1{"agrupa"} -->|"N"| Oferta
    Oferta ---|"N"| r2{"pide"} ---|"M"| Habilidad
    Usuario ---|"1"| r3{"tiene"} ---|"1"| PerfilUsuario
    Usuario ---|"1"| r4{"guarda"} -->|"N"| OfertaGuardada
    Oferta ---|"1"| r5{"aparece en"} -->|"N"| OfertaGuardada
    Usuario ---|"1"| r6{"conserva"} -->|"N"| BusquedaGuardada
```

Cada rombo es una relación y el número junto a cada caja indica cuántos elementos de esa entidad intervienen.

`OfertaGuardada` es la tabla intermedia que une usuarios y ofertas mediante una relación de muchos a muchos. `BusquedaGuardada` almacena los filtros y el criterio de ordenación de una búsqueda, asociados al usuario que la ha creado.

Validaciones propias: el salario máximo no puede ser menor que el mínimo, los rangos de fechas de búsqueda deben ser coherentes y las fotos de perfil deben ser JPG, PNG o WebP de hasta 3 MB.

## 📁 Estructura

```text
Remote_Jobs_IW/
├── manage.py
├── requirements.txt
├── .env.example
├── Remote_Jobs/                 # Configuración del proyecto
└── App_Remote_Jobs/             # La aplicación
    ├── models/                  # Entidades y relaciones
    ├── views/                   # Ofertas, cuentas, favoritos, búsquedas...
    ├── templates/               # Páginas, componentes y administración
    ├── static/App_Remote_Jobs/
    │   ├── css/
    │   │   ├── estilos.css      # Estilos generales
    │   │   └── admin.css        # Estilos de administración
    │   └── js/
    │       ├── favoritos.js     # Gestión AJAX de favoritos
    │       └── busquedas.js     # Eliminación AJAX de búsquedas
    ├── management/commands/
    │   ├── cargar_datos_demo.py
    │   └── configurar_roles.py
    ├── forms.py  urls.py  admin.py
    ├── backends.py              # Acceso con correo o nombre de usuario
    ├── adapters.py              # Perfil a partir de los datos de Google
    ├── signals.py               # Crea el perfil al crear la cuenta
    └── context_processors.py    # Perfil y favoritos en las plantillas
```

## 🚧 Estado del proyecto

- Los datos son de demostración; la solicitud de cada oferta remite a una URL externa.
- Las funcionalidades se comprueban en local desde el navegador y el administrador.
- La verificación de correo al registrarse está desactivada, y el correo de recuperación se escribe en la consola por defecto.
- Usa SQLite y almacenamiento local de imágenes. Para publicarlo habría que ajustar varias cosas, listadas en [CONFIGURACION.md](CONFIGURACION.md#despliegue).
- Se han incorporado ajustes de seguridad para producción, aunque el despliegue de Django requiere configuración adicional.

## 👥 Equipo

Proyecto realizado por Aritz, Iker, Oier y Ander. El uso de herramientas de apoyo se explica en [USO_IA.md](USO_IA.md).