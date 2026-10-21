from django import forms
from .models import PrediccionRiesgo

class PrediccionIndividualForm(forms.ModelForm):
    elegible_confirmado = forms.BooleanField(
        required=True,
        initial=True,
        label="Elegibilidad confirmada",
        help_text="El estudiante cuenta con antecedentes de al menos una asignatura desaprobada y pendiente al corte.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = PrediccionRiesgo
        fields = [
            'codigo_estudiante', 'nombre_referencial', 'periodo_corte', 'elegible_confirmado',
            # Asignaturas
            'cursos_t0', 'cursos_t1', 'aprobados_t0', 'aprobados_t1',
            'desaprobados_t0', 'desaprobados_t1', 'retirados_t0',
            # Calificaciones
            'media_simple_t0', 'media_simple_t1', 'gpa_t0', 'gpa_t1',
            'gpa_acumulado_t0', 'gpa_acumulado_t1',
            # Créditos
            'creditos_aprobados_t0', 'creditos_aprobados_t1',
            'creditos_totales_t0', 'creditos_totales_t1',
            # Factores críticos
            'matriculas_repetidas_t1', 'desaprobaciones_historial',
            'n_cursos_pendientes_al_corte'
        ]
        widgets = {
            'codigo_estudiante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. 73491028 o 20210045',
                'required': True
            }),
            'nombre_referencial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre o referencia académica'
            }),
            'periodo_corte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2025-I'
            }),
            # Asignaturas
            'cursos_t0': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'cursos_t1': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'aprobados_t0': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'aprobados_t1': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'desaprobados_t0': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'desaprobados_t1': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'retirados_t0': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),

            # Calificaciones (0-20)
            'media_simple_t0': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '20'}),
            'media_simple_t1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '20'}),
            'gpa_t0': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),
            'gpa_t1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),
            'gpa_acumulado_t0': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),
            'gpa_acumulado_t1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),

            # Créditos
            'creditos_aprobados_t0': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'creditos_aprobados_t1': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'creditos_totales_t0': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'creditos_totales_t1': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),

            # Historial y pendientes
            'matriculas_repetidas_t1': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'desaprobaciones_historial': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'n_cursos_pendientes_al_corte': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
        }

    def clean_codigo_estudiante(self):
        codigo = self.cleaned_data.get('codigo_estudiante', '').strip().upper()
        if not codigo:
            raise forms.ValidationError("El código del estudiante es obligatorio.")
        return codigo

    def clean(self):
        cleaned_data = super().clean()
        elegible = cleaned_data.get('elegible_confirmado')
        if not elegible:
            self.add_error('elegible_confirmado', 'Debe confirmar que el estudiante cumple los criterios de elegibilidad.')
        return cleaned_data
