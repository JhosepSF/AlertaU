from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from alertau_app.models import Estudiante, PrediccionRiesgo
from alertau_app.ml_service import predictor_servicio

class Command(BaseCommand):
    help = 'Inicializa usuario administrador y datos iniciales de prueba para AlertaU'

    def handle(self, *args, **kwargs):
        self.stdout.write("Configurando usuario administrador institucional...")
        user, created = User.objects.get_or_create(username='admin')
        if created:
            user.set_password('admin123')
            user.first_name = 'Tutor Académico'
            user.last_name = 'UNSM'
            user.email = 'tutor.alertau@unsm.edu.pe'
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS("Usuario 'admin' creado exitosamente (clave: admin123)."))
        else:
            user.set_password('admin123')
            user.save()
            self.stdout.write("Usuario 'admin' ya existía; credenciales actualizadas.")

        self.stdout.write("Registrando estudiantes y predicciones de demostración...")

        casos = [
            {
                'codigo': '20210089',
                'nombre': 'Carlos E. Rios Flores',
                'periodo': '2025-I',
                'factores': {
                    "cursos_t0": 6.0, "cursos_t1": 6.0, "aprobados_t0": 4.0, "aprobados_t1": 4.0,
                    "desaprobados_t0": 2.0, "desaprobados_t1": 2.0, "retirados_t0": 0.0,
                    "media_simple_t0": 12.0, "media_simple_t1": 12.0, "gpa_t0": 12.0, "gpa_t1": 12.0,
                    "gpa_acumulado_t0": 12.0, "gpa_acumulado_t1": 12.0, "creditos_aprobados_t0": 16.0,
                    "creditos_aprobados_t1": 16.0, "creditos_totales_t0": 22.0, "creditos_totales_t1": 22.0,
                    "matriculas_repetidas_t1": 1.0, "desaprobaciones_historial": 2.0, "n_cursos_pendientes_al_corte": 2.0
                }
            },
            {
                'codigo': '20200312',
                'nombre': 'Luis A. Pinedo Vela',
                'periodo': '2025-I',
                'factores': {
                    "cursos_t0": 6.0, "cursos_t1": 6.0, "aprobados_t0": 3.0, "aprobados_t1": 2.0,
                    "desaprobados_t0": 3.0, "desaprobados_t1": 4.0, "retirados_t0": 0.0,
                    "media_simple_t0": 10.5, "media_simple_t1": 9.8, "gpa_t0": 10.8, "gpa_t1": 9.5,
                    "gpa_acumulado_t0": 11.2, "gpa_acumulado_t1": 10.8, "creditos_aprobados_t0": 12.0,
                    "creditos_aprobados_t1": 8.0, "creditos_totales_t0": 22.0, "creditos_totales_t1": 22.0,
                    "matriculas_repetidas_t1": 2.0, "desaprobaciones_historial": 5.0, "n_cursos_pendientes_al_corte": 4.0
                }
            },
            {
                'codigo': '20220145',
                'nombre': 'María V. Gómez Salas',
                'periodo': '2025-I',
                'factores': {
                    "cursos_t0": 6.0, "cursos_t1": 5.0, "aprobados_t0": 5.0, "aprobados_t1": 4.0,
                    "desaprobados_t0": 1.0, "desaprobados_t1": 1.0, "retirados_t0": 0.0,
                    "media_simple_t0": 13.5, "media_simple_t1": 12.8, "gpa_t0": 13.2, "gpa_t1": 12.5,
                    "gpa_acumulado_t0": 13.0, "gpa_acumulado_t1": 12.8, "creditos_aprobados_t0": 18.0,
                    "creditos_aprobados_t1": 15.0, "creditos_totales_t0": 22.0, "creditos_totales_t1": 19.0,
                    "matriculas_repetidas_t1": 1.0, "desaprobaciones_historial": 1.0, "n_cursos_pendientes_al_corte": 1.0
                }
            },
            {
                'codigo': '20230211',
                'nombre': 'Jorge S. Tapia Ruiz',
                'periodo': '2025-I',
                'factores': {
                    "cursos_t0": 6.0, "cursos_t1": 6.0, "aprobados_t0": 6.0, "aprobados_t1": 5.0,
                    "desaprobados_t0": 0.0, "desaprobados_t1": 1.0, "retirados_t0": 0.0,
                    "media_simple_t0": 15.2, "media_simple_t1": 14.8, "gpa_t0": 15.0, "gpa_t1": 14.5,
                    "gpa_acumulado_t0": 14.8, "gpa_acumulado_t1": 14.6, "creditos_aprobados_t0": 22.0,
                    "creditos_aprobados_t1": 18.0, "creditos_totales_t0": 22.0, "creditos_totales_t1": 22.0,
                    "matriculas_repetidas_t1": 0.0, "desaprobaciones_historial": 1.0, "n_cursos_pendientes_al_corte": 1.0
                }
            },
            {
                'codigo': '20210452',
                'nombre': 'Ana Paula Reátegui T.',
                'periodo': '2024-II',
                'factores': {
                    "cursos_t0": 5.0, "cursos_t1": 6.0, "aprobados_t0": 3.0, "aprobados_t1": 3.0,
                    "desaprobados_t0": 2.0, "desaprobados_t1": 3.0, "retirados_t0": 0.0,
                    "media_simple_t0": 11.5, "media_simple_t1": 10.8, "gpa_t0": 11.2, "gpa_t1": 10.6,
                    "gpa_acumulado_t0": 11.8, "gpa_acumulado_t1": 11.3, "creditos_aprobados_t0": 12.0,
                    "creditos_aprobados_t1": 11.0, "creditos_totales_t0": 19.0, "creditos_totales_t1": 22.0,
                    "matriculas_repetidas_t1": 1.0, "desaprobaciones_historial": 3.0, "n_cursos_pendientes_al_corte": 3.0
                }
            },
            {
                'codigo': '20220980',
                'nombre': 'Fernando Díaz Saavedra',
                'periodo': '2024-II',
                'factores': {
                    "cursos_t0": 6.0, "cursos_t1": 6.0, "aprobados_t0": 5.0, "aprobados_t1": 5.0,
                    "desaprobados_t0": 1.0, "desaprobados_t1": 1.0, "retirados_t0": 0.0,
                    "media_simple_t0": 14.0, "media_simple_t1": 13.9, "gpa_t0": 13.8, "gpa_t1": 13.6,
                    "gpa_acumulado_t0": 13.7, "gpa_acumulado_t1": 13.6, "creditos_aprobados_t0": 18.0,
                    "creditos_aprobados_t1": 18.0, "creditos_totales_t0": 22.0, "creditos_totales_t1": 22.0,
                    "matriculas_repetidas_t1": 0.0, "desaprobaciones_historial": 1.0, "n_cursos_pendientes_al_corte": 1.0
                }
            }
        ]

        for caso in casos:
            est, _ = Estudiante.objects.get_or_create(
                codigo=caso['codigo'],
                defaults={
                    'nombres': caso['nombre'].split()[0],
                    'apellidos': " ".join(caso['nombre'].split()[1:]),
                    'facultad': 'Facultad de Ingeniería de Sistemas e Informática',
                    'escuela': 'Ingeniería de Sistemas',
                    'semestre_ingreso': '2021-I'
                }
            )

            res = predictor_servicio.predecir(caso['factores'], elegible_confirmado=True)

            PrediccionRiesgo.objects.update_or_create(
                codigo_estudiante=caso['codigo'],
                periodo_corte=caso['periodo'],
                defaults={
                    'estudiante': est,
                    'nombre_referencial': caso['nombre'],
                    'cursos_t0': caso['factores']['cursos_t0'],
                    'cursos_t1': caso['factores']['cursos_t1'],
                    'aprobados_t0': caso['factores']['aprobados_t0'],
                    'aprobados_t1': caso['factores']['aprobados_t1'],
                    'desaprobados_t0': caso['factores']['desaprobados_t0'],
                    'desaprobados_t1': caso['factores']['desaprobados_t1'],
                    'retirados_t0': caso['factores']['retirados_t0'],
                    'media_simple_t0': caso['factores']['media_simple_t0'],
                    'media_simple_t1': caso['factores']['media_simple_t1'],
                    'gpa_t0': caso['factores']['gpa_t0'],
                    'gpa_t1': caso['factores']['gpa_t1'],
                    'gpa_acumulado_t0': caso['factores']['gpa_acumulado_t0'],
                    'gpa_acumulado_t1': caso['factores']['gpa_acumulado_t1'],
                    'creditos_aprobados_t0': caso['factores']['creditos_aprobados_t0'],
                    'creditos_aprobados_t1': caso['factores']['creditos_aprobados_t1'],
                    'creditos_totales_t0': caso['factores']['creditos_totales_t0'],
                    'creditos_totales_t1': caso['factores']['creditos_totales_t1'],
                    'matriculas_repetidas_t1': caso['factores']['matriculas_repetidas_t1'],
                    'desaprobaciones_historial': caso['factores']['desaprobaciones_historial'],
                    'n_cursos_pendientes_al_corte': caso['factores']['n_cursos_pendientes_al_corte'],
                    'elegible_confirmado': True,
                    'probabilidad': res['probabilidad'],
                    'clase_predicha': res['clase_predicha'],
                    'umbral_usado': res['umbral'],
                    'nivel_riesgo': res['nivel_codigo'],
                    'observacion': res['diagnostico'],
                    'recomendacion': "\n".join(res['recomendaciones']),
                    'usuario_evaluador': user
                }
            )

        self.stdout.write(self.style.SUCCESS(f"Se crearon/actualizaron {len(casos)} casos demostrativos con éxito."))
