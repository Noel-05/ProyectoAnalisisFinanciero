from django import forms
from django.contrib.auth.forms import AuthenticationForm
from apps.usuario.models import Usuario

class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class FormularioUsuarioLogin(forms.ModelForm):

	password1=forms.CharField(label='Contraseña', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder':'Ingrese su Contraseña',
			'id': 'password1',
			'required':'required',
		}
	))

	password2=forms.CharField(label='Contraseña de Confirmacion', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder':'Ingrese nuevamente su Contraseña',
			'id': 'password2',
			'required':'required',
		}
	))

	class Meta:
		model=Usuario
		fields=('email', 'username', 'nombres', 'apellidos')
		widgets ={
			'email': forms.EmailInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Correo Electronico',
				}
			),
			'nombres': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Nombre',
				}
			),
			'apellidos': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Apellido',
				}
			),

			'username': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Carnet',
				}
			)
		
		}

	def clean_password2(self):

		print(self.cleaned_data)
		password1=self.cleaned_data.get('password1')
		password2=self.cleaned_data.get('password2')

		if password1 != password2:
			raise forms.ValidationError('Contraseñas no coinciden')
		return password2

	def save(self, commit=True):
		user=super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class FormularioUsuario(forms.ModelForm):

	password1=forms.CharField(label='Contraseña', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder':'Ingrese su Contraseña',
			'id': 'password1',
			'required':'required',
		}
	))

	password2=forms.CharField(label='Contraseña de Confirmacion', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder':'Ingrese nuevamente su Contraseña',
			'id': 'password2',
			'required':'required',
		}
	))

	class Meta:
		model=Usuario
		fields=('email', 'username', 'nombres', 'apellidos', 'rol')
		widgets ={
			'email': forms.EmailInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Correo Electronico',
				}
			),
			'nombres': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Nombre',
				}
			),
			'apellidos': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Apellido',
				}
			),

			'username': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Carnet',
				}
			)
		
		}

	def clean_password2(self):

		print(self.cleaned_data)
		password1=self.cleaned_data.get('password1')
		password2=self.cleaned_data.get('password2')

		if password1 != password2:
			raise forms.ValidationError('Contraseñas no coinciden')
		return password2

	def save(self, commit=True):
		user=super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class FormularioUsuarioEditar(forms.ModelForm):

	class Meta:
		model=Usuario
		fields=('email', 'username', 'nombres', 'apellidos', 'rol')
		widgets ={
			'email': forms.EmailInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Correo Electronico',
				}
			),
			'nombres': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Nombre',
				}
			),
			'apellidos': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Apellido',
				}
			),
			'username': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Carnet',
				}
			)
		}

	def save(self, commit=True):
		user=super().save(commit=False)
		if commit:
			user.save()
		return user




