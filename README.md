# AlertaU - Sistema de Predicción del Riesgo de Desaprobación Recurrente
### Universidad Nacional de San Martín (UNSM)

**AlertaU** es una aplicación web desarrollada en **Django** orientada al seguimiento académico temprano y a la predicción del riesgo de desaprobación recurrente en estudiantes universitarios de la **Universidad Nacional de San Martín (UNSM)**.

El sistema integra el modelo de Machine Learning semisupervisado **ST-LR (Self-Training Logistic Regression)** de la investigación de Tesis Riva, evaluando 20 variables académicas (periodos t0 y t1) bajo un umbral de decisión calibrado al **30.0%** y con fines formativos y preventivos no sancionadores.

---

## Paleta de Colores e Identidad Institucional

Inspirada en la identidad visual de la UNSM:
- **Verde principal institucional:** `#0c9b43` (títulos destacados, botones principales, énfasis)
- **Verde suave:** `#66c28a` (detalles y bordes activos)
- **Verde muy claro / Fondo suave:** `#eef8f1` y `#f4fbf6`
- **Blanco:** `#ffffff` (color predominante de fondo y tarjetas)
- **Gris suave:** `#e5e7eb` y `#f3f4f6` (bordes, fondos secundarios, tablas limpias)
- **Texto principal:** `#1f2937`
- **Espacio para Logo UNSM:** Contenedor oficial y placeholder `[Logo UNSM]` en el navbar superior, pantalla de login, portada y reportes, listo para ser reemplazado o renderizado directamente con la imagen institucional.

---

## Estructura de Páginas Implementadas

1. **Página de Inicio / Portada (`/`):**
   - Nombre: **AlertaU**
   - Subtítulo: *Sistema inteligente para la predicción del riesgo de desaprobación recurrente*
   - Propósito institucional, pilares de detección temprana, espacio para el logo de la UNSM.
   - Botones de acceso: *Iniciar sesión*, *Ir al sistema*, *Ver información*.

2. **Página de Inicio de Sesión (`/login/`):**
   - Diseño limpio y sobrio en fondo blanco con detalles verdes.
   - Campos de usuario y contraseña institucional.
   - Mensaje breve de privacidad y espacio para el logo de la UNSM.

3. **Dashboard Principal (`/dashboard/`):**
   - Resumen métrico:
     - Total de estudiantes evaluados.
     - Estudiantes en Alto Riesgo (rojo suave / `#fde8e8`).
     - Estudiantes en Riesgo Moderado (amarillo suave / `#fff9db`).
     - Estudiantes en Bajo Riesgo (verde suave / `#e8f5e9`).
     - Última fecha de actualización.
   - Barra comparativa y gráfica de distribución de riesgo.
   - Tabla de últimas evaluaciones registradas con accesos directos.

4. **Página de Predicción Individual (`/prediccion/individual/`):**
   - Formulario estructurado para las 20 variables académicas:
     - Identificación y confirmación de elegibilidad (antecedente de curso desaprobado pendiente).
     - Cursos en t0 y t1, aprobados, desaprobados y retirados.
     - Calificaciones: Media simple, GPA semestral y GPA acumulado (escala vigesimal 0 a 20).
     - Créditos aprobados y totales en t0 y t1.
     - Factores críticos: matrículas repetidas en t1, desaprobaciones en historial y cursos pendientes al corte.
   - Botones demo para autocompletar con un clic: *Alto Riesgo*, *Riesgo Moderado*, *Bajo Riesgo*.
   - Botón: **Predecir Riesgo**.

5. **Página de Resultado de Predicción (`/prediccion/resultado/<id>/`):**
   - Identificación del estudiante y periodo.
   - Nivel de riesgo detectado con tarjetas visuales limpias (Verde suave, Amarillo suave, Rojo suave).
   - Probabilidad estimada por el modelo ST-LR (ej. 94.73%, 45.2%, etc.) frente al umbral del 30.0%.
   - Mensaje interpretativo claro y factores determinantes destacados.
   - Recomendaciones específicas de tutoría y nivelación para la UNSM.
   - Botones para volver, exportar/imprimir o auditar los 20 factores.

6. **Página de Historial de Predicciones (`/historial/`):**
   - Tabla ordenada con: ID estudiante, fecha, resultado de riesgo, probabilidad, observación y opción de ver detalle.
   - Filtros de búsqueda por código/nombre, nivel de riesgo y periodo académico.
   - Paginación integrada y botón para **Exportar a CSV**.

7. **Página de Reportes (`/reportes/`):**
   - Filtro por periodo académico (ej. 2024-II, 2025-I, Todos).
   - Resumen estadístico y porcentual por categoría de vulnerabilidad.
   - Proporción comparativa con barra de progreso consolidada.
   - Tabla de cohortes y botón de impresión / descarga de reporte.

8. **Módulos Adicionales:**
   - **Carga de Datos (`/carga-masiva/`):** Procesamiento de archivos CSV por lotes y descarga de plantilla estándar.
   - **Glosario y Ayuda (`/ayuda/`):** Definición operativa de periodos t0 y t1, glosario de variables y lineamientos éticos no sancionadores.

---

## Organización del Proyecto

```text
AlertaU/
├── alerta_u/                  # Configuración principal de Django
│   ├── settings.py            # Apps, localización (es-pe), estáticos, autenticación
│   ├── urls.py                # Rutas maestras del proyecto
│   └── wsgi.py
├── alertau_app/               # Aplicación AlertaU
│   ├── models.py              # Modelos Estudiante y PrediccionRiesgo
│   ├── views.py               # Vistas de todas las páginas del sistema
│   ├── forms.py               # Formulario de predicción individual
│   ├── urls.py                # Rutas internas
│   ├── ml_service.py          # Servicio de inferencia semisupervisada ST-LR
│   ├── tests.py               # Suite de pruebas automatizadas (100% aprobadas)
│   ├── admin.py               # Panel administrativo de Django
│   └── management/commands/
│       └── seed_data.py       # Población de usuario admin y casos demo
├── ST_LR/                     # Artefactos del modelo ML de Tesis Riva
│   ├── artefactos/            # modelo_final.joblib, preprocesador_V2.joblib, configs
│   └── inferencia_django.py   # Script de referencia de inferencia
├── templates/alertau/         # Plantillas HTML con herencia base
│   ├── base.html              # Layout institucional, navbar con Logo UNSM y footer
│   ├── inicio.html            # Portada principal
│   ├── login.html             # Acceso institucional
│   ├── dashboard.html         # Panel de control y métricas
│   ├── prediccion_form.html   # Formulario de 20 variables
│   ├── prediccion_resultado.html # Diagnóstico y recomendaciones
│   ├── historial.html         # Registro histórico con filtros
│   ├── detalle.html           # Auditoría de factores evaluados
│   ├── reportes.html          # Reportes y filtros por periodo
│   ├── carga_masiva.html      # Subida por lote en CSV
│   └── ayuda.html             # Glosario t0/t1 y pautas metodológicas
├── static/
│   ├── css/custom.css         # Paleta institucional UNSM, tipografía y tarjetas
│   ├── js/main.js             # Interactividad y autocarga de casos demo
│   └── img/logo_unsm.png      # Logo oficial de la UNSM
└── manage.py
```

---

## Ejecución y Acceso Local

1. **Migraciones y datos iniciales (ya configurados):**
   ```bash
   python manage.py migrate
   python manage.py seed_data
   ```

2. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   Abra en su navegador: **http://127.0.0.1:8000/**

3. **Credenciales de Acceso Demo:**
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`
