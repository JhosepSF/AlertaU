import csv
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count, Q, Max

from .models import Estudiante, PrediccionRiesgo
from .forms import PrediccionIndividualForm
from .ml_service import predictor_servicio

def inicio_view(request):
    """Página de inicio / Portada pública del sistema AlertaU."""
    total_evaluaciones = PrediccionRiesgo.objects.count()
    return render(request, 'alertau/inicio.html', {
        'total_evaluaciones': total_evaluaciones,
    })

def login_view(request):
    """Página de inicio de sesión institucional."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido(a) a AlertaU, {user.first_name or user.username}.")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Credenciales incorrectas. Verifique su usuario y contraseña institucional.")
    else:
        form = AuthenticationForm()

    return render(request, 'alertau/login.html', {'form': form})

def logout_view(request):
    """Cierre de sesión."""
    logout(request)
    messages.info(request, "Ha cerrado sesión de forma segura.")
    return redirect('inicio')

@login_required
def dashboard_view(request):
    """Dashboard principal con tarjetas de resumen, gráficos y últimas evaluaciones."""
    total_estudiantes = PrediccionRiesgo.objects.values('codigo_estudiante').distinct().count()
    total_evaluaciones = PrediccionRiesgo.objects.count()

    alto_riesgo_count = PrediccionRiesgo.objects.filter(nivel_riesgo='ALTO').count()
    moderado_riesgo_count = PrediccionRiesgo.objects.filter(nivel_riesgo='MODERADO').count()
    bajo_riesgo_count = PrediccionRiesgo.objects.filter(nivel_riesgo='BAJO').count()

    ultima_actualizacion = PrediccionRiesgo.objects.aggregate(Max('fecha_registro'))['fecha_registro__max']

    ultimas_predicciones = PrediccionRiesgo.objects.all().order_by('-fecha_registro')[:8]

    # Cálculos porcentuales
    total_base = total_evaluaciones if total_evaluaciones > 0 else 1
    pct_alto = round((alto_riesgo_count / total_base) * 100, 1)
    pct_moderado = round((moderado_riesgo_count / total_base) * 100, 1)
    pct_bajo = round((bajo_riesgo_count / total_base) * 100, 1)

    context = {
        'total_estudiantes': total_estudiantes,
        'total_evaluaciones': total_evaluaciones,
        'alto_riesgo_count': alto_riesgo_count,
        'moderado_riesgo_count': moderado_riesgo_count,
        'bajo_riesgo_count': bajo_riesgo_count,
        'pct_alto': pct_alto,
        'pct_moderado': pct_moderado,
        'pct_bajo': pct_bajo,
        'ultima_actualizacion': ultima_actualizacion,
        'ultimas_predicciones': ultimas_predicciones,
        'modelo_info': {
            'umbral': predictor_servicio.threshold,
            'is_loaded': predictor_servicio.is_loaded,
        }
    }
    return render(request, 'alertau/dashboard.html', context)

@login_required
def prediccion_individual_view(request):
    """Página del formulario de predicción individual."""
    if request.method == 'POST':
        form = PrediccionIndividualForm(request.POST)
        if form.is_valid():
            prediccion = form.save(commit=False)
            prediccion.usuario_evaluador = request.user

            # Ejecutar inferencia a través del servicio ML
            factores = prediccion.to_factors_dict()
            resultado = predictor_servicio.predecir(factores, elegible_confirmado=prediccion.elegible_confirmado)

            # Asignar resultados calculados
            prediccion.probabilidad = resultado['probabilidad']
            prediccion.clase_predicha = resultado['clase_predicha']
            prediccion.umbral_usado = resultado['umbral']
            prediccion.nivel_riesgo = resultado['nivel_codigo']
            prediccion.observacion = resultado['diagnostico']
            prediccion.recomendacion = "\n".join(f"• {r}" for r in resultado['recomendaciones'])

            # Vincular o crear ficha de estudiante si no existe
            estudiante, _ = Estudiante.objects.get_or_create(
                codigo=prediccion.codigo_estudiante,
                defaults={
                    'nombres': prediccion.nombre_referencial or "Estudiante",
                    'apellidos': "UNSM"
                }
            )
            prediccion.estudiante = estudiante
            prediccion.save()

            messages.success(request, f"Predicción generada con éxito para el estudiante {prediccion.codigo_estudiante}.")
            return redirect('resultado_prediccion', pk=prediccion.pk)
        else:
            messages.error(request, "Por favor corrija los errores indicados en el formulario.")
    else:
        # Valores iniciales por defecto inspirados en el ejemplo del contrato
        form = PrediccionIndividualForm(initial={
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
            'elegible_confirmado': True
        })

    return render(request, 'alertau/prediccion_form.html', {'form': form})

@login_required
def resultado_prediccion_view(request, pk):
    """Página de resultado de predicción con diagnóstico interpretativo y recomendaciones."""
    prediccion = get_object_or_404(PrediccionRiesgo, pk=pk)

    # Interpretar de nuevo con el servicio para obtener desglose detallado
    factores = prediccion.to_factors_dict()
    resultado = predictor_servicio.predecir(factores, elegible_confirmado=prediccion.elegible_confirmado)

    context = {
        'prediccion': prediccion,
        'resultado': resultado,
        'factores': factores,
    }
    return render(request, 'alertau/prediccion_resultado.html', context)

@login_required
def historial_view(request):
    """Página de historial de predicciones con filtros y paginación."""
    query_codigo = request.GET.get('codigo', '').strip()
    filtro_riesgo = request.GET.get('riesgo', '').strip()
    filtro_periodo = request.GET.get('periodo', '').strip()

    predicciones = PrediccionRiesgo.objects.all().order_by('-fecha_registro')

    if query_codigo:
        predicciones = predicciones.filter(
            Q(codigo_estudiante__icontains=query_codigo) |
            Q(nombre_referencial__icontains=query_codigo)
        )

    if filtro_riesgo in ['ALTO', 'MODERADO', 'BAJO']:
        predicciones = predicciones.filter(nivel_riesgo=filtro_riesgo)

    if filtro_periodo:
        predicciones = predicciones.filter(periodo_corte=filtro_periodo)

    periodos_disponibles = PrediccionRiesgo.objects.values_list('periodo_corte', flat=True).distinct()

    paginator = Paginator(predicciones, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query_codigo': query_codigo,
        'filtro_riesgo': filtro_riesgo,
        'filtro_periodo': filtro_periodo,
        'periodos_disponibles': periodos_disponibles,
        'total_registros': predicciones.count(),
    }
    return render(request, 'alertau/historial.html', context)

@login_required
def detalle_prediccion_view(request, pk):
    """Visualización completa de los 20 factores evaluados en una predicción guardada."""
    prediccion = get_object_or_404(PrediccionRiesgo, pk=pk)
    factores = prediccion.to_factors_dict()
    resultado = predictor_servicio.predecir(factores, elegible_confirmado=prediccion.elegible_confirmado)

    return render(request, 'alertau/detalle.html', {
        'prediccion': prediccion,
        'resultado': resultado,
        'factores': factores
    })

@login_required
def reportes_view(request):
    """Página de reportes generales y filtrados por periodo académico."""
    periodo_seleccionado = request.GET.get('periodo', 'TODOS').strip()

    queryset = PrediccionRiesgo.objects.all()
    if periodo_seleccionado and periodo_seleccionado != 'TODOS':
        queryset = queryset.filter(periodo_corte=periodo_seleccionado)

    total = queryset.count()
    alto = queryset.filter(nivel_riesgo='ALTO').count()
    moderado = queryset.filter(nivel_riesgo='MODERADO').count()
    bajo = queryset.filter(nivel_riesgo='BAJO').count()

    base = total if total > 0 else 1
    pct_alto = round((alto / base) * 100, 1)
    pct_moderado = round((moderado / base) * 100, 1)
    pct_bajo = round((bajo / base) * 100, 1)

    periodos = PrediccionRiesgo.objects.values_list('periodo_corte', flat=True).distinct()

    # Últimos registros filtrados
    muestras = queryset.order_by('-fecha_registro')[:15]

    context = {
        'periodo_seleccionado': periodo_seleccionado,
        'periodos': periodos,
        'total': total,
        'alto': alto,
        'moderado': moderado,
        'bajo': bajo,
        'pct_alto': pct_alto,
        'pct_moderado': pct_moderado,
        'pct_bajo': pct_bajo,
        'muestras': muestras,
    }
    return render(request, 'alertau/reportes.html', context)

@login_required
def exportar_csv_view(request):
    """Exportación de predicciones a formato CSV."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="alertau_predicciones_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'

    # Añadir BOM para correcta visualización en Microsoft Excel
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow([
        'ID Estudiante', 'Nombre Referencial', 'Periodo Corte', 'Nivel de Riesgo',
        'Probabilidad (%)', 'Umbral', 'Fecha Evaluación', 'Cursos Pendientes',
        'Repetidas t1', 'GPA t1', 'GPA Acumulado t1'
    ])

    for p in PrediccionRiesgo.objects.all().order_by('-fecha_registro'):
        writer.writerow([
            p.codigo_estudiante,
            p.nombre_referencial,
            p.periodo_corte,
            p.nivel_riesgo,
            f"{p.probabilidad_porcentaje}%",
            p.umbral_usado,
            p.fecha_registro.strftime('%d/%m/%Y %H:%M'),
            p.n_cursos_pendientes_al_corte,
            p.matriculas_repetidas_t1,
            p.gpa_t1,
            p.gpa_acumulado_t1,
        ])

    return response

@login_required
def carga_masiva_view(request):
    """Página para carga masiva de datos y procesamiento de lotes académicos."""
    if request.method == 'POST' and request.FILES.get('archivo_csv'):
        archivo = request.FILES['archivo_csv']
        try:
            lineas = archivo.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(lineas)
            procesados = 0
            for row in reader:
                cod = row.get('codigo_estudiante', '').strip()
                if not cod:
                    continue
                # Parsear factores
                factores = {}
                for f in predictor_servicio.features:
                    factores[f] = float(row.get(f, 0.0))

                resultado = predictor_servicio.predecir(factores, elegible_confirmado=True)

                PrediccionRiesgo.objects.create(
                    codigo_estudiante=cod,
                    nombre_referencial=row.get('nombre_referencial', 'Estudiante Cargado'),
                    periodo_corte=row.get('periodo_corte', '2025-I'),
                    cursos_t0=factores.get('cursos_t0', 6.0),
                    cursos_t1=factores.get('cursos_t1', 6.0),
                    aprobados_t0=factores.get('aprobados_t0', 4.0),
                    aprobados_t1=factores.get('aprobados_t1', 4.0),
                    desaprobados_t0=factores.get('desaprobados_t0', 2.0),
                    desaprobados_t1=factores.get('desaprobados_t1', 2.0),
                    retirados_t0=factores.get('retirados_t0', 0.0),
                    media_simple_t0=factores.get('media_simple_t0', 12.0),
                    media_simple_t1=factores.get('media_simple_t1', 12.0),
                    gpa_t0=factores.get('gpa_t0', 12.0),
                    gpa_t1=factores.get('gpa_t1', 12.0),
                    gpa_acumulado_t0=factores.get('gpa_acumulado_t0', 12.0),
                    gpa_acumulado_t1=factores.get('gpa_acumulado_t1', 12.0),
                    creditos_aprobados_t0=factores.get('creditos_aprobados_t0', 16.0),
                    creditos_aprobados_t1=factores.get('creditos_aprobados_t1', 16.0),
                    creditos_totales_t0=factores.get('creditos_totales_t0', 22.0),
                    creditos_totales_t1=factores.get('creditos_totales_t1', 22.0),
                    matriculas_repetidas_t1=factores.get('matriculas_repetidas_t1', 1.0),
                    desaprobaciones_historial=factores.get('desaprobaciones_historial', 2.0),
                    n_cursos_pendientes_al_corte=factores.get('n_cursos_pendientes_al_corte', 2.0),
                    probabilidad=resultado['probabilidad'],
                    clase_predicha=resultado['clase_predicha'],
                    umbral_usado=resultado['umbral'],
                    nivel_riesgo=resultado['nivel_codigo'],
                    observacion=resultado['diagnostico'],
                    recomendacion="\n".join(resultado['recomendaciones']),
                    usuario_evaluador=request.user
                )
                procesados += 1

            messages.success(request, f"Se procesaron e infirieron con éxito {procesados} registros de estudiantes.")
            return redirect('historial')
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo CSV: {str(e)}")

    return render(request, 'alertau/carga_masiva.html')

@login_required
def descargar_plantilla_csv_view(request):
    """Descarga de plantilla CSV estandarizada para carga masiva."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="plantilla_carga_alertau.csv"'
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    cabeceras = ['codigo_estudiante', 'nombre_referencial', 'periodo_corte'] + predictor_servicio.features
    writer.writerow(cabeceras)

    # Fila de ejemplo 1
    writer.writerow([
        '20210089', 'García López, Juan', '2025-I',
        6.0, 6.0, 4.0, 4.0, 2.0, 2.0, 0.0,
        12.0, 12.0, 12.0, 12.0, 12.0, 12.0,
        16.0, 16.0, 22.0, 22.0, 1.0, 2.0, 2.0
    ])
    # Fila de ejemplo 2
    writer.writerow([
        '20220145', 'Paredes Rios, Maria', '2025-I',
        6.0, 6.0, 5.0, 5.0, 1.0, 1.0, 0.0,
        14.0, 13.5, 13.8, 13.2, 13.5, 13.4,
        18.0, 18.0, 21.0, 21.0, 0.0, 1.0, 1.0
    ])

    return response

@login_required
def ayuda_view(request):
    """Página de ayuda, glosario de variables t0/t1 y principios éticos del sistema."""
    return render(request, 'alertau/ayuda.html', {
        'threshold': predictor_servicio.threshold,
    })
