from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date


class Position(models.Model):
    job = models.CharField(max_length=100, unique=True, verbose_name='Cargo', null=True,  # Temporalmente nullable
    blank=True)

    class Meta:
        verbose_name = 'Cargo'  # Singular
        verbose_name_plural = 'Cargos'
    def __str__(self):
        return self.job



class WorkPlace(models.Model):
    work_place = models.CharField(max_length=200, verbose_name='Nombre de Faena', help_text='Ingrese el nombre de la faena')
    contract_number = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="número de contrato", unique=True,
                                          help_text='Ingrese número de contrato si corresponde',  null=True,  # ← Agregar esto
    blank=True)

    class Meta:
        verbose_name = 'Centro de Trabajo'
        verbose_name_plural = 'Centros de Trabajo'

    def __str__(self):
        return f'{self.work_place} - {self.contract_number}'



STATUS_CHOICE = (
    ('Activo', "Activo"),
    ('Desvinculado', "Desvinculado"),
    ('En_Proceso', "En Proceso de Contratación")
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
ESTADO_CIVIL = [
    ('casado', 'Casado'),
    ('soltero', 'Soltero'),
    ('separado', 'Separado'),
    ('viudo', 'Viudo')
]


class Employee(models.Model):
    # Datos personales
    name = models.CharField(max_length=100, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    id_card = models.CharField(max_length=10, verbose_name='Cédula de identidad', unique=True)
    birth_date = models.DateField(verbose_name='Fecha Nacimiento')
    #Contacto
    phone = PhoneNumberField(unique=True, verbose_name='Número de teléfono', region='CL', null=True, blank=True)
    mail = models.EmailField(unique=True)
    city = models.CharField(verbose_name='Ciudad', help_text='Ciudad del trabajador')
    address = models.CharField(max_length=200, verbose_name="Dirección", help_text="Dirección del trabajador")
    # Info Familiar
    children = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)],
                                   verbose_name='Cantidad de hijos')
    marital_status = models.CharField(choices=ESTADO_CIVIL, null=True, blank=True, verbose_name='Estado Civil')
    picture = models.ImageField(upload_to='upload/%d%m%Y')
    age = models.PositiveIntegerField(verbose_name='Edad', editable=False)

    @property
    def calcular_edad(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

    @property
    def calcular_antiguedad(self):
        """Calcula la antigüedad detallada en años, meses y días"""
        if self.entry_date:
            today = date.today()

            # Si el empleado está desvinculado, usar la fecha de salida
            fecha_fin = self.end_date if self.status == 'Desvinculado' and self.end_date else today

            # Calcular años
            años = fecha_fin.year - self.entry_date.year

            # Ajustar si no ha llegado el mes/día de aniversario
            if (fecha_fin.month, fecha_fin.day) < (self.entry_date.month, self.entry_date.day):
                años -= 1

            # Calcular meses restantes
            meses = fecha_fin.month - self.entry_date.month
            if fecha_fin.day < self.entry_date.day:
                meses -= 1

            if meses < 0:
                meses += 12

            # Calcular días restantes
            if fecha_fin.day >= self.entry_date.day:
                dias = fecha_fin.day - self.entry_date.day
            else:
                # Calcular días del mes anterior
                if fecha_fin.month == 1:
                    mes_anterior = 12
                    año_anterior = fecha_fin.year - 1
                else:
                    mes_anterior = fecha_fin.month - 1
                    año_anterior = fecha_fin.year

                # Días en el mes anterior
                from calendar import monthrange
                dias_mes_anterior = monthrange(año_anterior, mes_anterior)[1]
                dias = dias_mes_anterior - self.entry_date.day + fecha_fin.day

            return {
                'años': años,
                'meses': meses,
                'dias': dias,
                'total_dias': (fecha_fin - self.entry_date).days
            }
        return None

    @property
    def antiguedad_texto(self):
        """Devuelve la antigüedad en formato de texto legible"""
        antiguedad = self.calcular_antiguedad
        if antiguedad:
            años = antiguedad['años']
            meses = antiguedad['meses']
            dias = antiguedad['dias']

            partes = []
            if años > 0:
                partes.append(f"{años} año{'s' if años != 1 else ''}")
            if meses > 0:
                partes.append(f"{meses} mes{'es' if meses != 1 else ''}")
            if dias > 0:
                partes.append(f"{dias} día{'s' if dias != 1 else ''}")

            resultado = ", ".join(partes) if partes else "0 días"

            # Agregar estado si está desvinculado
            if self.status == 'Desvinculado':
                resultado += " (al momento de la desvinculación)"

            return resultado
        return "Sin fecha de ingreso"

    @property
    def años_antiguedad(self):
        """Devuelve solo los años de antigüedad (útil para cálculos)"""
        antiguedad = self.calcular_antiguedad
        return antiguedad['años'] if antiguedad else 0

    # datos laborales
    job = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Cargo')
    work_place = models.ForeignKey(
        WorkPlace,
        verbose_name='Lugar de Trabajo',
        on_delete=models.CASCADE,
        related_name='employees'
    )

    contract_number = models.IntegerField(verbose_name='Número de contrato')
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

    class Meta:
        verbose_name_plural = "Trabajadores"
        verbose_name = "Trabajador"

    def save(self, *args, **kwargs):
        # Calcular edad automáticamente antes de guardar
        self.age = self.calcular_edad

        # Asignar número de contrato si tiene lugar de trabajo
        if self.work_place:
            self.contract_number = self.work_place.contract_number

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.last_name}'

