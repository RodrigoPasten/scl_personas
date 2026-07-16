from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Employee


# Títulos del panel administrativo
admin.site.site_header = 'Administración de Personal'
admin.site.site_title = 'Admin Personal'
admin.site.index_title = 'Panel de Control'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'last_name',
        'id_card',
        'email',
        'notificaciones_email',
        'tiene_usuario',
        'crear_usuario_btn',
    ]

    list_filter = [
        'email_notifications_enabled',
    ]

    search_fields = [
        'name',
        'last_name',
        'id_card',
        'email',
    ]

    readonly_fields = [
        'email_consent_at',
        'email_consent_revoked_at',
    ]

    fieldsets = (
        ('Datos del trabajador', {
            'fields': (
                'name',
                'last_name',
                'id_card',
                'email',
                'user',
            )
        }),
        ('Notificaciones por correo', {
            'fields': (
                'email_notifications_enabled',
                'email_consent_at',
                'email_consent_revoked_at',
            ),
            'description': (
                'Las notificaciones deben ser autorizadas expresamente '
                'por el trabajador.'
            ),
        }),
    )

    @admin.display(
        boolean=True,
        description='Notificaciones por email',
    )
    def notificaciones_email(self, obj):
        return obj.email_notifications_enabled

    @admin.display(
        boolean=True,
        description='Tiene usuario',
    )
    def tiene_usuario(self, obj):
        return obj.user is not None

    @admin.display(description='Acción')
    def crear_usuario_btn(self, obj):
        if obj.user:
            url = reverse(
                'ver_credenciales_empleado',
                args=[obj.id],
            )

            return format_html(
                '<a class="button" href="{}">Ver credenciales</a>',
                url,
            )

        url = reverse(
            'crear_usuario_empleado',
            args=[obj.id],
        )

        return format_html(
            '<a class="button" href="{}">Crear usuario</a>',
            url,
        )