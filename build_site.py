#!/usr/bin/env python3
"""Genera index.html a partir de las carpetas de ejercicios.

Uso:  python3 build_site.py

Lee cada ejercicio (el archivo .py principal de su carpeta), extrae la
descripción de su docstring y genera el sitio estático con el código
incrustado (para copiar y descargar sin servidor).
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

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


def escapa_codigo(texto):
    """El código va dentro de <script type="text/plain">: solo hay que
    neutralizar la secuencia de cierre.</script>."""
    return texto.replace("</script", "<\\/script")


def escapa_html(texto):
    return (
        texto.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def lee_ejercicios():
    """Devuelve [(categoria, [ejercicio, ...]), ...] con slug, titulo,
    archivo, descripcion y codigo."""
    resultado = []
    numero = 0
    for categoria, slogs in CATEGORIAS:
        items = []
        for slug in slogs:
            numero += 1
            archivo = archivo_principal(slug)
            codigo = archivo.read_text(encoding="utf-8")
            items.append({
                "numero": numero,
                "slug": slug,
                "titulo": TITULOS.get(slug, slug.replace("-", " ").title()),
                "archivo": f"{slug}/{archivo.name}",
                "nombre": archivo.name,
                "descripcion": extrae_descripcion(codigo),
                "codigo": codigo,
            })
        resultado.append((categoria, items))
    return resultado


def fila_ejercicio(ejercicio):
    num = f"{ejercicio['numero']:02d}"
    slug = ejercicio["slug"]
    busqueda = " ".join([
        ejercicio["titulo"],
        ejercicio["descripcion"],
        slug,
        ejercicio["archivo"],
    ]).lower()
    return f"""        <article class="ejercicio" data-slug="{escapa_html(slug)}" data-nombre="{escapa_html(ejercicio['nombre'])}" data-busqueda="{escapa_html(busqueda)}">
          <div class="ejercicio-fila">
            <span class="ejercicio-num" aria-hidden="true">{num}</span>
            <div class="ejercicio-info">
              <h4 class="ejercicio-titulo">{escapa_html(ejercicio['titulo'])}</h4>
              <p class="ejercicio-desc">{escapa_html(ejercicio['descripcion'])}</p>
              <div class="ejercicio-acciones">
                <button class="btn" type="button" data-accion="ver" aria-expanded="false" aria-controls="codigo-{escapa_html(slug)}">Ver código</button>
                <button class="btn" type="button" data-accion="copiar">Copiar</button>
                <button class="btn" type="button" data-accion="descargar">Descargar</button>
              </div>
            </div>
          </div>
          <div class="ejercicio-codigo" id="codigo-{escapa_html(slug)}" hidden>
            <p class="codigo-archivo">{escapa_html(ejercicio['archivo'])}</p>
            <pre><code></code></pre>
          </div>
        </article>"""


def seccion_categoria(categoria, ejercicios):
    filas = "\n".join(fila_ejercicio(e) for e in ejercicios)
    return f"""      <section class="categoria" aria-labelledby="cat-{escapa_html(categoria.lower().replace(' ', '-'))}">
        <h3 class="categoria-nombre" id="cat-{escapa_html(categoria.lower().replace(' ', '-'))}">
          {escapa_html(categoria)}
          <span class="categoria-conteo">{len(ejercicios)}</span>
        </h3>
{filas}
      </section>"""


def bloques_codigo(ejercicios):
    bloques = []
    for categoria, items in ejercicios:
        for ejercicio in items:
            bloques.append(
                f'<script type="text/plain" id="src-{escapa_html(ejercicio["slug"])}">\n'
                f'{escapa_codigo(ejercicio["codigo"])}\n'
                f"</script>"
            )
    return "\n".join(bloques)


def genera_html(ejercicios):
    total = sum(len(items) for _, items in ejercicios)
    secciones = "\n".join(seccion_categoria(c, i) for c, i in ejercicios)
    codigos = bloques_codigo(ejercicios)
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="Índice de {total} ejercicios de Python: verlos, copiarlos y descargarlos.">
  <title>Pythoncises · {total} ejercicios de Python</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,400;6..72,600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="nav-mast">
    <p class="mast-line">web-pythoncises · índice de ejercicios · 2026</p>
    <h1 class="mast-name">Pythoncises</h1>
    <nav class="mast-nav" aria-label="Principal">
      <ul>
        <li><a href="#como-usar">Cómo usar</a></li>
        <li><a href="#indice">Índice</a></li>
        <li><a href="#licencia">Licencia</a></li>
      </ul>
    </nav>
    <hr class="mast-rule" aria-hidden="true">
  </header>

  <main>
    <section class="intro" aria-labelledby="intro-titulo">
      <h2 class="intro-title" id="intro-titulo">{total} programas de Python.</h2>
      <p class="intro-copy">Verlos, copiarlos, descargarlos. Cada ejercicio es un archivo, cada archivo con su propósito.</p>
      <div class="buscar">
        <label class="buscar-label" for="buscar">Buscar</label>
        <input id="buscar" type="search" placeholder="ahorcado, pdf, rombo…" autocomplete="off" spellcheck="false">
        <span class="buscar-conteo" id="buscar-conteo" aria-live="polite">{total} ejercicios</span>
      </div>
    </section>

    <section class="como-usar" id="como-usar" aria-labelledby="como-usar-titulo">
      <h2 class="como-usar-titulo" id="como-usar-titulo">Cómo usar</h2>
      <ol class="usos">
        <li>
          <span class="uso-verbo">Ver</span>
          <p>«Ver código» abre el archivo en la página, sin salir de ella.</p>
        </li>
        <li>
          <span class="uso-verbo">Copiar</span>
          <p>Un clic deja el código completo en el portapapeles.</p>
        </li>
        <li>
          <span class="uso-verbo">Descargar</span>
          <p>Guarda el archivo .py tal cual está en el repositorio.</p>
        </li>
      </ol>
    </section>

    <section class="indice" id="indice" aria-labelledby="indice-titulo">
      <h2 class="indice-titulo" id="indice-titulo">Índice</h2>
{secciones}
      <p class="sin-resultados" id="sin-resultados" hidden>Ningún ejercicio coincide con la búsqueda.</p>
    </section>

    <section class="licencia" id="licencia" aria-labelledby="licencia-titulo">
      <h2 class="licencia-titulo" id="licencia-titulo">Licencia</h2>
      <p>El repositorio está publicado bajo la licencia MIT. Los ejercicios pueden usarse, copiarse y modificarse libremente.</p>
    </section>
  </main>

  <footer class="foot-dense">
    <p>web-pythoncises · {total} ejercicios de Python · licencia MIT · construido sin frameworks.</p>
  </footer>

{codigos}
  <script>
    (function () {{
      "use strict";

      var filas = Array.prototype.slice.call(document.querySelectorAll(".ejercicio"));
      var categorias = Array.prototype.slice.call(document.querySelectorAll(".categoria"));
      var input = document.getElementById("buscar");
      var conteo = document.getElementById("buscar-conteo");
      var sinResultados = document.getElementById("sin-resultados");

      function normaliza(texto) {{
        return texto.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
      }}

      function codigoDe(boton) {{
        var ficha = boton.closest(".ejercicio");
        var fuente = document.getElementById("src-" + ficha.dataset.slug);
        return fuente.textContent.replace(/^\\n/, "").replace(/\\s+$/, "");
      }}

      function filtrar() {{
        var termino = normaliza(input.value.trim());
        var visibles = 0;
        filas.forEach(function (fila) {{
          var coincide = !termino || normaliza(fila.dataset.busqueda).indexOf(termino) !== -1;
          fila.hidden = !coincide;
          if (coincide) visibles++;
        }});
        categorias.forEach(function (cat) {{
          cat.hidden = cat.querySelectorAll(".ejercicio:not([hidden])").length === 0;
        }});
        conteo.textContent = visibles + " de " + filas.length + (visibles === 1 ? " ejercicio" : " ejercicios");
        sinResultados.hidden = visibles !== 0;
      }}

      input.addEventListener("input", filtrar);

      document.addEventListener("click", function (evento) {{
        var boton = evento.target.closest("button[data-accion]");
        if (!boton) return;

        var ficha = boton.closest(".ejercicio");
        var panel = ficha.querySelector(".ejercicio-codigo");
        var codigo = codigoDe(boton);
        var accion = boton.dataset.accion;

        if (accion === "ver") {{
          var abierto = !panel.hidden;
          if (abierto) {{
            panel.hidden = true;
            boton.setAttribute("aria-expanded", "false");
            boton.textContent = "Ver código";
          }} else {{
            panel.querySelector("code").textContent = codigo;
            panel.hidden = false;
            boton.setAttribute("aria-expanded", "true");
            boton.textContent = "Ocultar código";
          }}
        }} else if (accion === "copiar") {{
          copiar(boton, codigo);
        }} else if (accion === "descargar") {{
          descargar(ficha.dataset.nombre, codigo);
        }}
      }});

      function copiar(boton, texto) {{
        var hecho = function () {{
          var original = boton.textContent;
          boton.textContent = "Copiado ✓";
          boton.dataset.copiado = "true";
          setTimeout(function () {{
            boton.textContent = original;
            delete boton.dataset.copiado;
          }}, 2500);
        }};
        if (navigator.clipboard && window.isSecureContext) {{
          navigator.clipboard.writeText(texto).then(hecho, function () {{ copiarPorSeleccion(texto, hecho); }});
        }} else {{
          copiarPorSeleccion(texto, hecho);
        }}
      }}

      function copiarPorSeleccion(texto, hecho) {{
        var area = document.createElement("textarea");
        area.value = texto;
        area.setAttribute("readonly", "");
        area.style.position = "fixed";
        area.style.opacity = "0";
        document.body.appendChild(area);
        area.select();
        try {{ document.execCommand("copy"); hecho(); }} catch (error) {{ /* sin acción */ }}
        document.body.removeChild(area);
      }}

      function descargar(nombre, texto) {{
        var blob = new Blob([texto], {{ type: "text/plain;charset=utf-8" }});
        var url = URL.createObjectURL(blob);
        var enlace = document.createElement("a");
        enlace.href = url;
        enlace.download = nombre;
        document.body.appendChild(enlace);
        enlace.click();
        document.body.removeChild(enlace);
        URL.revokeObjectURL(url);
      }}
    }})();
  </script>
</body>
</html>
"""


def main():
    ejercicios = lee_ejercicios()
    html = genera_html(ejercicios)
    (RAIZ / "index.html").write_text(html, encoding="utf-8")
    total = sum(len(items) for _, items in ejercicios)
    print(f"index.html generado con {total} ejercicios.")


if __name__ == "__main__":
    main()
