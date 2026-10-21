from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from alertau_app.models import Estudiante, PrediccionRiesgo
from alertau_app.ml_service import predictor_servicio

class AlertaUTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='evaluador_test',
            password='Password123!',
            first_name='Evaluador',
            last_name='UNSM'
        )
        self.estudiante = Estudiante.objects.create(
            codigo='20210089',
            nombres='Carlos',
            apellidos='Silva',
            facultad='Facultad de Ingeniería de Sistemas e Informática',
            escuela='Ingeniería de Sistemas',
            semestre_ingreso='2021-I'
        )

    def test_inicio_view(self):
        """Verifica que la portada pública responda 200 y contenga los textos de AlertaU."""
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AlertaU')
        self.assertContains(response, 'Universidad Nacional de San Martín')
        self.assertContains(response, 'Logo UNSM')

    def test_login_view_get(self):
        """Verifica la página de login institucional."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Iniciar Sesión')
        self.assertContains(response, 'Usuario Institucional')
        self.assertContains(response, 'Logo UNSM')

    def test_login_successful(self):
        """Prueba autenticación válida y redirección a dashboard."""
        response = self.client.post(reverse('login'), {
            'username': 'evaluador_test',
            'password': 'Password123!'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_dashboard_authenticated(self):
        """Verifica que el dashboard renderice las métricas cuando está autenticado."""
        self.client.login(username='evaluador_test', password='Password123!')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Panel de Control Académico')
        self.assertContains(response, 'Total Estudiantes Evaluados')
        self.assertContains(response, 'Alto Riesgo')
        self.assertContains(response, 'Riesgo Moderado')
        self.assertContains(response, 'Bajo Riesgo')

    def test_prediccion_ml_inferencia_y_guardado(self):
        """Prueba el flujo completo de inferencia con el modelo ST-LR y guardado en BD."""
        self.client.login(username='evaluador_test', password='Password123!')
        
        datos_formulario = {
            'codigo_estudiante': '20210089',
            'nombre_referencial': 'Estudiante Test Inferencia',
            'periodo_corte': '2025-I',
            'elegible_confirmado': 'on',
            'cursos_t0': 6.0,
            'cursos_t1': 6.0,
            'aprobados_t0': 4.0,
            'aprobados_t1': 4.0,
            'desaprobados_t0': 2.0,
            'desaprobados_t1': 2.0,
            'retirados_t0': 0.0,
            'media_simple_t0': 12.0,
            'media_simple_t1': 12.0,
            'gpa_t0': 12.0,
            'gpa_t1': 12.0,
            'gpa_acumulado_t0': 12.0,
            'gpa_acumulado_t1': 12.0,
            'creditos_aprobados_t0': 16.0,
            'creditos_aprobados_t1': 16.0,
            'creditos_totales_t0': 22.0,
            'creditos_totales_t1': 22.0,
            'matriculas_repetidas_t1': 1.0,
            'desaprobaciones_historial': 2.0,
            'n_cursos_pendientes_al_corte': 2.0,
        }

        response = self.client.post(reverse('prediccion_individual'), datos_formulario)
        
        # Debe redirigir al resultado
        self.assertEqual(response.status_code, 302)
        pred = PrediccionRiesgo.objects.latest('id')
        self.assertEqual(pred.codigo_estudiante, '20210089')
        self.assertGreater(pred.probabilidad, 0.5)
        self.assertEqual(pred.nivel_riesgo, 'ALTO')
        self.assertEqual(pred.umbral_usado, 0.3)

        # Verificar la página de resultado
        res_page = self.client.get(reverse('resultado_prediccion', kwargs={'pk': pred.pk}))
        self.assertEqual(res_page.status_code, 200)
        self.assertContains(res_page, 'NIVEL: ALTO')
        self.assertContains(res_page, 'Recomendaciones Institucionales (UNSM)')

    def test_historial_y_reportes(self):
        """Verifica la visualización de la tabla de historial y los reportes."""
        self.client.login(username='evaluador_test', password='Password123!')
        
        # Historial
        resp_hist = self.client.get(reverse('historial'))
        self.assertEqual(resp_hist.status_code, 200)
        self.assertContains(resp_hist, 'Historial de Predicciones de Riesgo')

        # Reportes
        resp_rep = self.client.get(reverse('reportes'))
        self.assertEqual(resp_rep.status_code, 200)
        self.assertContains(resp_rep, 'Reporte Consolidado de Riesgo Académico')

        # Exportar CSV
        resp_csv = self.client.get(reverse('exportar_csv'))
        self.assertEqual(resp_csv.status_code, 200)
        self.assertEqual(resp_csv['Content-Type'], 'text/csv; charset=utf-8')
