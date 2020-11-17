# Generated by Django 3.1.1 on 2020-11-17 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Nombre de usuario')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('nombres', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombres')),
                ('apellidos', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellidos')),
                ('imagen', models.ImageField(blank=True, max_length=200, null=True, upload_to='perfil/', verbose_name='Imagen de Perfil')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
                ('rol', models.CharField(choices=[('ADM', 'Administrador'), ('GER', 'Gerente'), ('EMP', 'Empleado')], default='EMP', max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
