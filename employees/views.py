
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import Employee


def normalizar_rut(rut):
    """
    Convierte diferentes formatos de RUT a un formato único.

    Ejemplos:
    12.345.678-9 -> 123456789
    12345678-9   -> 123456789
    """
    return (
        rut.replace('.', '')
        .replace('-', '')
        .replace(' ', '')
        .upper()
    )


@staff_member_required
def crear_usuario_empleado(request, employee_id):
    empleado = get_object_or_404(Employee, id=employee_id)

    # Evitar crear dos usuarios para el mismo trabajador.
    if empleado.user:
        messages.warning(
            request,
            f'{empleado} ya tiene un usuario creado.'
        )
        return redirect('/admin/employees/employee/')

    rut_normalizado = normalizar_rut(empleado.id_card)

    # El RUT será el username interno de Django.
    username = rut_normalizado

    # Contraseña inicial.
    password = rut_normalizado

    # Evitar que dos trabajadores compartan el mismo RUT.
    if User.objects.filter(username=username).exists():
        messages.error(
            request,
            f'Ya existe un usuario asociado al RUT {empleado.id_card}.'
        )
        return redirect('/admin/employees/employee/')

    # Crea el usuario y conecta el Employee en una sola operación.
    with transaction.atomic():
        nuevo_usuario = User.objects.create_user(
            username=username,
            password=password,
            first_name=empleado.name,
            last_name=empleado.last_name,
            email=empleado.email or '',
        )

        empleado.user = nuevo_usuario
        empleado.save()

    messages.success(
        request,
        (
            f'Usuario creado para {empleado}. '
            f'RUT de acceso: {empleado.id_card}. '
            f'Contraseña inicial: {password}.'
        )
    )

    return redirect('/admin/employees/employee/')


@staff_member_required
def ver_credenciales_empleado(request, employee_id):
    empleado = get_object_or_404(Employee, id=employee_id)

    if not empleado.user:
        messages.error(
            request,
            f'{empleado} no tiene un usuario creado.'
        )
        return redirect('/admin/employees/employee/')

    context = {
        'empleado': empleado,
        'username': empleado.id_card,
        'password_original': empleado.id_card,
    }

    return render(
        request,
        'credenciales.html',
        context,
    )
@staff_member_required
def resetear_password_empleado(request, employee_id):
    empleado = get_object_or_404(Employee, id=employee_id)

    if not empleado.user:
        messages.error(request, f'{empleado} no tiene un usuario creado.')
        return redirect('/admin/employees/employee/')

    rut_normalizado = normalizar_rut(empleado.id_card)

    with transaction.atomic():
        empleado.user.set_password(rut_normalizado)
        empleado.user.save()

        empleado.must_change_password = True
        empleado.save()

    messages.success(
        request,
        f'Contraseña de {empleado} reseteada a su RUT (sin puntos ni guion). '
        f'Deberá crear una nueva al iniciar sesión.'
    )
    return redirect('/admin/employees/employee/')