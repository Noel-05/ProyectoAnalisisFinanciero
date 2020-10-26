from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Sector(models.Model):
    codSector = models.CharField(primary_key=True, max_length=15, null=False)
    nombreSector = models.CharField(max_length=100, null=False)
    descripcionSector = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.nombreSector

class ActividadEconomica(models.Model):
    codActividadEconomica = models.CharField(primary_key=True, max_length=15, null=False)
    nombreActividadEconomica = models.CharField(max_length=100, null=False)
    descripcionActividadEconomica = models.CharField(max_length=100, null=True, blank=True)
    codSector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreActividadEconomica


class Empresa(models.Model):
    codEmpresa = models.CharField(primary_key=True, max_length=15, null=False)
    codActividadEconomica = models.ForeignKey(ActividadEconomica, on_delete=models.CASCADE)
    nombreEmpresa = models.CharField(max_length=100, null=False)
    descripcionEmpresa = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.codEmpresa


class TipoCuenta(models.Model):
    codTipoCuenta = models.CharField(primary_key=True, max_length=15, null=False)
    nombreTipoCuenta =models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombreTipoCuenta


class Rubro(models.Model):
    codRubro = models.CharField(primary_key=True, max_length=50, null=False)
    nombreRubro = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombreRubro


class CatalogoCuenta(models.Model):
    codCuenta = models.CharField(primary_key=True, max_length=50, null=False)
    codEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombreCuenta = models.CharField(max_length=100, null=False)
    codTipoCuenta = models.ForeignKey(TipoCuenta, on_delete=models.CASCADE)
    codRubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("codEmpresa", "codCuenta")

    def __str__(self):
        return self.codCuenta.__str__()



class CuentaBalance(models.Model):
    codCuenta = models.ForeignKey(CatalogoCuenta, on_delete=models.CASCADE)
    codEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    año = models.IntegerField(null=False)
    valor = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    class Meta:
        unique_together = ("codEmpresa", "codCuenta", "año")

    def save(self, *args, **kwargs):
        # Aqui ponemos el codigo del trigger -------
        catalogo = CatalogoCuenta.objects.filter(codCuenta = self.codCuenta, codEmpresa = self.codEmpresa)

        suma = 1
        if len(catalogo) == 0:
            suma = 0

        if suma == 0:
            raise ValidationError(
                _('La Empresa: %(value)s no posee la cuenta %(value2)s'),
                params={
                    'value': self.codEmpresa,
                    'value2': self.codCuenta 
                },
            )
        return super(CuentaBalance, self).save( *args, **kwargs)  # llamada al save() original con sus parámetros correspondientes

    def __str__(self):
        return self.codEmpresa.__str__()



class RazonesFinanciera(models.Model):
    codRazon = models.CharField(primary_key=True, max_length=10, null=False)
    nombreRazon = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nombreRazon


class Ratio(models.Model):
    codRatio = models.CharField(primary_key=True, max_length=10, null=False)
    nombreRatio = models.CharField(max_length=100, null=False)
    codRazon = models.ForeignKey(RazonesFinanciera, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreRatio


class RatiosEmpresa(models.Model):
    codRatio = models.ForeignKey(Ratio, on_delete=models.CASCADE)
    codEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    valorRatioEmpresa = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    año = models.IntegerField(null=False)
    
    class Meta:
        unique_together = ("codEmpresa", "codRatio", "año")
    
    def __str__(self):
        return self.codEmpresa.__str__()


class RatiosSector(models.Model):
    codRatio = models.ForeignKey(Ratio, on_delete=models.CASCADE)
    codSector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    parametroComparacion = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    class Meta:
        unique_together = ("codSector", "codRatio")

    def __str__(self):
        return self.codSector.__str__()