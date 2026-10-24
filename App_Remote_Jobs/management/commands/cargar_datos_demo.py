"""Carga un juego de datos de demostración sin duplicarlo si se repite el comando."""
from datetime import date

from django.core.management.base import BaseCommand

from App_Remote_Jobs.models import Habilidad, Oferta, Sector


SECTORES = [
    {
        "nombre": "Desarrollo web",
        "slug": "desarrollo-web",
        "icono": "</>",
        "orden": 1,
        "descripcion": "Construye productos web útiles, accesibles y rápidos. Descubre puestos iniciales de frontend, backend y desarrollo full-stack.",
    },
    {
        "nombre": "Ciberseguridad",
        "slug": "ciberseguridad",
        "icono": "◇",
        "orden": 2,
        "descripcion": "Ayuda a proteger sistemas, datos y personas. Hay oportunidades de iniciación en análisis de seguridad, monitorización y respuesta a incidentes.",
    },
    {
        "nombre": "Diseño UX/UI",
        "slug": "diseno-ux-ui",
        "icono": "✳",
        "orden": 3,
        "descripcion": "Investiga necesidades, diseña interfaces inclusivas y convierte ideas complejas en experiencias digitales sencillas.",
    },
    {
        "nombre": "Ciencia de datos e IA",
        "slug": "ciencia-de-datos-ia",
        "icono": "⌁",
        "orden": 4,
        "descripcion": "Transforma datos en decisiones y experimenta con modelos de aprendizaje automático en equipos multidisciplinares.",
    },
    {
        "nombre": "Marketing digital",
        "slug": "marketing-digital",
        "icono": "↗",
        "orden": 5,
        "descripcion": "Combina creatividad y análisis para hacer crecer productos y comunidades a través de campañas digitales medibles.",
    },
    {
        "nombre": "Producto digital",
        "slug": "producto-digital",
        "icono": "◎",
        "orden": 6,
        "descripcion": "Conecta las necesidades de clientes y negocio para priorizar mejoras, medir resultados y ayudar a los equipos a entregar valor.",
    },
]

HABILIDADES = [
    ("Python", "python", "Lenguaje versátil utilizado en backend, automatización, análisis y aprendizaje automático.", "Programación"),
    ("Django", "django", "Framework de Python para desarrollar aplicaciones web con rapidez y estructura.", "Backend"),
    ("JavaScript", "javascript", "Lenguaje fundamental para añadir interactividad a la web.", "Frontend"),
    ("React", "react", "Biblioteca para construir interfaces de usuario basadas en componentes.", "Frontend"),
    ("SQL", "sql", "Consulta y manipulación de datos en bases de datos relacionales.", "Datos"),
    ("Git", "git", "Control de versiones y colaboración sobre código.", "Herramientas"),
    ("Inglés B2+", "ingles-b2", "Capacidad para trabajar y comunicarse profesionalmente en inglés.", "Idiomas"),
    ("Linux", "linux", "Uso de sistemas Linux, terminal y herramientas de administración.", "Sistemas"),
    ("SIEM", "siem", "Monitorización y correlación de eventos de seguridad.", "Ciberseguridad"),
    ("OWASP", "owasp", "Buenas prácticas y riesgos comunes de seguridad en aplicaciones web.", "Ciberseguridad"),
    ("Figma", "figma", "Diseño y prototipado colaborativo de interfaces digitales.", "Diseño"),
    ("Accesibilidad web", "accesibilidad-web", "Diseño de experiencias utilizables por personas con diferentes capacidades.", "Diseño"),
    ("Pandas", "pandas", "Limpieza, transformación y análisis de datos con Python.", "Datos"),
    ("Power BI", "power-bi", "Creación de informes visuales y cuadros de mando para apoyar decisiones.", "Datos"),
    ("SEO", "seo", "Optimización de contenidos y páginas para mejorar su visibilidad orgánica.", "Marketing"),
    ("Google Analytics", "google-analytics", "Interpretación de métricas de tráfico y comportamiento digital.", "Marketing"),
    ("Scrum", "scrum", "Marco de trabajo ágil para planificar y mejorar entregas de producto.", "Producto"),
    ("Analítica de producto", "analitica-producto", "Definición de métricas y análisis del uso de funcionalidades digitales.", "Producto"),
]

OFERTAS = [
    {
        "slug": "desarrollador-a-frontend-junior-react",
        "titulo": "Desarrollador/a Frontend Junior",
        "empresa": "Northstar Labs",
        "sector": "desarrollo-web",
        "resumen": "Construye interfaces rápidas y accesibles para una plataforma que utilizan equipos de todo el mundo.",
        "descripcion": "Te incorporarás a un equipo pequeño de producto para implementar nuevas pantallas, mejorar componentes existentes y colaborar en decisiones de experiencia de usuario. Tendrás acompañamiento técnico y revisiones de código desde el primer día.",
        "requisitos": "Conocimientos de JavaScript, HTML y CSS\nPrimer contacto con React o interés por aprenderlo\nConocer Git y el trabajo en equipo\nInglés B2 o equivalente",
        "beneficios": "Trabajo remoto desde España\nMentoría y plan de aprendizaje\nHorario flexible\nPresupuesto anual de formación",
        "habilidades": ["JavaScript", "React", "Git", "Inglés B2+", "Accesibilidad web"],
        "modalidad": "remoto", "tipo_empleo": "junior", "ubicacion": "España · Remoto",
        "salario_min": 26000, "salario_max": 32000, "fecha_publicacion": date(2026, 10, 20),
    },
    {
        "slug": "desarrollador-a-backend-python-practicas",
        "titulo": "Desarrollador/a Backend en prácticas",
        "empresa": "Brújula Digital",
        "sector": "desarrollo-web",
        "resumen": "Participa en APIs y servicios Python con foco en calidad, documentación y aprendizaje.",
        "descripcion": "Colaborarás en el diseño de endpoints, pequeñas tareas de integración y pruebas automatizadas. La posición está pensada para estudiantes de último curso o recién graduados que quieran dar sus primeros pasos en desarrollo backend.",
        "requisitos": "Fundamentos de Python\nConocimientos básicos de bases de datos y SQL\nCuriosidad por las APIs REST\nGanas de aprender y pedir feedback",
        "beneficios": "Prácticas remuneradas\nTutor/a asignado/a\nModelo híbrido con flexibilidad\nPosibilidad de incorporación",
        "habilidades": ["Python", "Django", "SQL", "Git"],
        "modalidad": "hibrido", "tipo_empleo": "practicas", "ubicacion": "Bilbao · Híbrido",
        "salario_min": 12000, "salario_max": 15000, "fecha_publicacion": date(2026, 10, 17),
    },
    {
        "slug": "analista-junior-ciberseguridad",
        "titulo": "Analista Junior de Ciberseguridad",
        "empresa": "Kern Security",
        "sector": "ciberseguridad",
        "resumen": "Ayuda a investigar alertas, identificar patrones y mejorar la defensa de entornos digitales.",
        "descripcion": "Trabajarás junto al equipo de operaciones de seguridad en la revisión inicial de alertas, documentación de incidentes y mejora de reglas de detección. Aprenderás metodologías y herramientas en un entorno acompañado.",
        "requisitos": "Fundamentos de redes y sistemas operativos\nInterés por Linux y seguridad defensiva\nCapacidad de documentar hallazgos\nInglés técnico B2 o equivalente",
        "beneficios": "Trabajo remoto dentro de España\nCertificaciones financiadas\nTurnos planificados con antelación\nPlan de carrera técnica",
        "habilidades": ["Linux", "SIEM", "OWASP", "Inglés B2+"],
        "modalidad": "remoto", "tipo_empleo": "junior", "ubicacion": "España · Remoto",
        "salario_min": 27000, "salario_max": 34000, "fecha_publicacion": date(2026, 10, 19),
    },
    {
        "slug": "ux-ui-designer-practicas",
        "titulo": "Diseñador/a UX/UI en prácticas",
        "empresa": "Pixelwave Studio",
        "sector": "diseno-ux-ui",
        "resumen": "Convierte investigación y feedback de usuarios en flujos e interfaces fáciles de usar.",
        "descripcion": "Participarás en entrevistas, organización de hallazgos, wireframes y prototipos de alta fidelidad. Colaborarás con diseño y desarrollo para comprobar que cada propuesta sea comprensible, coherente y accesible.",
        "requisitos": "Conocimientos básicos de diseño de interacción\nManejo inicial de Figma\nInterés por investigación de usuarios\nPortfolio académico o proyectos propios",
        "beneficios": "Mentoría de diseño\nHorario flexible\nPrácticas remuneradas\nPresupuesto para cursos y eventos",
        "habilidades": ["Figma", "Accesibilidad web", "Inglés B2+"],
        "modalidad": "hibrido", "tipo_empleo": "practicas", "ubicacion": "Donostia · Híbrido",
        "salario_min": 11500, "salario_max": 14500, "fecha_publicacion": date(2026, 10, 16),
    },
    {
        "slug": "data-analyst-junior",
        "titulo": "Data Analyst Junior",
        "empresa": "Orbit Data",
        "sector": "ciencia-de-datos-ia",
        "resumen": "Explora conjuntos de datos, prepara métricas y cuenta historias claras con información.",
        "descripcion": "Ayudarás a consolidar fuentes de datos, revisar su calidad y preparar análisis recurrentes para los equipos de producto y negocio. No esperamos que lo sepas todo: valoramos el razonamiento, la curiosidad y la comunicación.",
        "requisitos": "SQL para consultas y agregaciones\nConocimientos de Python y Pandas\nFundamentos de visualización de datos\nCapacidad para explicar resultados con claridad",
        "beneficios": "Remoto desde España\nFormación en analítica avanzada\nEquipo multidisciplinar\nDías de desconexión adicionales",
        "habilidades": ["Python", "Pandas", "SQL", "Power BI", "Inglés B2+"],
        "modalidad": "remoto", "tipo_empleo": "junior", "ubicacion": "España · Remoto",
        "salario_min": 28000, "salario_max": 35000, "fecha_publicacion": date(2026, 10, 18),
    },
    {
        "slug": "especialista-seo-practicas",
        "titulo": "Especialista SEO en prácticas",
        "empresa": "Lumen & Co.",
        "sector": "marketing-digital",
        "resumen": "Mejora la visibilidad orgánica de contenidos y aprende a medir el impacto de cada cambio.",
        "descripcion": "Apoyarás auditorías SEO, investigación de palabras clave, optimización de contenidos y análisis de resultados. Trabajarás de forma coordinada con contenidos, diseño y desarrollo.",
        "requisitos": "Interés por marketing de contenidos\nConocimientos básicos de SEO\nManejo de hojas de cálculo\nAtención al detalle y buena redacción",
        "beneficios": "Prácticas remuneradas\nModelo remoto\nAprendizaje con proyectos reales\nFeedback semanal",
        "habilidades": ["SEO", "Google Analytics", "Inglés B2+"],
        "modalidad": "remoto", "tipo_empleo": "practicas", "ubicacion": "España · Remoto",
        "salario_min": 10500, "salario_max": 13500, "fecha_publicacion": date(2026, 10, 15),
    },
    {
        "slug": "product-analyst-junior",
        "titulo": "Product Analyst Junior",
        "empresa": "Northstar Labs",
        "sector": "producto-digital",
        "resumen": "Ayuda al equipo de producto a priorizar mejoras a partir de métricas y señales de uso.",
        "descripcion": "Definirás junto a otras personas métricas de producto, analizarás embudos sencillos y prepararás conclusiones accionables para experimentos y decisiones de roadmap.",
        "requisitos": "SQL básico o intermedio\nInterés por productos digitales\nPensamiento analítico\nFacilidad para comunicar conclusiones",
        "beneficios": "Trabajo remoto\nMentoría con Product Managers\nPresupuesto de formación\nEquipo internacional",
        "habilidades": ["SQL", "Analítica de producto", "Scrum", "Inglés B2+"],
        "modalidad": "remoto", "tipo_empleo": "junior", "ubicacion": "España · Remoto",
        "salario_min": 27500, "salario_max": 33000, "fecha_publicacion": date(2026, 10, 14),
    },
    {
        "slug": "qa-automation-trainee",
        "titulo": "QA Automation Trainee",
        "empresa": "Brújula Digital",
        "sector": "desarrollo-web",
        "resumen": "Contribuye a que las nuevas funcionalidades lleguen con pruebas fiables y repetibles.",
        "descripcion": "Trabajarás con desarrollo para diseñar escenarios de prueba, detectar regresiones y automatizar comprobaciones de funcionalidades web. Es un puesto de entrada con acompañamiento.",
        "requisitos": "Conceptos básicos de programación\nInterés por calidad de software\nManejo básico de Git\nCuriosidad y pensamiento sistemático",
        "beneficios": "Modalidad híbrida flexible\nPlan de aprendizaje\nPrácticas remuneradas\nPosibilidad de crecer hacia automatización",
        "habilidades": ["Python", "Git", "JavaScript"],
        "modalidad": "hibrido", "tipo_empleo": "practicas", "ubicacion": "Vitoria-Gasteiz · Híbrido",
        "salario_min": 12000, "salario_max": 15000, "fecha_publicacion": date(2026, 10, 12),
    },
    {
        "slug": "data-science-intern",
        "titulo": "Data Science Intern",
        "empresa": "Orbit Data",
        "sector": "ciencia-de-datos-ia",
        "resumen": "Experimenta con datos reales y prototipos de modelos bajo la guía del equipo de ciencia de datos.",
        "descripcion": "Ayudarás a preparar datasets, explorar hipótesis y comparar prototipos de modelos. La prioridad será aprender buenas prácticas experimentales y saber comunicar limitaciones y resultados.",
        "requisitos": "Python y Pandas a nivel académico\nConocimientos básicos de estadística\nSQL básico\nInterés por machine learning",
        "beneficios": "Mentoría de ciencia de datos\nHorario compatible con estudios\nPrácticas remuneradas\nAcceso a cursos internos",
        "habilidades": ["Python", "Pandas", "SQL"],
        "modalidad": "remoto", "tipo_empleo": "practicas", "ubicacion": "España · Remoto",
        "salario_min": 12500, "salario_max": 15500, "fecha_publicacion": date(2026, 10, 10),
    },
]


class Command(BaseCommand):
    help = "Carga sectores, habilidades y ofertas de ejemplo para probar Remote Jobs."

    def handle(self, *args, **options):
        sectores = {}
        for datos in SECTORES:
            sector, _ = Sector.objects.update_or_create(slug=datos["slug"], defaults=datos)
            sectores[datos["slug"]] = sector

        habilidades = {}
        for nombre, slug, descripcion, categoria in HABILIDADES:
            habilidad, _ = Habilidad.objects.update_or_create(
                slug=slug,
                defaults={"nombre": nombre, "descripcion": descripcion, "categoria": categoria},
            )
            habilidades[nombre] = habilidad

        for datos in OFERTAS:
            datos_oferta = datos.copy()
            habilidades_oferta = datos_oferta.pop("habilidades")
            slug = datos_oferta["slug"]
            datos_oferta["sector"] = sectores[datos_oferta.pop("sector")]
            oferta, _ = Oferta.objects.update_or_create(slug=slug, defaults=datos_oferta)
            oferta.habilidades.set([habilidades[nombre] for nombre in habilidades_oferta])

        self.stdout.write(self.style.SUCCESS(
            f"Datos de demostración listos: {Sector.objects.count()} sectores, "
            f"{Habilidad.objects.count()} habilidades y {Oferta.objects.count()} ofertas."
        ))
