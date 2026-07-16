from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee',
        null=True,
        blank=True,
        verbose_name='Usuario del sistema',
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Nombres',
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name='Apellidos',
    )

    id_card = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='RUT',
        help_text='Ejemplo: 12.345.678-9',
    )

    email = models.EmailField(
        blank=True,
        verbose_name='Correo electrónico',
    )

    email_notifications_enabled = models.BooleanField(
        default=False,
        verbose_name='Autoriza notificaciones por correo',
        help_text=(
            'El trabajador autoriza recibir notificaciones cuando '
            'se publiquen nuevos contenidos en el portal.'
        ),
    )

    email_consent_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name='Fecha de autorización',
    )

    email_consent_revoked_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name='Fecha de retiro de autorización',
    )

    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'
        ordering = ['last_name', 'name']

    def clean(self):
        super().clean()

        if self.email_notifications_enabled and not self.email:
            raise ValidationError({
                'email': (
                    'Debe ingresar un correo electrónico para activar '
                    'las notificaciones.'
                )
            })

    def save(self, *args, **kwargs):
        # Normalizar el RUT: elimina puntos, guion y espacios.
        self.id_card = (
            self.id_card
            .replace('.', '')
            .replace('-', '')
            .replace(' ', '')
            .upper()
        )

        previous_consent = False

        if self.pk:
            previous_consent = Employee.objects.filter(
                pk=self.pk
            ).values_list(
                'email_notifications_enabled',
                flat=True,
            ).first()

        # El trabajador acaba de autorizar.
        if self.email_notifications_enabled and not previous_consent:
            self.email_consent_at = timezone.now()
            self.email_consent_revoked_at = None

        # El trabajador acaba de retirar la autorización.
        if previous_consent and not self.email_notifications_enabled:
            self.email_consent_revoked_at = timezone.now()

        self.full_clean()
        super().save(*args, **kwargs)

        # Mantener sincronizados nombre, apellido y correo con Django User.
        if self.user:
            fields_to_update = []

            if self.user.first_name != self.name:
                self.user.first_name = self.name
                fields_to_update.append('first_name')

            if self.user.last_name != self.last_name:
                self.user.last_name = self.last_name
                fields_to_update.append('last_name')

            if self.user.email != self.email:
                self.user.email = self.email
                fields_to_update.append('email')

            if fields_to_update:
                self.user.save(update_fields=fields_to_update)

    @property
    def full_name(self):
        return f'{self.name} {self.last_name}'.strip()

    def __str__(self):
        return self.full_name