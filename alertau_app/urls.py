from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('prediccion/individual/', views.prediccion_individual_view, name='prediccion_individual'),
    path('prediccion/resultado/<int:pk>/', views.resultado_prediccion_view, name='resultado_prediccion'),
    path('prediccion/detalle/<int:pk>/', views.detalle_prediccion_view, name='detalle_prediccion'),
    path('historial/', views.historial_view, name='historial'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('exportar/csv/', views.exportar_csv_view, name='exportar_csv'),
    path('carga-masiva/', views.carga_masiva_view, name='carga_masiva'),
    path('descargar-plantilla/', views.descargar_plantilla_csv_view, name='descargar_plantilla'),
    path('ayuda/', views.ayuda_view, name='ayuda'),
]
