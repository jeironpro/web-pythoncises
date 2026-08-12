(function () {
  "use strict";

  /* Índice: filtro de búsqueda por nombre y descripción */
  var input = document.getElementById("buscar");

  if (input) {
    var filas = Array.prototype.slice.call(document.querySelectorAll(".ejercicio"));
    var categorias = Array.prototype.slice.call(document.querySelectorAll(".categoria"));
    var vacio = document.getElementById("sin-resultados");

    function normaliza(texto) {
      return texto.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }

    input.addEventListener("input", function () {
      var termino = normaliza(input.value.trim());
      var visibles = 0;

      filas.forEach(function (fila) {
        var coincide = !termino || normaliza(fila.dataset.busqueda).indexOf(termino) !== -1;
        fila.hidden = !coincide;
        if (coincide) visibles++;
      });

      categorias.forEach(function (categoria) {
        categoria.hidden = categoria.querySelectorAll(".ejercicio:not([hidden])").length === 0;
      });

      if (vacio) vacio.hidden = visibles !== 0;
    });
  }

  /* Detalle: copiar y descargar */
  var codigo = document.querySelector(".detalle pre code");

  document.addEventListener("click", function (evento) {
    var boton = evento.target.closest("button[data-accion]");
    if (!boton || !codigo) return;

    var texto = codigo.textContent.replace(/\s+$/, "");
    var accion = boton.dataset.accion;

    if (accion === "copiar") {
      copiar(boton, texto);
    } else if (accion === "descargar") {
      descargar(boton.dataset.nombre, texto);
    }
  });

  function copiar(boton, texto) {
    var hecho = function () {
      var original = boton.textContent;
      boton.textContent = "Copiado ✓";
      boton.dataset.copiado = "true";
      setTimeout(function () {
        boton.textContent = original;
        delete boton.dataset.copiado;
      }, 2500);
    };

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(texto).then(hecho, function () {
        copiarPorSeleccion(texto, hecho);
      });
    } else {
      copiarPorSeleccion(texto, hecho);
    }
  }

  function copiarPorSeleccion(texto, hecho) {
    var area = document.createElement("textarea");
    area.value = texto;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    try {
      document.execCommand("copy");
      hecho();
    } catch (error) {
      /* sin acción */
    }
    document.body.removeChild(area);
  }

  function descargar(nombre, texto) {
    var blob = new Blob([texto], { type: "text/plain;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var enlace = document.createElement("a");
    enlace.href = url;
    enlace.download = nombre;
    document.body.appendChild(enlace);
    enlace.click();
    document.body.removeChild(enlace);
    URL.revokeObjectURL(url);
  }
})();
