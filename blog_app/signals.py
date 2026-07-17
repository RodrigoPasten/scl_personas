from django.conf import settings
from django.core.mail import send_mass_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from employees.models import Employee
from .models import Blog


@receiver(post_save, sender=Blog)
def notificar_publicacion(sender, instance, **kwargs):
    # Salir temprano si no corresponde avisar.
    if instance.status != 'Publicado' or instance.notification_sent:
        return

    # Solo quienes autorizaron y tienen correo cargado.
    destinatarios = (
        Employee.objects
        .filter(email_notifications_enabled=True)
        .exclude(email='')
        .values_list('email', flat=True)
    )

    if destinatarios:
        url = f"{settings.SITE_URL}/{instance.slug}"
        asunto = f'Nueva publicación: {instance.title}'
        cuerpo = (
            f'Se ha publicado un nuevo contenido en el portal:\n\n'
            f'{instance.title}\n\n'
            f'{instance.short_description}\n\n'
            f'Puede leerlo aquí: {url}\n\n'
            f'— Gestión de Personas, Serving Consultores'
        )

        # Un mensaje por persona: nadie ve el correo de los demás.
        mensajes = tuple(
            (asunto, cuerpo, settings.DEFAULT_FROM_EMAIL, [correo])
            for correo in destinatarios
        )
        send_mass_mail(mensajes, fail_silently=False)

    # Marcar como enviada. .update() NO dispara post_save,
    # así evitamos que la señal se llame a sí misma en bucle infinito.
    Blog.objects.filter(pk=instance.pk).update(notification_sent=True)