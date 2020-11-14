from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'analisisFinanciero'

urlpatterns = [
    path('', index),
    path('analisisFinanciero/index/', index, name='index'),
    
    path('analisisFinanciero/consultaBalance', consultarBalance, name="consultarBalance"),
    path('analisisFinanciero/subirBalance/', subirBalance, name="subirBalance"),
    path('analisisFinanciero/Balances', filtrarBalance, name="filtrarBalance"),

    path('analisisFinanciero/consultaRazonActividad', consultarRazonActividad, name="consultarRazonActividad"),
    path('analisisFinanciero/ratiosActividad', ratiosActividad, name="ratiosActividad"),

    path('analisisFinanciero/consultaRazonLiquidez', consultarRazonLiquidez, name="consultarRazonLiquidez"),
    path('analisisFinanciero/ratiosLiquidez', ratiosLiquidez, name="ratiosLiquidez"),

    path('analisisFinanciero/consultaRazonApalancamiento', consultarRazonApalancamiento, name="consultarRazonApalancamiento"),
    path('analisisFinanciero/ratiosApalancamiento', ratiosApalancamiento, name="ratiosApalancamiento"),

    path('analisisFinanciero/consultaRazonRentabilidad', consultarRazonRentabilidad, name="consultarRazonRentabilidad"),
    path('analisisFinanciero/ratiosRentabilidad', ratiosRentabilidad, name="ratiosRentabilidad"),

    path('analisisFinanciero/consultaAnalisisDupont', consultarAnalisisDupont, name="consultarAnalisisDupont"),
    path('analisisFinanciero/analisisDupont', analisisDupont, name="analisisDupont"),

    path('analisisFinanciero/consultaAnalisisHorizontal', consultarAnalisisHorizontal, name="consultarAnalisisHorizontal"),
    path('analisisFinanciero/analisisHorizontal', analisisHorizontal, name="analisisHorizontal"),

    path('analisisFinanciero/consultaAnalisisVertical', consultarAnalisisVertical, name="consultarAnalisisVertical"),
    path('analisisFinanciero/analisisVertical', analisisVertical, name="analisisVertical"),

    path('analisisFinanciero/consultarInformes', consultarInformes, name="consultarInformes"),
    path('analisisFinanciero/analisisInformes', informeAnalisis, name="informeAnalisis"),
    path('analisisFinanciero/insertarRatioSector', insertarRatioSector, name="insertarRatioSector"),
    path('analisisFinanciero/consultarRatioSector', consultarRatioSector, name="consultarRatioSector"),
    #path('analisisFinanciero/consultarRatioSector/<codAct>/<codRat>', consultarRatioSector, name="consultarRatioSector"),
    path('analisisFinanciero/actualizarRatioSector', actualizarRatioSector, name="actualizarRatioSector"),
    path('analisisFinanciero/guardarModificacionRatioSector', guardarModificacionRatioSector, name="guardarModificacionRatioSector"),
    path('analisisFinanciero/eliminarRatioSecto', eliminarRatioSector, name="eliminarRatioSector"),

    path('analisisFinanciero/insertarEmpresa', insertarEmpresa, name="insertarEmpresa"),
    path('analisisFinanciero/consultarEmpresa', consultarEmpresa, name="consultarEmpresa"),
    path('analisisFinanciero/actualizarEmpresa', actualizarEmpresa, name="actualizarEmpresa"),
    path('analisisFinanciero/guardarModificacionEmpresa', guardarModificacionEmpresa, name="guardarModificacionEmpresa"),
    path('analisisFinanciero/eliminarEmpresa', eliminarEmpresa, name="eliminarEmpresa"),
]
