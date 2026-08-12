#!/usr/bin/env python3
"""Genera el sitio web a partir de las carpetas de ejercicios.

Uso:  python3 build_site.py

Produce:
- index.html                  índice ligero (búsqueda + categorías + enlaces)
- ejercicios/<slug>.html      una página por ejercicio (código, copiar, descargar)

El código de cada ejercicio vive solo en su propia página; el índice no
contiene código. El diseño se define en styles.css y tokens.css.
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SALIDA = RAIZ / "ejercicios"

CATEGORIAS = [
    ("Juegos", [
        "adivina-numero",
        "ahorcado",
        "piedra-papel-tijera",
        "dados-aleatorios",
    ]),
    ("Patrones", [
        "patron-triangulo",
        "patron-triangulo-invertido",
        "patron-rombo",
    ]),
    ("Calculadoras", [
        "calculadora",
        "calculadora-indice-masa-corporal",
        "calculadora-propina",
    ]),
    ("Web y API", [
        "convertidor-moneda",
        "corta-url",
    ]),
    ("Texto y cadenas", [
        "generador-contraseñas",
        "generador-chiste-random",
        "historias-divertidas",
        "partes-correo",
        "convertir-markdown-html",
    ]),
    ("Archivos y PDF", [
        "combinar-pdfs",
        "marca-agua",
        "extraer-texto-pdf-ocr",
        "herramienta-renombra-archivo",
        "organizador-archivos",
        "convertir-videos",
    ]),
    ("Tiempo y hábitos", [
        "cuenta-tiempo-atras",
        "pomodoro",
        "reloj-alarma",
        "reloj-digital",
        "rastreador-habitos-diarios",
        "lista-to-do",
    ]),
    ("Visión por computador", [
        "detector-cara-opencv",
        "sistema-reconocimiento-facial",
    ]),
    ("Correo", [
        "enviar-correo-csv",
    ]),
]

TITULOS = {
    "adivina-numero": "Adivina el número",
    "ahorcado": "El ahorcado",
    "piedra-papel-tijera": "Piedra, papel o tijera",
    "dados-aleatorios": "Dados aleatorios",
    "patron-triangulo": "Patrón triángulo",
    "patron-triangulo-invertido": "Patrón triángulo invertido",
    "patron-rombo": "Patrón rombo",
    "calculadora": "Calculadora",
    "calculadora-indice-masa-corporal": "Calculadora de IMC",
    "calculadora-propina": "Calculadora de propina",
    "convertidor-moneda": "Convertidor de moneda",
    "corta-url": "Acortador de URLs",
    "generador-contraseñas": "Generador de contraseñas",
    "generador-chiste-random": "Generador de chistes",
    "historias-divertidas": "Historias divertidas",
    "partes-correo": "Partes de un correo",
    "convertir-markdown-html": "Markdown a HTML",
    "combinar-pdfs": "Combinar PDFs",
    "marca-agua": "Marca de agua",
    "extraer-texto-pdf-ocr": "OCR sobre PDF",
    "herramienta-renombra-archivo": "Renombrador de archivos",
    "organizador-archivos": "Organizador de archivos",
    "convertir-videos": "Convertidor de vídeos",
    "cuenta-tiempo-atras": "Cuenta atrás",
    "pomodoro": "Pomodoro",
    "reloj-alarma": "Reloj alarma",
    "reloj-digital": "Reloj digital",
    "rastreador-habitos-diarios": "Rastreador de hábitos",
    "lista-to-do": "Lista de tareas",
    "detector-cara-opencv": "Detector de caras",
    "sistema-reconocimiento-facial": "Reconocimiento facial",
    "enviar-correo-csv": "Envío de correos desde CSV",
}


def archivo_principal(slug):
    """Devuelve el .py principal de la carpeta del ejercicio."""
    carpeta = RAIZ / slug
    python = sorted(carpeta.glob("*.py"))
    if not python:
        raise SystemExit(f"Sin archivos .py en {slug}")
    esperado = slug.replace("-", "_") + ".py"
    for archivo in python:
        if archivo.name == esperado:
            return archivo
    return max(python, key=lambda p: len(p.read_text(encoding="utf-8")))


def extrae_descripcion(texto):
    """Primer docstring del archivo, como párrafo limpio."""
    match = re.search(r'"""\s*(.*?)\s*"""', texto, re.S)
    if not match:
        return ""
    lineas = [linea.strip() for linea in match.group(1).splitlines() if linea.strip()]
    return " ".join(lineas)


def escapa_html(texto):
    return (
        texto.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def lee_ejercicios():
    """Devuelve (categorias, plana): categorias con sus ejercicios y la
    lista plana (para navegación anterior/siguiente)."""
    categorias = []
    plana = []
    numero = 0
    for nombre_cat, slogs in CATEGORIAS:
        items = []
        for slug in slogs:
            numero += 1
            archivo = archivo_principal(slug)
            codigo = archivo.read_text(encoding="utf-8")
            ejercicio = {
                "numero": numero,
                "slug": slug,
                "titulo": TITULOS.get(slug, slug.replace("-", " ").title()),
                "archivo": f"{slug}/{archivo.name}",
                "nombre": archivo.name,
                "descripcion": extrae_descripcion(codigo),
                "codigo": codigo,
            }
            items.append(ejercicio)
            plana.append(ejercicio)
        categorias.append((nombre_cat, items))
    return categorias, plana


def cabecera(rel, titulo, descripcion):
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="{escapa_html(descripcion)}">
  <title>{escapa_html(titulo)}</title>
  <link rel="icon" type="image/svg+xml" href="{rel}favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="{rel}favicon-32.png">
  <link rel="apple-touch-icon" href="{rel}favicon-180.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{rel}styles.css">
  <script src="{rel}app.js" defer></script>
</head>
<body>"""


def nav(rel):
    return f"""  <header class="nav">
    <a class="nav-word" href="{rel}index.html">Pythoncises</a>
    <nav aria-label="Principal">
      <ul class="nav-links">
        <li><a href="{rel}index.html#indice">Índice</a></li>
        <li><a href="{rel}index.html#licencia">Licencia</a></li>
      </ul>
    </nav>
  </header>"""


def pie():
    return """  <footer class="footer">
    <p>&copy; Pythoncises - 2026</p>
  </footer>
</body>
</html>
"""


def fila_indice(ejercicio):
    num = f"{ejercicio['numero']:02d}"
    busqueda = " ".join([
        ejercicio["titulo"],
        ejercicio["descripcion"],
        ejercicio["slug"],
        ejercicio["archivo"],
    ]).lower()
    return f"""      <article class="ejercicio" data-busqueda="{escapa_html(busqueda)}">
        <span class="ejercicio-num" aria-hidden="true">{num}</span>
        <div class="ejercicio-info">
          <h3 class="ejercicio-titulo"><a href="ejercicios/{escapa_html(ejercicio['slug'])}.html">{escapa_html(ejercicio['titulo'])}</a></h3>
          <p class="ejercicio-desc">{escapa_html(ejercicio['descripcion'])}</p>
        </div>
      </article>"""


def genera_indice(categorias, total):
    secciones = []
    for nombre_cat, items in categorias:
        filas = "\n".join(fila_indice(e) for e in items)
        secciones.append(f"""    <section class="categoria" aria-labelledby="cat-{escapa_html(nombre_cat.lower().replace(' ', '-'))}">
      <h2 class="categoria-nombre" id="cat-{escapa_html(nombre_cat.lower().replace(' ', '-'))}">{escapa_html(nombre_cat)}</h2>
{filas}
    </section>""")
    return f"""{cabecera("", "Pythoncises", "Índice de ejercicios de Python: verlos, copiarlos y descargarlos.")}
{nav("")}
  <main>
    <section class="intro" aria-labelledby="intro-titulo">
      <p class="intro-label">Índice</p>
      <h1 class="intro-title" id="intro-titulo">Ejercicios de Python.</h1>
      <p class="intro-copy">Verlos, copiarlos, descargarlos. Cada ejercicio en su propia página.</p>
      <div class="buscar">
        <label for="buscar">Buscar</label>
        <input id="buscar" type="search" placeholder="ahorcado, pdf, rombo…" autocomplete="off" spellcheck="false">
      </div>
    </section>

    <section class="indice" id="indice" aria-label="Índice de ejercicios">
{chr(10).join(secciones)}
      <p class="sin-resultados" id="sin-resultados" hidden>Ningún ejercicio coincide con la búsqueda.</p>
    </section>

    <section class="licencia" id="licencia" aria-labelledby="licencia-titulo">
      <h2 class="licencia-titulo" id="licencia-titulo">Licencia</h2>
      <p>El repositorio está publicado bajo la licencia MIT. Los ejercicios pueden usarse, copiarse y modificarse libremente.</p>
    </section>
  </main>
{pie()}"""


def pagina_ejercicio(ejercicio, anterior, siguiente):
    meta = " · ".join([
        ejercicio["categoria"],
        f"{ejercicio['numero']:02d}",
        ejercicio["nombre"],
    ])
    nav_previo = f'<a class="anterior" href="{anterior["slug"]}.html">← {escapa_html(anterior["titulo"])}</a>' if anterior else ""
    nav_siguiente = f'<a class="siguiente" href="{siguiente["slug"]}.html">{escapa_html(siguiente["titulo"])} →</a>' if siguiente else ""
    return f"""{cabecera("../", f"Pythoncises · {ejercicio['titulo']}", ejercicio['descripcion'])}
{nav("../")}
  <main class="detalle">
    <a class="detalle-volver" href="../index.html#indice">← Índice</a>
    <p class="detalle-meta">{escapa_html(meta)}</p>
    <h1 class="detalle-titulo">{escapa_html(ejercicio['titulo'])}</h1>
    <p class="detalle-desc">{escapa_html(ejercicio['descripcion'])}</p>
    <div class="detalle-acciones">
      <button class="btn" type="button" data-accion="copiar">Copiar</button>
      <button class="btn" type="button" data-accion="descargar" data-nombre="{escapa_html(ejercicio['nombre'])}">Descargar</button>
    </div>
    <p class="codigo-archivo">{escapa_html(ejercicio['archivo'])}</p>
    <pre><code>{escapa_html(ejercicio['codigo'])}</code></pre>
    <nav class="detalle-nav" aria-label="Navegación entre ejercicios">
      {nav_previo}
      {nav_siguiente}
    </nav>
  </main>
{pie()}"""


def main():
    categorias, plana = lee_ejercicios()
    # Añadir la categoría a cada ejercicio para la meta del detalle
    por_slug = {}
    for nombre_cat, items in categorias:
        for e in items:
            e["categoria"] = nombre_cat
            por_slug[e["slug"]] = e

    (RAIZ / "index.html").write_text(genera_indice(categorias, len(plana)), encoding="utf-8")

    SALIDA.mkdir(exist_ok=True)
    for indice, ejercicio in enumerate(plana):
        anterior = plana[indice - 1] if indice > 0 else None
        siguiente = plana[indice + 1] if indice < len(plana) - 1 else None
        (SALIDA / f"{ejercicio['slug']}.html").write_text(
            pagina_ejercicio(ejercicio, anterior, siguiente), encoding="utf-8"
        )

    print(f"index.html + {len(plana)} páginas en ejercicios/ generados.")


if __name__ == "__main__":
    main()
