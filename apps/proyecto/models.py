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
    nombreTipoCuenta =models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nombreTipoCuenta


class Rubro(models.Model):
    codRubro = models.CharField(primary_key=True, max_length=50, null=False)
    nombreRubro = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.codRubro


class CatalogoCuenta(models.Model):
    codCuenta = models.CharField(primary_key=True, max_length=50, null=False)
    nombreCuenta = models.CharField(max_length=100, null=False)
    codEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codRubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    codTipoCuenta = models.ForeignKey(TipoCuenta, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("codEmpresa", "codCuenta")

    def __str__(self):
        return self.codCuenta.__str__()



class CuentaBalance(models.Model):
    codCuenta = models.ForeignKey(CatalogoCuenta, on_delete=models.CASCADE)
    codEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    año = models.IntegerField(null=False)
    valor = models.DecimalField(max_digits=18, decimal_places=2, null=False)

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
    valorRatioEmpresa = models.DecimalField(max_digits=18, decimal_places=3, null=False)
    año = models.IntegerField(null=False)
    
    class Meta:
        unique_together = ("codEmpresa", "codRatio", "año")
    
    def __str__(self):
        return self.codEmpresa.__str__()


class RatiosSector(models.Model):
    codRatio = models.ForeignKey(Ratio, on_delete=models.CASCADE)
    codActividadEconomica = models.ForeignKey(ActividadEconomica, on_delete=models.CASCADE)
    parametroComparacion = models.DecimalField(max_digits=18, decimal_places=3, null=False)

    class Meta:
        unique_together = ("codActividadEconomica", "codRatio")

    def __str__(self):
        return self.codActividadEconomica.__str__()


class AnalisisHorizontal(models.Model):
    codEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codCuenta = models.ForeignKey(CatalogoCuenta, on_delete=models.CASCADE)
    añoActual = models.IntegerField(null=False)
    valorActual = models.DecimalField(max_digits=18, decimal_places=2, null=False)
    añoAnterior = models.IntegerField(null=False)
    valorAnterior = models.DecimalField(max_digits=18, decimal_places=2, null=False)
    valorAbsoluto = models.DecimalField(max_digits=18, decimal_places=3, null=False)
    valorRelativo = models.DecimalField(max_digits=18, decimal_places=3, null=False)

    class Meta:
            unique_together = ("codEmpresa", "codCuenta", "añoActual")

    def __str__(self):
        return self.codEmpresa.__str__() + self.codCuenta.__str__() + self.añoActual.__str__()


class AnalisisVertical(models.Model):
    codEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codCuenta = models.ForeignKey(CatalogoCuenta, on_delete=models.CASCADE)
    codRubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    año = models.IntegerField(null=False)
    valor = models.DecimalField(max_digits=18, decimal_places=3, null=False)
    
    class Meta:
            unique_together = ("codEmpresa", "codCuenta", "año")

    def __str__(self):
        return self.codEmpresa.__str__() + self.codCuenta.__str__() + self.año.__str__()


class RatiosEmpresaSector(models.Model):
    codActividadEconomica = models.ForeignKey(ActividadEconomica, on_delete=models.CASCADE)
    año = models.IntegerField(null=False)
    codRatio = models.ForeignKey(Ratio, on_delete=models.CASCADE)
    valorSector = models.DecimalField(max_digits=18, decimal_places=3, null=False)
    promEmpresas = models.DecimalField(max_digits=18, decimal_places=3, null=False)
    empresasCumplenSector = models.CharField(max_length=300, null=False)
    empresasCumplenEmpresa = models.CharField(max_length=300, null=False)
    
    class Meta:
        unique_together = ("codActividadEconomica", "año", "codRatio")
    
    def __str__(self):
        return self.codActividadEconomica.__str__() + self.año.__str__() + self.codRatio.__str__()


class AnalisisEmpresaSector(models.Model):
    codEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    año = models.IntegerField(null=False)
    codRatio = models.ForeignKey(Ratio, on_delete=models.CASCADE)
    valorSector = models.DecimalField(max_digits=18, decimal_places=3, null=True, blank=True)
    valorEmpresa = models.DecimalField(max_digits=18, decimal_places=3, null=True, blank=True)
    mensajeSector = models.CharField(max_length=250, null=True, blank=True)
    promEmpresas = models.DecimalField(max_digits=18, decimal_places=3, null=True, blank=True)
    mensajePromedio = models.CharField(max_length=250, null=True, blank=True)
    
    class Meta:
        unique_together = ("codEmpresa", "año", "codRatio")
    
    def __str__(self):
        return self.codEmpresa.__str__() + self.año.__str__() + self.codRatio.__str__()