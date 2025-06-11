from django.contrib import admin
from .models import WorkPlace, Employee, Position, Region, City
from django.urls import reverse
from django.utils.html import format_html


# Cambiar títulos principales del admin
admin.site.site_header = 'Administración de Personal'
admin.site.site_title = 'Admin Personal'
admin.site.index_title = 'Panel de Control'

# Tus admin classes...

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Region',{
            'fields':('name',)
        }),
    )
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Ciudad',{
            'fields':('name', 'region')
        }),
    )

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Información del Cargo', {
            'fields': ('job',)
        }),
    )
    list_display = ('job',)
    search_fields = ('job',)


from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Employee, Region, City, Position, WorkPlace


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'id_card', 'status', 'photo_preview', 'tiene_usuario', 'crear_usuario_btn']
    list_filter = ['status', 'work_place']
    search_fields = ['name', 'last_name', 'id_card']

    # NUEVA FUNCIÓN: Mostrar miniatura de la foto
    def photo_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.picture.url
            )
        return "Sin foto"

    photo_preview.short_description = 'Foto'

    def tiene_usuario(self, obj):
        if obj.user:
            return "✅ Sí"
        return "❌ No"

    tiene_usuario.short_description = 'Tiene Usuario'

    def crear_usuario_btn(self, obj):
        if obj.user:
            url = reverse('ver_credenciales_empleado', args=[obj.id])
            return format_html('<a class="button" href="{}">Ver Credenciales</a>', url)
        if obj.status != 'Activo':
            return "No activo"

        url = reverse('crear_usuario_empleado', args=[obj.id])
        return format_html('<a class="button" href="{}">Crear Usuario</a>', url)

    crear_usuario_btn.short_description = 'Acción'
    crear_usuario_btn.allow_tags = True

@admin.register(WorkPlace)
class WorkPlaceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Faenas',{
            'fields':('work_place', 'contract_number', 'adc')
        }),
    )
