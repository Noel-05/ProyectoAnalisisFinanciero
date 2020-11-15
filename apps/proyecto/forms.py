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
		
class CuentaBalanceForm(forms.ModelForm):
	class Meta:
		model=CuentaBalance
		fields={
		'codCuenta':forms.CharField,
		'codEmpresa':forms.CharField,
		'año':forms.CharField,
		'valor':forms.CharField,
		}
		labels={
		'codCuenta':'Codigo de Cuenta',
		'codEmpresa':'Codigo de Empresa',
		'año': 'Año',
		'valor':'Valor',
		}