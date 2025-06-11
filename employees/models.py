from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from smart_selects.db_fields import ChainedForeignKey


class Region(models.Model):
    """Regiones de Chile"""
    name = models.CharField(max_length=100, verbose_name='Región', unique=True)


    class Meta:
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'


    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    """Ciudades y comunas"""
    name = models.CharField(max_length=100, verbose_name='Ciudad/Comuna')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Región')
    is_capital = models.BooleanField(default=False, verbose_name='Es capital regional')


    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        unique_together = ['name', 'region']
        ordering = ['region', 'name']

    def __str__(self):
        return f"{self.name}"


class EducationLevel(models.Model):
    """Niveles educacionales"""
    EDUCATION_CHOICES = [
        (1, 'Sin estudios'),
        (2, 'Básica incompleta'),
        (3, 'Básica completa'),
        (4, 'Media incompleta'),
        (5, 'Media completa'),
        (6, 'Técnica incompleta'),
        (7, 'Técnica completa'),
        (8, 'Universitaria incompleta'),
        (9, 'Universitaria completa'),
        (10, 'Postgrado'),
    ]

    level = models.PositiveSmallIntegerField(choices=EDUCATION_CHOICES, unique=True)
    name = models.CharField(max_length=50, verbose_name='Nivel educacional')
    years_study = models.PositiveSmallIntegerField(verbose_name='Años de estudio promedio')

    class Meta:
        verbose_name = 'Nivel Educacional'
        verbose_name_plural = 'Niveles Educacionales'
        ordering = ['level']

    def __str__(self):
        return self.name

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
                                          help_text='Ingrese número de contrato si corresponde',  null=True,
    blank=True)
    adc = models.CharField(max_length=150, verbose_name='Nombre ADC o líder del contrato')

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
    ('soltero', 'Soltero/a'),
    ('casado', 'Casado/a'),
    ('separado', 'Separado/a'),
    ('divorciado', 'Divorciado/a'),
    ('viudo', 'Viudo/a'),
    ('union_civil', 'Unión Civil'),
]


class Employee(models.Model):
    # Datos personales
    name = models.CharField(max_length=100, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    id_card = models.CharField(max_length=10, verbose_name='Cédula de identidad', unique=True)
    birth_date = models.DateField(verbose_name='Fecha Nacimiento')
    #Contacto
    phone = PhoneNumberField(unique=True, verbose_name='Número de teléfono', region='CL', null=True, blank=True)
    mail = models.EmailField(unique=True, verbose_name='E-mail')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Región de origen')
    city = ChainedForeignKey(
        City,
        chained_field="region",
        chained_model_field="region",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name = "Ciudad"
    )
    address = models.CharField(max_length=200, verbose_name="Dirección", help_text="Dirección del trabajador")
    # Info Familiar
    children = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)],
                                   verbose_name='Cantidad de hijos')
    marital_status = models.CharField(choices=ESTADO_CIVIL, null=True, blank=True, verbose_name='Estado Civil')
    contacto_emergencia = models.CharField(max_length=100, verbose_name="nombre contacto emergencia:",
                                           help_text="En caso de emergencia, llamar a:", blank= True, null=True)
    numero_emergencia = PhoneNumberField(unique=True, verbose_name="Teléfono emergencia", blank=True, null=True)
    picture = models.ImageField(upload_to='upload/%d%m%Y')

    # Conexion con Django User
    user = models.OneToOneField(
        User,
        on_delete= models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Usuario del sistema'
    )

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
    job = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Cargo')
    work_place = models.ForeignKey(
        WorkPlace,
        verbose_name='Lugar de Trabajo',
        on_delete=models.CASCADE,
        related_name='employees'
    )

    boss = models.BooleanField(verbose_name="Es jefatura")
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

