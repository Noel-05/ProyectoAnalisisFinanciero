from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static 
 
app_name = 'analisisFinanciero'

urlpatterns = [
    path('', index),
    path('analisisFinanciero/index/', index, name='index'),
    
    path('analisisFinanciero/crearBalance', BalanceCrear.as_view(template_name = "proyecto/crearBalance.html"), name='crearBalance'),
    path('analisisFinanciero/editarBalance/<str:pk>', BalanceActualizar.as_view(template_name = "proyecto/editarBalance.html"), name='editarBalance'),
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

    path('analisisFinanciero/catalogo', CatalogoListado.as_view(template_name = "proyecto/catalogo.html"), name='catalogo'),
    path('analisisFinanciero/crearCatalogo', CatalogoCrear.as_view(template_name = "proyecto/crearCatalogo.html"), name='crearCatalogo'),
    path('analisisFinanciero/editarCatalogo/<str:pk>', CatalogoActualizar.as_view(template_name = "proyecto/editarCatalogo.html"), name='editarCatalogo'),
    path('analisisFinanciero/eliminarCatalogo/<str:pk>', CatalogoEliminar.as_view(), name='eliminarCatalogo'),
    path('analisisFinanciero/detalleCatalogo/<str:pk>', CatalogoDetalle.as_view(template_name = "proyecto/detalleCatalogo.html"), name='detalleCatalogo'),

]
