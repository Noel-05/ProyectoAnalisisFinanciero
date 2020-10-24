#resources.py  
from import_export import resources
from .models import *


class BalanceResource(resources.ModelResource):
    class Meta:
        model = CuentaBalance
        exclude = ('nombreCuenta',)


#---------------------------------------------------

# class PruebaResource(resources.ModelResource):
#     class Meta:
#         model = Prueba
#         import_id_fields = ('codigoPrueba',)
