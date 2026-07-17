from django.urls import path
from . import views


urlpatterns = [
    path('crear-usuario/<int:employee_id>/', views.crear_usuario_empleado, name='crear_usuario_empleado'),
    path('ver-credenciales/<int:employee_id>/', views.ver_credenciales_empleado, name='ver_credenciales_empleado'),
    path('resetear-password/<int:employee_id>/', views.resetear_password_empleado, name='resetear_password_empleado'),
]
