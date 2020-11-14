from django.contrib import admin

from .models import *

admin.site.register(Sector)
admin.site.register(ActividadEconomica)
admin.site.register(Empresa)
admin.site.register(TipoCuenta)
admin.site.register(Rubro)
admin.site.register(CatalogoCuenta)
admin.site.register(CuentaBalance)
admin.site.register(RazonesFinanciera)
admin.site.register(Ratio)
admin.site.register(RatiosEmpresa)
admin.site.register(RatiosSector)
admin.site.register(RatiosEmpresaSector)
admin.site.register(AnalisisHorizontal)
admin.site.register(AnalisisVertical)