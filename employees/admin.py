from django.contrib import admin
from .models import WorkPlace, Employee, Position


# Cambiar títulos principales del admin
admin.site.site_header = 'Administración de Personal'
admin.site.site_title = 'Admin Personal'
admin.site.index_title = 'Panel de Control'

# Tus admin classes...


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Información del Cargo', {
            'fields': ('job',)
        }),
    )
    list_display = ('job',)
    search_fields = ('job',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🧍 Datos Personales', {
            'fields': ('name', 'last_name', 'id_card', 'birth_date', 'age', 'picture')
        }),
        ('🏠 Información de Contacto', {
            'fields': ('address','city', 'mail', 'phone')
        }),
        ('👶 Datos Familiares', {
            'fields': ('children','marital_status')
        }),
        (' Datos Laborales',{
            'fields': ('job','work_place','entry_date', 'contract_type','end_date', 'reason_for_leaving','status')
        })
    )

    list_display = ('name', 'last_name', 'id_card', 'work_place', 'status','get_antiguedad_completa')
    list_filter = ('status', 'work_place', 'contract_type')
    search_fields = ('name', 'last_name', 'id_card')
    readonly_fields = ('age', 'contract_number', 'antiguedad_texto')
    list_editable = ('status',)

    def get_antiguedad_completa(self, obj):
        """Muestra la antigüedad completa en el list_display"""
        return obj.antiguedad_texto

    get_antiguedad_completa.short_description = 'Antigüedad'
    get_antiguedad_completa.admin_order_field = 'entry_date'


@admin.register(WorkPlace)
class WorkPlaceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Faenas',{
            'fields':('work_place', 'contract_number')
        }),
    )
