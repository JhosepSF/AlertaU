/**
 * AlertaU - JavaScript de apoyo interactivo
 */

document.addEventListener('DOMContentLoaded', function () {
  // Inicialización de tooltips si Bootstrap está presente
  if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }

  // Helper para autocompletar casos de prueba en el formulario de predicción individual
  const btnCaso1 = document.getElementById('btn-cargar-caso-1');
  const btnCaso2 = document.getElementById('btn-cargar-caso-2');
  const btnCaso3 = document.getElementById('btn-cargar-caso-3');

  function rellenarFormulario(data) {
    for (const [key, val] of Object.entries(data)) {
      const input = document.getElementById(`id_${key}`);
      if (input) {
        if (input.type === 'checkbox') {
          input.checked = Boolean(val);
        } else {
          input.value = val;
        }
        // Disparar evento change para reflejar visualmente
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }
  }

  // Ejemplo 1: Caso Ficticio con Alto Riesgo (del dataset ficticio de prueba de Tesis Riva)
  if (btnCaso1) {
    btnCaso1.addEventListener('click', function () {
      rellenarFormulario({
        'codigo_estudiante': '20210089',
        'nombre_referencial': 'Estudiante Ficticio 01 (Alto Riesgo)',
        'periodo_corte': '2025-I',
        'cursos_t0': 6,
        'cursos_t1': 6,
        'aprobados_t0': 4,
        'aprobados_t1': 4,
        'desaprobados_t0': 2,
        'desaprobados_t1': 2,
        'retirados_t0': 0,
        'media_simple_t0': 12.0,
        'media_simple_t1': 12.0,
        'gpa_t0': 12.0,
        'gpa_t1': 12.0,
        'gpa_acumulado_t0': 12.0,
        'gpa_acumulado_t1': 12.0,
        'creditos_aprobados_t0': 16,
        'creditos_aprobados_t1': 16,
        'creditos_totales_t0': 22,
        'creditos_totales_t1': 22,
        'matriculas_repetidas_t1': 1,
        'desaprobaciones_historial': 2,
        'n_cursos_pendientes_al_corte': 2,
        'elegible_confirmado': true
      });
    });
  }

  // Ejemplo 2: Caso Ficticio con Riesgo Moderado
  if (btnCaso2) {
    btnCaso2.addEventListener('click', function () {
      rellenarFormulario({
        'codigo_estudiante': '20220145',
        'nombre_referencial': 'Estudiante Ficticio 02 (Riesgo Moderado)',
        'periodo_corte': '2025-I',
        'cursos_t0': 6,
        'cursos_t1': 5,
        'aprobados_t0': 5,
        'aprobados_t1': 4,
        'desaprobados_t0': 1,
        'desaprobados_t1': 1,
        'retirados_t0': 0,
        'media_simple_t0': 13.5,
        'media_simple_t1': 12.8,
        'gpa_t0': 13.2,
        'gpa_t1': 12.5,
        'gpa_acumulado_t0': 13.0,
        'gpa_acumulado_t1': 12.8,
        'creditos_aprobados_t0': 18,
        'creditos_aprobados_t1': 15,
        'creditos_totales_t0': 22,
        'creditos_totales_t1': 19,
        'matriculas_repetidas_t1': 1,
        'desaprobaciones_historial': 1,
        'n_cursos_pendientes_al_corte': 1,
        'elegible_confirmado': true
      });
    });
  }

  // Ejemplo 3: Caso Ficticio con Bajo Riesgo
  if (btnCaso3) {
    btnCaso3.addEventListener('click', function () {
      rellenarFormulario({
        'codigo_estudiante': '20230211',
        'nombre_referencial': 'Estudiante Ficticio 03 (Bajo Riesgo)',
        'periodo_corte': '2025-I',
        'cursos_t0': 6,
        'cursos_t1': 6,
        'aprobados_t0': 6,
        'aprobados_t1': 5,
        'desaprobados_t0': 0,
        'desaprobados_t1': 1,
        'retirados_t0': 0,
        'media_simple_t0': 15.2,
        'media_simple_t1': 14.8,
        'gpa_t0': 15.0,
        'gpa_t1': 14.5,
        'gpa_acumulado_t0': 14.8,
        'gpa_acumulado_t1': 14.6,
        'creditos_aprobados_t0': 22,
        'creditos_aprobados_t1': 18,
        'creditos_totales_t0': 22,
        'creditos_totales_t1': 22,
        'matriculas_repetidas_t1': 0,
        'desaprobaciones_historial': 1,
        'n_cursos_pendientes_al_corte': 1,
        'elegible_confirmado': true
      });
    });
  }
});
