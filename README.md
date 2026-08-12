# web-pythoncises

Sitio web estatico con ejercicios de Python para estudiantes de programacion y entusiastas del lenguaje. Cada ejercicio tiene su propia pagina: se puede ver el codigo, copiarlo al portapapeles y descargar el archivo `.py` original. Los programas interactivos incluyen ademas una salida de ejemplo capturada ejecutandolos de verdad.

## Descripcion

Este proyecto forma parte de un portafolio personal. Reune 32 ejercicios de Python organizados en nueve categorias: juegos, patrones, calculadoras, web y API, texto y cadenas, archivos y PDF, tiempo y habitos, vision por computador y correo.

El sitio esta disenado con un enfoque minimalista (tema Atelier, paleta marina): papel marfil, tipografia serif Fraunces para texto y JetBrains Mono para el codigo, sin adornos. Es estatico: funciona abriendo `index.html` directamente en el navegador o alojado en GitHub Pages.

## Estructura

```
index.html                  indice: busqueda, categorias y enlaces
ejercicios/<slug>.html      una pagina por ejercicio (codigo, copiar, descargar, salida)
app.js                      busqueda en el indice y acciones copiar/descargar
styles.css                  estilos del sitio
tokens.css                  variables de diseno (colores, tipografia, espacio)
build_site.py               genera el sitio a partir de las carpetas de ejercicios
salidas.json                transcripciones de la salida real de cada programa
favicon.svg                 favicon de serpiente (y PNGs derivados)
<ejercicio>/                codigo fuente de cada ejercicio
```

## Regenerar el sitio

El codigo de los ejercicios vive en sus carpetas; las paginas HTML se generan con:

```bash
python3 build_site.py
```

Esto produce `index.html` y las paginas de `ejercicios/`. Si se anade un ejercicio nuevo hay que registrarlo en `CATEGORIAS` y `TITULOS` dentro de `build_site.py`.

Las salidas de ejemplo viven en `salidas.json` (un mapa de slug a transcripcion). Se capturaron ejecutando cada programa con entradas de ejemplo. Si el archivo no existe o falta un ejercicio, el sitio se genera igualmente, simplemente sin la seccion de salida para ese programa.

## Ejercicios

| # | Ejercicio | Carpeta |
|---|---|---|
| 01 | Adivina el numero | `adivina-numero/` |
| 02 | El ahorcado | `ahorcado/` |
| 03 | Piedra, papel o tijera | `piedra-papel-tijera/` |
| 04 | Dados aleatorios | `dados-aleatorios/` |
| 05 | Patron triangulo | `patron-triangulo/` |
| 06 | Patron triangulo invertido | `patron-triangulo-invertido/` |
| 07 | Patron rombo | `patron-rombo/` |
| 08 | Calculadora | `calculadora/` |
| 09 | Calculadora de IMC | `calculadora-indice-masa-corporal/` |
| 10 | Calculadora de propina | `calculadora-propina/` |
| 11 | Convertidor de moneda | `convertidor-moneda/` |
| 12 | Acortador de URLs | `corta-url/` |
| 13 | Generador de contrasenas | `generador-contrasenas/` |
| 14 | Generador de chistes | `generador-chiste-random/` |
| 15 | Historias divertidas | `historias-divertidas/` |
| 16 | Partes de un correo | `partes-correo/` |
| 17 | Markdown a HTML | `convertir-markdown-html/` |
| 18 | Combinar PDFs | `combinar-pdfs/` |
| 19 | Marca de agua | `marca-agua/` |
| 20 | OCR sobre PDF | `extraer-texto-pdf-ocr/` |
| 21 | Renombrador de archivos | `herramienta-renombra-archivo/` |
| 22 | Organizador de archivos | `organizador-archivos/` |
| 23 | Convertidor de videos | `convertir-videos/` |
| 24 | Cuenta atras | `cuenta-tiempo-atras/` |
| 25 | Pomodoro | `pomodoro/` |
| 26 | Reloj alarma | `reloj-alarma/` |
| 27 | Reloj digital | `reloj-digital/` |
| 28 | Rastreador de habitos | `rastreador-habitos-diarios/` |
| 29 | Lista de tareas | `lista-to-do/` |
| 30 | Detector de caras | `detector-cara-opencv/` |
| 31 | Reconocimiento facial | `sistema-reconocimiento-facial/` |
| 32 | Envio de correos desde CSV | `enviar-correo-csv/` |

## Licencia

Este proyecto esta bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para mas detalles.
