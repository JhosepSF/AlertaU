TESIS RIVA - PAQUETE DE IMPLEMENTACION DJANGO

Modelo elegido MANUALMENTE: ST-LR
No es una seleccion por las metricas del test; debe estar preseleccionado y documentado.

Archivos:
- artefactos/modelo_final.joblib: estimador semisupervisado entrenado
- artefactos/preprocesador_V2.joblib: imputacion y escalado entrenados SOLO con train
- artefactos/predictores_originales.json: lista ordenada de las 20 variables
- artefactos/mejor_configuracion_validacion.json: hiperparametros y umbral
- artefactos/config_inferencia.json: contrato de inferencia
- ejemplos/ejemplos_ficticios.json: DOS casos totalmente ficticios para probar la interfaz
- inferencia_django.py: referencia Python para integracion en el servidor
- sha256_archivos.json: integridad de archivos del paquete

FLUJO INFERENCIA:
1) Autenticar personal autorizado en Django y limitar acceso al sistema.
2) Verificar elegibilidad: antecedentes de asignaturas desaprobadas aun pendientes.
3) Generar SOLO factores historicos anteriores o iguales al semestre de corte.
4) Construir DataFrame de una fila respetando el orden 'features' de config_inferencia.json.
5) Transformar con preprocesador_V2.joblib sin hacer fit ni recalcular escalas.
6) Aplicar model.predict_proba(X_transformada), elegir columna classes_=1.
7) Usar threshold=0.300000, sin modificarlo segun resultados del test.
8) Mostrar probabilidad estimada, clase y advertencia de uso academico.

IMPORTANTE: No corresponde pedir al alumno que ingrese 'su riesgo' o etiqueta real.
La aplicacion necesita calcular las 20 variables desde historial academico confiable.
No inventar variables, ni asumir equivalencia de asignaturas no validada.
No mostrar probabilidades como garantias ni usar para sanciones.

DATOS Y SEGURIDAD:
Este ZIP no incluye notas reales, identificadores de alumnos, historiales de prueba,
ni etiquetas reservadas. Los ejemplos son ficticios, NO ejemplos del Test.
En produccion implementar permisos por rol, minimizacion de PII, cifrado,
HTTPS, auditoria de acceso y politica de retencion. Deshabilitar logs con datos sensibles.
Nunca cargar archivos joblib recibidos de fuentes no confiables.
Fijar versiones compatibles; probar inferencia en entorno destino.

LIMITACIONES:
La poblacion elegible, la calidad de las etiquetas y las equivalencias de cursos
requieren validacion institucional antes de despliegue real. Las probabilidades
pueden no estar calibradas. Una etiqueta 0 significa ausencia verificada del evento
bajo la definicion y seguimiento del estudio, no aprobacion futura garantizada.
No reentrenar ni usar Test para ajustar formularios o umbrales.
