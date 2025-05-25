from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class WorkPlace(models.Model):
    work_place = models.CharField(max_length=200, verbose_name='Nombre de Faena', help_text='Ingrese el nombre de la faena')
    contract_number = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="número de contrato", unique=True, help_text='Ingrese número de contrato si corresponde')

    def __str__(self):
        return f'{self.work_place} - {self.contract_number}'


STATUS_CHOICE = (
    ('Activo', "Activo"),
    ('Desvinculado', "Desvinculado")
)

EXIT_REASONS = [
        ('Renuncia', 'Renuncia voluntaria'),
        ('Termino_del_Plazo', 'Término de contrato'),
        ('Necesidades_empresa', 'Despido por necesidades de la empresa'),
        ('Abandono', 'Abandono del trabajo'),
        ('Inc_Grave', 'Despido por incumplimiento grave'),
        ('Mutuo_Acuerdo', 'Mutuo acuerdo'),
        ('Muerte', 'Muerte del trabajador'),
        ('Jubilado', 'Jubilación'),
    ]

CONTRACT_TYPE=[
    ('Plazo_Fijo', 'Plazo Fijo'),
    ('Indefinido', 'Indefinido')

]
class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    id_card = models.CharField(max_length=10, verbose_name='Cédula de identidad', unique=True)
    phone = PhoneNumberField(unique=True, verbose_name='Número de teléfono', region='CL', null=True, blank=True)
    mail = models.EmailField(unique=True)
    city = models.CharField(verbose_name='Ciudad', help_text='Ciudad del trabajador')
    birth_date = models.DateField(verbose_name='Fecha Nacimiento')
    address = models.CharField(max_length=200, verbose_name="Dirección", help_text="Dirección del trabajador")
    children = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)],verbose_name='Cantidad de hijos')
    picture = models.ImageField(upload_to='upload/%d%m%Y')

    # Lugar de trabajo
    work_place = models.ForeignKey(
        WorkPlace,
        verbose_name='Lugar de Trabajo',
        on_delete=models.CASCADE,
        related_name='employees'
    )

    contract_number = models.IntegerField(
        verbose_name='Número de contrato')
    status = models.CharField(choices=STATUS_CHOICE, verbose_name='Estado')

    entry_date = models.DateField(verbose_name='Fecha de Ingreso')
    contract_type = models.CharField(choices=CONTRACT_TYPE, verbose_name='Tipo de Contrato')
    end_date = models.DateField(verbose_name='Fecha de Salida', blank=True, null=True)


    reason_for_leaving = models.CharField(
        max_length=30,
        choices=EXIT_REASONS,
        verbose_name='Motivo de salida',
        null=True,
        blank=True
    )


    def save(self, *args, **kwargs):
        if self.work_place:
            self.contract_number = self.work_place.contract_number
        super().save(*args, **kwargs)


