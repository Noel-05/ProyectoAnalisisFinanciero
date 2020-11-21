# Generated by Django 3.1.1 on 2020-11-17 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalisisEmpresaSector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('año', models.IntegerField()),
                ('valorSector', models.DecimalField(blank=True, decimal_places=3, max_digits=18, null=True)),
                ('valorEmpresa', models.DecimalField(blank=True, decimal_places=3, max_digits=18, null=True)),
                ('mensajeSector', models.CharField(blank=True, max_length=250, null=True)),
                ('promEmpresas', models.DecimalField(blank=True, decimal_places=3, max_digits=18, null=True)),
                ('mensajePromedio', models.CharField(blank=True, max_length=250, null=True)),
                ('codEmpresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.empresa')),
                ('codRatio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.ratio')),
            ],
            options={
                'unique_together': {('codEmpresa', 'año', 'codRatio')},
            },
        ),
    ]