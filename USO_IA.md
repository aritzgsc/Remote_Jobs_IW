# Uso de herramientas de IA

En Remote Jobs usamos la IA como **ayuda para aprender, desarrollar y desbloquearnos**. Gran parte del trabajo se ha resuelto buscando en internet, a veces con las respuestas de IA de Google, para programar bien lo que queríamos. También hemos utilizado ChatGPT para plantear funcionalidades, generar código, revisar el proyecto y trabajar los estilos de la aplicación.

## Resumen

| Integrante | Herramienta | Para qué | Conversaciones |
| --- | --- | --- | --- |
| **Aritz** | ChatGPT | Propuesta y planteamiento inicial del proyecto Django. Actualización de los estilos CSS. | [Propuesta proyecto Django](https://chatgpt.com/share/6add2629-f68c-83eb-a46e-527b79e9131c) · [Actualizar estilos CSS](https://chatgpt.com/share/6ae1c832-4880-83ed-a71e-aad9b1a6194c) |
| **Iker** | ChatGPT | Análisis del repositorio Django. Personalización de los estilos del administrador. | [Analizar repositorio Django](https://chatgpt.com/share/6ade39d1-7920-83ed-b54b-fdcaf2592e2e) · [Personalizar administración Django](https://chatgpt.com/share/6b060295-5d80-83ed-8855-6cce27e8d257?no_universal_links=1) |
| **Oier** | ChatGPT | Recuperación de contraseña. | [Recuperación de contraseña](https://chatgpt.com/share/6ae1c7e1-5568-83eb-8119-e6931af0c0b4) |
| **Ander** | ChatGPT | Revisión entrega final (E3). | [Evaluación entrega Django](https://chatgpt.com/share/6ae463bf-796c-83eb-9977-daecf833b6ce) |

## Los estilos

La hoja de estilos (`estilos.css`) la generó **ChatGPT casi por completo**, a partir de unas **imágenes de referencia creadas con Canva** a mano, utilizando como base la plantilla inicial y ciertas ideas que teníamos de antemano. Posteriormente, hemos revisado y modificado el CSS para corregir detalles visuales y adaptarlo a las nuevas funcionalidades de la aplicación.

Para la personalización del administrador de Django (`admin.css`) hemos seguido un proceso parecido. Primero se creó la plantilla `base_site.html` para personalizar la plantilla original del administrador y poder cargar nuestra propia hoja de estilos. Después, se pidió a ChatGPT que generase una primera versión del CSS tomando como referencia los estilos de nuestra aplicación.

A partir de esa primera versión, se crearon nuevas imágenes de referencia con Canva para representar cómo queríamos que se viesen las diferentes pantallas del administrador. Estas imágenes se utilizaron para mejorar progresivamente el CSS generado por ChatGPT.

Por último, se retocaron los estilos a mano, corrigiendo pequeños errores y ajustando colores, tamaños, márgenes y otros detalles visuales. También se comprobó el CSS mediante el validador de W3C.

## Búsquedas en internet

Muchas dudas de Python, Django (plantillas, formularios, modelos, migraciones, autenticación), JavaScript y errores se han resuelto directamente en Google, a veces con ayuda de su IA. También hemos pedido recomendaciones sobre los textos para rellenar la página, emojis, caracteres, ideas para logos y otros elementos visuales.

Estas consultas no dejaron ninguna conversación que guardar, así que el registro de arriba no recoge todo lo que hemos consultado.

## Ampliación del proyecto (E4)

En la cuarta entrega hemos utilizado ChatGPT también para plantear y generar código para las nuevas funcionalidades, como la gestión de favoritos mediante AJAX, las búsquedas guardadas con ModelForm, el panel personal del usuario, los roles administrativos y la ampliación de los datos de demostración.

También nos ha servido para revisar aspectos de seguridad, rendimiento y accesibilidad, y para organizar la implementación de las funcionalidades de manera progresiva.

## Cómo lo integramos

Lo que salía de una búsqueda o de una conversación con ChatGPT lo adaptábamos al proyecto y lo probábamos antes de quedarnos con ello.

En esta última entrega hemos ido incorporando las nuevas funcionalidades por separado, comprobando su funcionamiento y realizando modificaciones a mano cuando algo no nos convencía o no encajaba con el resto de la aplicación.

Para nosotros es importante entender y saber explicar el código que se entrega, además de conseguir que la aplicación funcione correctamente y tenga una buena estética.

## Revisión final

El estado final de la E3 fue revisado por ChatGPT, a partir del cual pudimos ver qué habíamos hecho mejor y peor, tanto para corregirlo en aquella entrega como para tenerlo en cuenta de cara a futuras entregas.

Durante la E4 hemos seguido utilizando ChatGPT para revisar las nuevas funcionalidades, detectar posibles errores y proponer mejoras, complementando estas revisiones con comprobaciones manuales de la aplicación.