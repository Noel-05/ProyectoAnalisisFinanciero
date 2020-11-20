from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static 
 
app_name = 'analisisFinanciero'

urlpatterns = [
    path('', index),
    path('analisisFinanciero/index/', index, name='index'),
    
    path('analisisFinanciero/consultaBalance/<username>/', consultarBalance, name="consultarBalance"),
    path('analisisFinanciero/subirBalance/', subirBalance, name="subirBalance"),
    path('analisisFinanciero/Balances', filtrarBalance, name="filtrarBalance"),
    path('analisisFinanciero/crearBalance', BalanceCrear.as_view(template_name = "proyecto/crearBalance.html"), name='crearBalance'),
    path('analisisFinanciero/actualizarBalance', actualizarBalance, name="actualizarBalance"),
    path('analisisFinanciero/guardarModificacionBalance', guardarModificacionBalance, name="guardarModificacionBalance"),

    path('analisisFinanciero/consultaRazonActividad/<username>/', consultarRazonActividad, name="consultarRazonActividad"),
    path('analisisFinanciero/ratiosActividad', ratiosActividad, name="ratiosActividad"),

    path('analisisFinanciero/consultaRazonLiquidez/<username>/', consultarRazonLiquidez, name="consultarRazonLiquidez"),
    path('analisisFinanciero/ratiosLiquidez', ratiosLiquidez, name="ratiosLiquidez"),

    path('analisisFinanciero/consultaRazonApalancamiento/<username>/', consultarRazonApalancamiento, name="consultarRazonApalancamiento"),
    path('analisisFinanciero/ratiosApalancamiento', ratiosApalancamiento, name="ratiosApalancamiento"),

    path('analisisFinanciero/consultaRazonRentabilidad/<username>/', consultarRazonRentabilidad, name="consultarRazonRentabilidad"),
    path('analisisFinanciero/ratiosRentabilidad', ratiosRentabilidad, name="ratiosRentabilidad"),

    path('analisisFinanciero/consultaAnalisisDupont/<username>/', consultarAnalisisDupont, name="consultarAnalisisDupont"),
    path('analisisFinanciero/analisisDupont', analisisDupont, name="analisisDupont"),

    path('analisisFinanciero/consultaAnalisisHorizontal/<username>/', consultarAnalisisHorizontal, name="consultarAnalisisHorizontal"),
    path('analisisFinanciero/analisisHorizontal', analisisHorizontal, name="analisisHorizontal"),

    path('analisisFinanciero/consultaAnalisisVertical/<username>/', consultarAnalisisVertical, name="consultarAnalisisVertical"),
    path('analisisFinanciero/analisisVertical', analisisVertical, name="analisisVertical"),

    path('analisisFinanciero/consultarInformes', consultarInformes, name="consultarInformes"),
    path('analisisFinanciero/analisisInformes', informeAnalisis, name="informeAnalisis"),

    path('analisisFinanciero/consultarInformeEmpresa/<username>/', consultarInformeEmpresa, name="consultarInformeEmpresa"),
    path('analisisFinanciero/analisisInformeEmpresa', informeAnalisisEmpresa, name="informeAnalisisEmpresa"),

    path('analisisFinanciero/insertarRatioSector', insertarRatioSector, name="insertarRatioSector"),
    path('analisisFinanciero/consultarRatioSector', consultarRatioSector, name="consultarRatioSector"),
    path('analisisFinanciero/actualizarRatioSector', actualizarRatioSector, name="actualizarRatioSector"),
    path('analisisFinanciero/guardarModificacionRatioSector', guardarModificacionRatioSector, name="guardarModificacionRatioSector"),
    path('analisisFinanciero/eliminarRatioSecto', eliminarRatioSector, name="eliminarRatioSector"),

    path('analisisFinanciero/insertarEmpresa', insertarEmpresa, name="insertarEmpresa"),
    path('analisisFinanciero/consultarEmpresaAdmin/', consultarEmpresaAdmin, name="consultarEmpresaAdmin"),
    path('analisisFinanciero/consultarEmpresa/<username>/', consultarEmpresa, name="consultarEmpresa"),
    path('analisisFinanciero/actualizarEmpresa', actualizarEmpresa, name="actualizarEmpresa"),
    path('analisisFinanciero/guardarModificacionEmpresa', guardarModificacionEmpresa, name="guardarModificacionEmpresa"),
    path('analisisFinanciero/eliminarEmpresa', eliminarEmpresa, name="eliminarEmpresa"),

    # path('analisisFinanciero/catalogo', CatalogoListado.as_view(template_name = "proyecto/catalogo.html"), name='catalogo'),
    # path('analisisFinanciero/consultarCatalogo', consultarCatalogo, name="consultarCatalogo"),
    # path('analisisFinanciero/crearCatalogo', CatalogoCrear.as_view(template_name = "proyecto/crearCatalogo.html"), name='crearCatalogo'),
    # path('analisisFinanciero/editarCatalogo/<str:pk>', CatalogoActualizar.as_view(template_name = "proyecto/editarCatalogo.html"), name='editarCatalogo'),
    # path('analisisFinanciero/editarCatalogo2/<str:pk>', CatalogoActualizar2.as_view(template_name = "proyecto/editarCatalogo.html"), name='editarCatalogo2'),
    # path('analisisFinanciero/eliminarCatalogo/<str:pk>', CatalogoEliminar.as_view(), name='eliminarCatalogo'),
    # path('analisisFinanciero/detalleCatalogo/<str:pk>', CatalogoDetalle.as_view(template_name = "proyecto/detalleCatalogo.html"), name='detalleCatalogo'),

    path('analisisFinanciero/catalogo', CatalogoListado.as_view(template_name = "proyecto/catalogo.html"), name='catalogo'),
    path('analisisFinanciero/consultarCatalogo/<username>/', consultarCatalogo, name="consultarCatalogo"),
    path('analisisFinanciero/crearCatalogo', CatalogoCrear.as_view(template_name = "proyecto/crearCatalogo.html"), name='crearCatalogo'),
    path('analisisFinanciero/editarCatalogo2/<str:pk>', CatalogoActualizar2.as_view(template_name = "proyecto/editarCatalogo.html"), name='editarCatalogo2'),
    path('analisisFinanciero/eliminarCatalogo/<str:pk>', CatalogoEliminar.as_view(), name='eliminarCatalogo'),
    path('analisisFinanciero/detalleCatalogo/<str:pk>', CatalogoDetalle.as_view(template_name = "proyecto/detalleCatalogo.html"), name='detalleCatalogo'),


]
