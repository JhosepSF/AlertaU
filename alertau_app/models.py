from django.db import models
from django.contrib.auth.models import User

class Estudiante(models.Model):
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código de Estudiante")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    facultad = models.CharField(max_length=150, default="Facultad de Ingeniería de Sistemas e Informática", verbose_name="Facultad")
    escuela = models.CharField(max_length=150, default="Ingeniería de Sistemas", verbose_name="Escuela Profesional")
    semestre_ingreso = models.CharField(max_length=15, default="2022-I", verbose_name="Semestre de Ingreso")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.apellidos}, {self.nombres}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"


class PrediccionRiesgo(models.Model):
    NIVELES_RIESGO = [
        ('ALTO', 'Alto Riesgo'),
        ('MODERADO', 'Riesgo Moderado'),
        ('BAJO', 'Bajo Riesgo'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.SET_NULL, null=True, blank=True, related_name='predicciones')
    codigo_estudiante = models.CharField(max_length=20, verbose_name="Código del Estudiante")
    nombre_referencial = models.CharField(max_length=150, blank=True, default="", verbose_name="Nombre Referencial")
    periodo_corte = models.CharField(max_length=20, default="2025-I", verbose_name="Periodo de Corte (t1)")

    # 20 Variables del Contrato de Inferencia de Tesis Riva
    cursos_t0 = models.FloatField(default=6.0, verbose_name="N° cursos en t0 (periodo anterior)")
    cursos_t1 = models.FloatField(default=6.0, verbose_name="N° cursos en t1 (periodo de corte)")
    aprobados_t0 = models.FloatField(default=4.0, verbose_name="Cursos aprobados en t0")
    aprobados_t1 = models.FloatField(default=4.0, verbose_name="Cursos aprobados en t1")
    desaprobados_t0 = models.FloatField(default=2.0, verbose_name="Cursos desaprobados en t0")
    desaprobados_t1 = models.FloatField(default=2.0, verbose_name="Cursos desaprobados en t1")
    retirados_t0 = models.FloatField(default=0.0, verbose_name="Cursos retirados en t0")

    media_simple_t0 = models.FloatField(default=12.0, verbose_name="Media simple en t0 (0-20)")
    media_simple_t1 = models.FloatField(default=12.0, verbose_name="Media simple en t1 (0-20)")
    gpa_t0 = models.FloatField(default=12.0, verbose_name="GPA en t0 (0-20)")
    gpa_t1 = models.FloatField(default=12.0, verbose_name="GPA en t1 (0-20)")
    gpa_acumulado_t0 = models.FloatField(default=12.0, verbose_name="GPA acumulado al cierre de t0")
    gpa_acumulado_t1 = models.FloatField(default=12.0, verbose_name="GPA acumulado al cierre de t1")

    creditos_aprobados_t0 = models.FloatField(default=16.0, verbose_name="Créditos aprobados en t0")
    creditos_aprobados_t1 = models.FloatField(default=16.0, verbose_name="Créditos aprobados en t1")
    creditos_totales_t0 = models.FloatField(default=22.0, verbose_name="Créditos totales matriculados en t0")
    creditos_totales_t1 = models.FloatField(default=22.0, verbose_name="Créditos totales matriculados en t1")

    matriculas_repetidas_t1 = models.FloatField(default=1.0, verbose_name="Matrículas repetidas en t1 (2da o 3ra vez)")
    desaprobaciones_historial = models.FloatField(default=2.0, verbose_name="Desaprobaciones en historial académico")
    n_cursos_pendientes_al_corte = models.FloatField(default=2.0, verbose_name="N° cursos pendientes de subsanar al corte")

    # Inferencia y Diagnóstico
    elegible_confirmado = models.BooleanField(default=True, verbose_name="Elegibilidad confirmada")
    probabilidad = models.FloatField(default=0.0, verbose_name="Probabilidad de recurrencia (0.0 - 1.0)")
    clase_predicha = models.IntegerField(default=0, verbose_name="Clase predicha (0=Sin recurrencia, 1=Recurrencia)")
    umbral_usado = models.FloatField(default=0.30, verbose_name="Umbral de decisión (threshold)")
    nivel_riesgo = models.CharField(max_length=20, choices=NIVELES_RIESGO, default='BAJO', verbose_name="Nivel de Riesgo")
    observacion = models.TextField(blank=True, verbose_name="Observación diagnóstica")
    recomendacion = models.TextField(blank=True, verbose_name="Recomendación académica")

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Evaluación")
    usuario_evaluador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Evaluador")

    class Meta:
        verbose_name = "Predicción de Riesgo"
        verbose_name_plural = "Predicciones de Riesgo"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.codigo_estudiante} | {self.nivel_riesgo} ({self.probabilidad_porcentaje}%) - {self.fecha_registro.strftime('%d/%m/%Y %H:%M')}"

    @property
    def probabilidad_porcentaje(self):
        return round(self.probabilidad * 100, 2)

    @property
    def badge_css(self):
        if self.nivel_riesgo == 'ALTO':
            return 'danger'
        elif self.nivel_riesgo == 'MODERADO':
            return 'warning'
        return 'success'

    @property
    def badge_class_custom(self):
        if self.nivel_riesgo == 'ALTO':
            return 'risk-high'
        elif self.nivel_riesgo == 'MODERADO':
            return 'risk-moderate'
        return 'risk-low'

    def to_factors_dict(self):
        """Convierte los campos del modelo en el diccionario de entrada para el estimador ML."""
        return {
            "cursos_t0": float(self.cursos_t0),
            "cursos_t1": float(self.cursos_t1),
            "aprobados_t0": float(self.aprobados_t0),
            "aprobados_t1": float(self.aprobados_t1),
            "desaprobados_t0": float(self.desaprobados_t0),
            "desaprobados_t1": float(self.desaprobados_t1),
            "retirados_t0": float(self.retirados_t0),
            "media_simple_t0": float(self.media_simple_t0),
            "media_simple_t1": float(self.media_simple_t1),
            "gpa_t0": float(self.gpa_t0),
            "gpa_t1": float(self.gpa_t1),
            "gpa_acumulado_t0": float(self.gpa_acumulado_t0),
            "gpa_acumulado_t1": float(self.gpa_acumulado_t1),
            "creditos_aprobados_t0": float(self.creditos_aprobados_t0),
            "creditos_aprobados_t1": float(self.creditos_aprobados_t1),
            "creditos_totales_t0": float(self.creditos_totales_t0),
            "creditos_totales_t1": float(self.creditos_totales_t1),
            "matriculas_repetidas_t1": float(self.matriculas_repetidas_t1),
            "desaprobaciones_historial": float(self.desaprobaciones_historial),
            "n_cursos_pendientes_al_corte": float(self.n_cursos_pendientes_al_corte),
        }
