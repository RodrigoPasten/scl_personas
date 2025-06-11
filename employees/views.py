from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Employee


@staff_member_required  # Solo admin puede usar esto
def crear_usuario_empleado(request, employee_id):
    # Buscar el empleado
    empleado = get_object_or_404(Employee, id=employee_id)

    # ¿Ya tiene usuario?
    if empleado.user:
        messages.warning(request, f'{empleado} ya tiene usuario creado')
        return redirect('/admin/')  # Vuelve al admin

    # ¿Está activo?
    if empleado.status != 'Activo':
        messages.error(request, f'{empleado} no está activo, no se puede crear usuario')
        return redirect('/admin/')

    # Generar username y password
    username = generar_username(empleado)
    password = empleado.id_card  # Usamos la cédula como contraseña inicial

    # Crear el usuario en Django
    nuevo_usuario = User.objects.create_user(
        username=username,
        password=password,
        first_name=empleado.name,
        last_name=empleado.last_name,
        email=empleado.mail
    )

    # Conectar empleado con usuario
    empleado.user = nuevo_usuario
    empleado.save()

    messages.success(request, f'Usuario creado para {empleado}. Username: {username}, Password: {password}')
    return redirect('/admin/')


def generar_username(empleado):
    # Ejemplo: juan.perez (nombre.apellido)
    nombre = empleado.name.split()[0].lower()  # Primer nombre
    apellido = empleado.last_name.split()[0].lower()  # Primer apellido
    username = f"{nombre}.{apellido}"

    # Si ya existe, agregar número
    counter = 1
    original_username = username
    while User.objects.filter(username=username).exists():
        username = f"{original_username}{counter}"
        counter += 1

    return username


@staff_member_required
def ver_credenciales_empleado(request, employee_id):
    empleado = get_object_or_404(Employee, id=employee_id)

    if not empleado.user:
        messages.error(request, f'{empleado} no tiene usuario creado')
        return redirect('/admin/')

    # Mostrar las credenciales
    context = {
        'empleado': empleado,
        'username': empleado.user.username,
        'password_original': empleado.id_card,  # Sabemos que usamos la cédula
    }

    return render(request, 'credenciales.html', context)