from django.contrib import admin
from .models import WorkPlace, Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🧍 Datos Personales', {
            'fields': ('name', 'last_name', 'id_card', 'birth_date', 'picture')
        }),
        ('🏠 Información de Contacto', {
            'fields': ('address','city', 'mail', 'phone')
        }),
        ('👶 Datos Familiares', {
            'fields': ('children',)
        }),
        (' Datos Laborales',{
            'fields': ('work_place','entry_date', 'contract_type','end_date', 'reason_for_leaving','status')
        })
    )


    list_display = ('name', 'last_name', 'id_card', 'phone', 'work_place', 'entry_date', 'status')
    search_fields = ('last_name', 'id_card')
    list_editable = ('status',)
    list_filter = ('entry_date','contract_number')
    list_per_page = 20


@admin.register(WorkPlace)
class WorkPlaceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Faenas',{
            'fields':('work_place', 'contract_number')
        }),
    )
