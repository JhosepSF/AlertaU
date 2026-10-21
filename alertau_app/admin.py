from django.contrib import admin
from .models import Estudiante, PrediccionRiesgo

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'apellidos', 'nombres', 'facultad', 'escuela', 'semestre_ingreso')
    search_fields = ('codigo', 'nombres', 'apellidos')
    list_filter = ('facultad', 'escuela', 'semestre_ingreso')

@admin.register(PrediccionRiesgo)
class PrediccionRiesgoAdmin(admin.ModelAdmin):
    list_display = ('codigo_estudiante', 'nombre_referencial', 'periodo_corte', 'nivel_riesgo', 'probabilidad_porcentaje', 'fecha_registro')
    list_filter = ('nivel_riesgo', 'periodo_corte', 'elegible_confirmado')
    search_fields = ('codigo_estudiante', 'nombre_referencial')
    readonly_fields = ('fecha_registro', 'probabilidad', 'clase_predicha', 'umbral_usado', 'nivel_riesgo')
