from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    """
    Si el usuario autenticado tiene must_change_password activo,
    lo redirige al cambio de contraseña en cualquier página que visite.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            empleado = getattr(request.user, 'employee', None)

            if empleado and empleado.must_change_password:
                rutas_permitidas = [
                    reverse('cambiar_password'),
                    reverse('logout'),
                ]

                if request.path not in rutas_permitidas and not request.path.startswith('/admin/'):
                    return redirect('cambiar_password')

        return self.get_response(request)