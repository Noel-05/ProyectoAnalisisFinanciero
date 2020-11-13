from django import forms
from .models import *

class CatalogoCuentaForm(forms.ModelForm):
	class Meta:
		model=CatalogoCuenta
		fields={
		'codCuenta':forms.CharField,
		'nombreCuenta':forms.CharField,
		'codEmpresa':forms.CharField,
		'codRubro':forms.CharField,
		'codTipoCuenta':forms.CharField,
		}
		labels={
		'codCuenta':'Codigo de Cuenta',
		'nombreCuenta': 'Nombre de la Cuenta',
		'codEmpresa':'Codigo de Empresa',
		'codRubro':'Codigo del Rubro',
		'codTipoCuenta': 'Codigo del Tipo de Cuenta',
		}