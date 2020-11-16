from django.shortcuts import redirect
from django.contrib import messages

# Mixin Empleado, Gerente y Administrador
class LoginGEAMixin(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.rol == 'EMP' or request.user.rol == 'GER' or request.user.rol == 'ADM':
				return super().dispatch(request, *args, **kwargs)
			messages.error(request, 'No tienes permisos para realizar esta acción.')
		return redirect('usuario:index')

# Mixin Gerente y Administrador
class LoginGAMixin(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.rol == 'GER' or request.user.rol == 'ADM':
				return super().dispatch(request, *args, **kwargs)
			messages.error(request, 'No tienes permisos para realizar esta acción.')
		return redirect('usuario:index')

# Mixin Empleado y Administrador
class LoginEAMixin(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.rol == 'EMP' or request.user.rol == 'ADM':
				return super().dispatch(request, *args, **kwargs)
			messages.error(request, 'No tienes permisos para realizar esta acción.')
		return redirect('usuario:index')

# Mixin Administrador
class LoginAMixin(object):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.rol == 'ADM':
				return super().dispatch(request, *args, **kwargs)
			messages.error(request, 'No tienes permisos para realizar esta acción.')
		return redirect('usuario:index')