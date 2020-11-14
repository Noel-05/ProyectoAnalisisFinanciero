from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import render
from django.shortcuts import redirect
from django.core import serializers
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView
from django import forms

import tablib
from tablib import Dataset
from .resources import *


#Vista para el menu base
def index(request):
    return render(
        request,
        'base/base.html'
    )


#--------------------------------------------------------------------------------------------------------------------------------------------


def consultarBalance(request):
    return render(
        request,
        'proyecto/ConsultaBalance.html'
    )



def subirBalance(request):
    error = 0
    if request.method == 'POST':
        balance_resource = BalanceResource()  
        dataset = Dataset()
        print(dataset)  
        nuevo_balance = request.FILES['xlsfile']  
        print(nuevo_balance)  
        imported_data = dataset.load(nuevo_balance.read())  
        print(dataset)  
        result = balance_resource.import_data(dataset, dry_run=True) # Test the data import  
        print(result.has_errors())  
        
        if result.has_errors():
            return render(request, 'proyecto/error.html')
        
        if not result.has_errors():
            balance_resource.import_data(dataset, dry_run=False) # Actually import now 
    
    return render(request, 'proyecto/SubirBalance.html')



def filtrarBalance(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']

        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año).order_by('codCuenta')
        empresa = Empresa.objects.get(codEmpresa=codEmpresa)

        contexto = {
            'queryset': queryset, 
            'año': año,
            'empresa': empresa,
        }

        return render(
            request,
            'proyecto/ConsultaBalance.html', contexto
        )

class BalanceCrear(SuccessMessageMixin, CreateView):
    model = CuentaBalance #Llamada a la clase "CatalogoCuenta" en el archivo models.py
    form = CuentaBalanceForm #Definición del formulario ubicado en forms.py
    fields = "__all__" #Le decimos a Django que muestre todos los campos de la tabla de nuestra Base de Datos
    success_message='¡Balance Creado Correctamente!' #Muestra el mensaje si se ha realizado correctamente la operación

    def get_success_url(self):
        return reverse('analisisFinanciero:crearBalance')
        
class BalanceActualizar(SuccessMessageMixin, UpdateView): 
    model = CuentaBalance 
    form = CuentaBalanceForm 
    fields = "__all__" 
    success_message = '¡Balance Actualizado Correctamente!' 
 
    
    def get_success_url(self):               
        return reverse('analisisFinanciero:editarBalance') 

#--------------------------------------------------------------------------------------------------------------------------------------------


def consultarRazonActividad(request):
    return render(
        request,
        'proyecto/ConsultaRazonActividad.html'
    )



def ratiosActividad(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']
        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año)

        #Por si no existe el balance de ese año que no me de error
        if (len(queryset) == 0):
            contexto = {
                'queryset': queryset, 
            }
            return render(
                request,
                'proyecto/ConsultaRazonActividad.html', contexto
            )

        #Obtengo los datos del año anterior para sacar Promedio
        año2 = int(año) - 1
        queryset2 = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año2)

    #PROCEDIMIENTO DE CALCULO DE RATIOS.

        #Recuperacion de valores para el año solicitado
        i=0
        while(i < len(queryset)):
            tipo = queryset[i].codCuenta.codTipoCuenta_id
            if(tipo == "EFEC"):
                efectivo = queryset[i].valor
            elif(tipo == "INV"):
                inventario = queryset[i].valor
            elif(tipo == "ACCIR"):
                actCirculante = queryset[i].valor
            elif(tipo == "PASTOT"):
                pasivoTotal = queryset[i].valor
            elif(tipo == "COSVEN"):
                costoVentas = queryset[i].valor
            elif(tipo == "CxC"):
                cuentasXCobrar = queryset[i].valor
            elif(tipo == "ACFI"):
                activoFijo = queryset[i].valor
            elif(tipo == "ACTO"):
                activoTotal = queryset[i].valor
            elif(tipo == "PASCIR"):
                pasivoCirc = queryset[i].valor
            elif(tipo == "CxP"):
                cuentasXPagar = queryset[i].valor
            elif(tipo == "PATR"):
                patrimonio = queryset[i].valor
            elif(tipo == "UTBR"):
                utilidadBruta = queryset[i].valor
            elif(tipo == "ING"):
                ingresos = queryset[i].valor
            elif(tipo == "UTOP"):
                utilidadOperativa = queryset[i].valor
            elif(tipo == "GASTFI"):
                gastosFijo = queryset[i].valor
            elif(tipo == "UTAI"):
                utilidadAntesImp = queryset[i].valor
            elif(tipo == "UTNET"):
                utilidadNeta = queryset[i].valor
                
            i+=1

        #Recuperacion de valores para el año anterior para sacar el Promedio
        if( len(queryset2) != 0):
            inventario2 = 0
            cuentasXCobrar2 = 0
            cuentasXPagar2 = 0
            activoTotal2 = 0
            activoFijo2 = 0

            j=0
            while(j < len(queryset2)):
                tipo2 = queryset2[j].codCuenta.codTipoCuenta_id
                if(tipo2 == "EFEC"):
                    efectivo2 = queryset2[j].valor
                elif(tipo2 == "INV"):
                    inventario2 = queryset2[j].valor
                elif(tipo2 == "ACCIR"):
                    actCirculante2 = queryset2[j].valor
                elif(tipo2 == "PASTOT"):
                    pasivoTotal2 = queryset2[j].valor
                elif(tipo2 == "COSVEN"):
                    costoVentas2 = queryset2[j].valor
                elif(tipo2 == "CxC"):
                    cuentasXCobrar2 = queryset2[j].valor
                elif(tipo2 == "ACFI"):
                    activoFijo2 = queryset2[j].valor
                elif(tipo2 == "ACTO"):
                    activoTotal2 = queryset2[j].valor
                elif(tipo2 == "PASCIR"):
                    pasivoCirc2 = queryset2[j].valor
                elif(tipo2 == "CxP"):
                    cuentasXPagar2 = queryset2[j].valor
                elif(tipo2 == "PATR"):
                    patrimonio2 = queryset2[j].valor
                elif(tipo2 == "UTBR"):
                    utilidadBruta2 = queryset2[j].valor
                elif(tipo2 == "ING"):
                    ingresos2 = queryset2[j].valor
                elif(tipo2 == "UTOP"):
                    utilidadOperativa2 = queryset2[j].valor
                elif(tipo2 == "GASTFI"):
                    gastosFijo2 = queryset2[j].valor
                elif(tipo2 == "UTAI"):
                    utilidadAntesImp2 = queryset2[j].valor
                elif(tipo2 == "UTNET"):
                    utilidadNeta2 = queryset2[j].valor

                j+=1
        
            
            #Calculo de las cuentas que se usan en Promedio
            if(inventario2 > 0):
                inventarioPromedio = (inventario2 + inventario) / 2
            else:
                inventarioPromedio = inventario

            if(cuentasXCobrar2 > 0):
                cxcPromedio = (cuentasXCobrar2 + cuentasXCobrar) / 2
            else:
                cxcPromedio = cuentasXCobrar
            
            if(cuentasXPagar2 > 0):
                cxpPromedio = (cuentasXPagar2 + cuentasXPagar) / 2
            else:
                cxpPromedio = cuentasXPagar
            
            if(activoTotal2 > 0):
                actTotPromedio = (activoTotal2 + activoTotal) / 2
            else:
                actTotPromedio = activoTotal

            if(activoFijo2 > 0):
                actFijoPromedio = (activoFijo2 + activoFijo) / 2
            else:
                actFijoPromedio = activoFijo
            
        else:
            #En caso que no haya registros de años anteriores
            inventarioPromedio = inventario
            cxcPromedio = cuentasXCobrar
            cxpPromedio = cuentasXPagar
            actTotPromedio = activoTotal
            actFijoPromedio = activoFijo
        
        #Calculo de los Ratios
        razonRotInve = costoVentas / inventarioPromedio
        razonDiasInve = inventarioPromedio / (costoVentas / 365)

        razonRotCxC = ingresos / cxcPromedio
        razonPerMedCobro = (cxcPromedio * 365) / ingresos

        razonRotCxP = costoVentas / cxpPromedio
        razonPerMedPago = (cxpPromedio * 365) / costoVentas

        indiceRotActTot = ingresos / actTotPromedio
        indiceRotActFij = ingresos / actFijoPromedio

        indiceMargenBruto = utilidadBruta / ingresos
        indiceMargenOperativo = utilidadOperativa / ingresos
        

        #Guardar en BD los Ratios

        # -> Ratio Razon de Rotacion de Invetario
        codRatio="RRI"
        comprobarRRI = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRRI) == 0):
            ratioRazRotInv = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRotInve , codEmpresa_id=codEmpresa, año=año)
            ratioRazRotInv.save()
        
        # -> Ratio Razon de Dias de Inventario
        codRatio="RDI"
        comprobarRDI = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRDI) == 0):
            ratioRazDiasInven = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonDiasInve , codEmpresa_id=codEmpresa, año=año)
            ratioRazDiasInven.save()

        # -> Ratio Razon de Rotacion C x C
        codRatio="RRCC"
        comprobarRRCC = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRRCC) == 0):
            ratioRazRotCxC = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRotCxC , codEmpresa_id=codEmpresa, año=año)
            ratioRazRotCxC.save()
        
        # -> Ratio Razon de Periodo Medio de Cobranza
        codRatio="RPMC"
        comprobarRPMC = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRPMC) == 0):
            ratioRazPerMedCobr = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonPerMedCobro , codEmpresa_id=codEmpresa, año=año)
            ratioRazPerMedCobr.save()
        
        # -> Ratio Razon de Rotacion de Cuentas por Pagar
        codRatio="RRCP"
        comprobarRRCP = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRRCP) == 0):
            ratioRazRotCxP = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRotCxP , codEmpresa_id=codEmpresa, año=año)
            ratioRazRotCxP.save()

        # -> Ratio Razon de Periodo Medio de Pago
        codRatio="RPMP"
        comprobarRPMP = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRPMP) == 0):
            ratioRazPerMedPago = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonPerMedPago , codEmpresa_id=codEmpresa, año=año)
            ratioRazPerMedPago.save()

        # -> Ratio Razon de Indice de Rotacion de Activos Totales
        codRatio="IRAT"
        comprobarIRAT = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarIRAT) == 0):
            ratioIndiceRotActTot = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=indiceRotActTot , codEmpresa_id=codEmpresa, año=año)
            ratioIndiceRotActTot.save()
        
        # -> Ratio Razon de Indice de Rotacion de Activos Fijos
        codRatio="IRAF"
        comprobarIRAF = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarIRAF) == 0):
            ratioIndiceRotActFij = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=indiceRotActFij , codEmpresa_id=codEmpresa, año=año)
            ratioIndiceRotActFij.save()

        # -> Ratio Razon de Indice de Margen Bruto
        codRatio="IMB"
        comprobarIMB = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarIMB) == 0):
            ratioIndiceMargenBruto = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=indiceMargenBruto , codEmpresa_id=codEmpresa, año=año)
            ratioIndiceMargenBruto.save()
        
        # -> Ratio Razon de Indice de Margen Operativo
        codRatio="IMO"
        comprobarIMO = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarIMO) == 0):
            ratioIndiceMargenOper = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=indiceMargenOperativo , codEmpresa_id=codEmpresa, año=año)
            ratioIndiceMargenOper.save()


    #FIN PROCEDIMIENTO DE CALCULO DE RATIOS.
        
        #Para imprimir los ratios de está razón
        recuperar = RatiosEmpresa.objects.filter(codEmpresa_id=codEmpresa, año=año).order_by('codRatio')
        empresa = Empresa.objects.get(codEmpresa=codEmpresa)
        razon = "ACT"
        consulta=[]
        i=0
        while(i < len(recuperar)):
            prueba = recuperar[i].codRatio.codRazon_id
            if(  prueba == razon):
                consulta.append((recuperar[i]))
            i+=1

        contexto = {
            'queryset': queryset,
            'consulta': consulta, 
            'empresa': empresa,
            'año': año,
        }

        return render(
            request,
            'proyecto/ConsultaRazonActividad.html', 
            contexto
        )


#--------------------------------------------------------------------------------------------------------------------------------------------


def consultarRazonLiquidez(request):
    return render(
        request,
        'proyecto/ConsultaRazonLiquidez.html'
    )



def ratiosLiquidez(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']
        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año)

        #Por si no existe el balance de ese año que no me de error
        if (len(queryset) == 0):
            contexto = {
                'queryset': queryset, 
            }
            return render(
                request,
                'proyecto/ConsultaRazonLiquidez.html', contexto
            )

    #PROCEDIMIENTO DE CALCULO DE RATIOS.

        #Recuperacion de valores para el año solicitado
        i=0
        while(i < len(queryset)):
            tipo = queryset[i].codCuenta.codTipoCuenta_id
            if(tipo == "EFEC"):
                efectivo = queryset[i].valor
            elif(tipo == "INV"):
                inventario = queryset[i].valor
            elif(tipo == "ACCIR"):
                actCirculante = queryset[i].valor
            elif(tipo == "PASTOT"):
                pasivoTotal = queryset[i].valor
            elif(tipo == "COSVEN"):
                costoVentas = queryset[i].valor
            elif(tipo == "CxC"):
                cuentasXCobrar = queryset[i].valor
            elif(tipo == "ACFI"):
                activoFijo = queryset[i].valor
            elif(tipo == "ACTO"):
                activoTotal = queryset[i].valor
            elif(tipo == "PASCIR"):
                pasivoCirc = queryset[i].valor
            elif(tipo == "CxP"):
                cuentasXPagar = queryset[i].valor
            elif(tipo == "PATR"):
                patrimonio = queryset[i].valor
            elif(tipo == "UTBR"):
                utilidadBruta = queryset[i].valor
            elif(tipo == "ING"):
                ingresos = queryset[i].valor
            elif(tipo == "UTOP"):
                utilidadOperativa = queryset[i].valor
            elif(tipo == "GASTFI"):
                gastosFijo = queryset[i].valor
            elif(tipo == "UTAI"):
                utilidadAntesImp = queryset[i].valor
            elif(tipo == "UTNET"):
                utilidadNeta = queryset[i].valor
                
            i+=1
        
        #Calculo de los Ratios
        razonCirculante = actCirculante / pasivoCirc

        razonRapida = (actCirculante - inventario) / pasivoCirc

        razonCapitalTrabajo = (actCirculante - pasivoCirc) / activoTotal

        razonEfectivo = (efectivo) / pasivoCirc
        

        #Guardar en BD los Ratios

        # -> Ratio Razon de Circulante o Liquidez Corriente
        codRatio="RC"
        comprobarRC = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRC) == 0):
            ratioRazCirc = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonCirculante, codEmpresa_id=codEmpresa, año=año)
            ratioRazCirc.save()

        # -> Ratio Razon Rápida
        codRatio="RR"
        comprobarRR = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRR) == 0):
            ratioRazRapida = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRapida, codEmpresa_id=codEmpresa, año=año)
            ratioRazRapida.save()
        
        # -> Ratio Razon de Capital de Trabajo
        codRatio="RCT"
        comprobarRCT = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRCT) == 0):
            ratioRazCaptTrab = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonCapitalTrabajo, codEmpresa_id=codEmpresa, año=año)
            ratioRazCaptTrab.save()

        # -> Ratio Razon de Efectivo
        codRatio="RE"
        comprobarRE = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRE) == 0):
            ratioRazEfectivo = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonEfectivo, codEmpresa_id=codEmpresa, año=año)
            ratioRazEfectivo.save()


    #FIN PROCEDIMIENTO DE CALCULO DE RATIOS.

        #Para imprimir los ratios de está razón
        recuperar = RatiosEmpresa.objects.filter(codEmpresa_id=codEmpresa, año=año).order_by('codRatio')
        empresa = Empresa.objects.get(codEmpresa=codEmpresa)
        razon = "LIQ"
        consulta=[]
        i=0
        while(i < len(recuperar)):
            prueba = recuperar[i].codRatio.codRazon_id
            print(prueba)
            if( prueba == razon):
                consulta.append((recuperar[i]))
                print(consulta)
            i+=1

        print(" ")
        print(consulta)

        contexto = {
            'queryset': queryset,
            'consulta': consulta, 
            'empresa': empresa,
            'año': año,
        }

        return render(
            request,
            'proyecto/ConsultaRazonLiquidez.html',
            contexto
        )


#--------------------------------------------------------------------------------------------------------------------------------------------


def consultarRazonApalancamiento(request):
    return render(
        request,
        'proyecto/ConsultaRazonApalancamiento.html'
    )



def ratiosApalancamiento(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']
        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año)

        #Por si no existe el balance de ese año que no me de error
        if (len(queryset) == 0):
            contexto = {
                'queryset': queryset, 
            }
            return render(
                request,
                'proyecto/ConsultaRazonApalancamiento.html', contexto
            )

    #PROCEDIMIENTO DE CALCULO DE RATIOS.

        #Recuperacion de valores para el año solicitado
        i=0
        while(i < len(queryset)):
            tipo = queryset[i].codCuenta.codTipoCuenta_id
            if(tipo == "EFEC"):
                efectivo = queryset[i].valor
            elif(tipo == "INV"):
                inventario = queryset[i].valor
            elif(tipo == "ACCIR"):
                actCirculante = queryset[i].valor
            elif(tipo == "PASTOT"):
                pasivoTotal = queryset[i].valor
            elif(tipo == "COSVEN"):
                costoVentas = queryset[i].valor
            elif(tipo == "CxC"):
                cuentasXCobrar = queryset[i].valor
            elif(tipo == "ACFI"):
                activoFijo = queryset[i].valor
            elif(tipo == "ACTO"):
                activoTotal = queryset[i].valor
            elif(tipo == "PASCIR"):
                pasivoCirc = queryset[i].valor
            elif(tipo == "CxP"):
                cuentasXPagar = queryset[i].valor
            elif(tipo == "PATR"):
                patrimonio = queryset[i].valor
            elif(tipo == "UTBR"):
                utilidadBruta = queryset[i].valor
            elif(tipo == "ING"):
                ingresos = queryset[i].valor
            elif(tipo == "UTOP"):
                utilidadOperativa = queryset[i].valor
            elif(tipo == "GASTFI"):
                gastosFijo = queryset[i].valor
            elif(tipo == "UTAI"):
                utilidadAntesImp = queryset[i].valor
            elif(tipo == "UTNET"):
                utilidadNeta = queryset[i].valor
                
            i+=1
        
        #Calculo de los Ratios
        gradoEndeudamiento = pasivoTotal / activoTotal

        gradoPropiedad = patrimonio / activoTotal

        razonEndeudaPatrimonial = pasivoTotal / patrimonio

        razonCoberturaGastFinanc = utilidadAntesImp / gastosFijo
        

        #Guardar en BD los Ratios

        # -> Ratio Grado de Endeudamiento
        codRatio="GE"
        comprobarGE = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarGE) == 0):
            ratioGradoEndeuda = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=gradoEndeudamiento, codEmpresa_id=codEmpresa, año=año)
            ratioGradoEndeuda.save()

        # -> Ratio Grado de Propiedad
        codRatio="GP"
        comprobarGP = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarGP) == 0):
            ratioGradoProp = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=gradoPropiedad, codEmpresa_id=codEmpresa, año=año)
            ratioGradoProp.save()
        
        # -> Ratio Razon de Cobertura de Gastos Financieros
        codRatio="RCGF"
        comprobarRCGF = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRCGF) == 0):
            ratioRazCobertGastFin = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonCoberturaGastFinanc, codEmpresa_id=codEmpresa, año=año)
            ratioRazCobertGastFin.save()

        # -> Ratio Razon de Endeudamiento Patrimonial
        codRatio="REP"
        comprobarREP = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarREP) == 0):
            ratioRazEndeudaPatr = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonEndeudaPatrimonial, codEmpresa_id=codEmpresa, año=año)
            ratioRazEndeudaPatr.save()


    #FIN PROCEDIMIENTO DE CALCULO DE RATIOS.

        #Para imprimir los ratios de está razón
        recuperar = RatiosEmpresa.objects.filter(codEmpresa_id=codEmpresa, año=año).order_by('codRatio')
        empresa = Empresa.objects.get(codEmpresa=codEmpresa)
        razon = "APA"
        consulta=[]
        i=0
        while(i < len(recuperar)):
            prueba = recuperar[i].codRatio.codRazon_id
            print(prueba)
            if( prueba == razon):
                consulta.append((recuperar[i]))
                print(consulta)
            i+=1

        print(" ")
        print(consulta)

        contexto = {
            'queryset': queryset,
            'consulta': consulta, 
            'empresa': empresa,
            'año': año,
        }

        return render(
            request,
            'proyecto/ConsultaRazonApalancamiento.html',
            contexto
        )


#--------------------------------------------------------------------------------------------------------------------------------------------


def consultarRazonRentabilidad(request):
    return render(
        request,
        'proyecto/ConsultaRazonRentabilidad.html'
    )



def ratiosRentabilidad(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']
        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año)

        #Por si no existe el balance de ese año que no me de error
        if (len(queryset) == 0):
            contexto = {
                'queryset': queryset, 
            }
            return render(
                request,
                'proyecto/ConsultaRazonRentabilidad.html', contexto
            )

        #Obtengo los datos del año anterior para sacar Promedio
        año2 = int(año) - 1
        queryset2 = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año2)

    #PROCEDIMIENTO DE CALCULO DE RATIOS.

        #Recuperacion de valores para el año solicitado
        i=0
        while(i < len(queryset)):
            tipo = queryset[i].codCuenta.codTipoCuenta_id
            if(tipo == "EFEC"):
                efectivo = queryset[i].valor
            elif(tipo == "INV"):
                inventario = queryset[i].valor
            elif(tipo == "ACCIR"):
                actCirculante = queryset[i].valor
            elif(tipo == "PASTOT"):
                pasivoTotal = queryset[i].valor
            elif(tipo == "COSVEN"):
                costoVentas = queryset[i].valor
            elif(tipo == "CxC"):
                cuentasXCobrar = queryset[i].valor
            elif(tipo == "ACFI"):
                activoFijo = queryset[i].valor
            elif(tipo == "ACTO"):
                activoTotal = queryset[i].valor
            elif(tipo == "PASCIR"):
                pasivoCirc = queryset[i].valor
            elif(tipo == "CxP"):
                cuentasXPagar = queryset[i].valor
            elif(tipo == "PATR"):
                patrimonio = queryset[i].valor
            elif(tipo == "UTBR"):
                utilidadBruta = queryset[i].valor
            elif(tipo == "ING"):
                ingresos = queryset[i].valor
            elif(tipo == "UTOP"):
                utilidadOperativa = queryset[i].valor
            elif(tipo == "GASTFI"):
                gastosFijo = queryset[i].valor
            elif(tipo == "UTAI"):
                utilidadAntesImp = queryset[i].valor
            elif(tipo == "UTNET"):
                utilidadNeta = queryset[i].valor
                
            i+=1

        #Recuperacion de valores para el año anterior para sacar el Promedio
        if( len(queryset2) != 0):
            activoTotal2 = 0
            patrimonio2 = 0

            j=0
            while(j < len(queryset2)):
                tipo2 = queryset2[j].codCuenta.codTipoCuenta_id
                if(tipo2 == "EFEC"):
                    efectivo2 = queryset2[j].valor
                elif(tipo2 == "INV"):
                    inventario2 = queryset2[j].valor
                elif(tipo2 == "ACCIR"):
                    actCirculante2 = queryset2[j].valor
                elif(tipo2 == "PASTOT"):
                    pasivoTotal2 = queryset2[j].valor
                elif(tipo2 == "COSVEN"):
                    costoVentas2 = queryset2[j].valor
                elif(tipo2 == "CxC"):
                    cuentasXCobrar2 = queryset2[j].valor
                elif(tipo2 == "ACFI"):
                    activoFijo2 = queryset2[j].valor
                elif(tipo2 == "ACTO"):
                    activoTotal2 = queryset2[j].valor
                elif(tipo2 == "PASCIR"):
                    pasivoCirc2 = queryset2[j].valor
                elif(tipo2 == "CxP"):
                    cuentasXPagar2 = queryset2[j].valor
                elif(tipo2 == "PATR"):
                    patrimonio2 = queryset2[j].valor
                elif(tipo2 == "UTBR"):
                    utilidadBruta2 = queryset2[j].valor
                elif(tipo2 == "ING"):
                    ingresos2 = queryset2[j].valor
                elif(tipo2 == "UTOP"):
                    utilidadOperativa2 = queryset2[j].valor
                elif(tipo2 == "GASTFI"):
                    gastosFijo2 = queryset2[j].valor
                elif(tipo2 == "UTAI"):
                    utilidadAntesImp2 = queryset2[j].valor
                elif(tipo2 == "UTNET"):
                    utilidadNeta2 = queryset2[j].valor

                j+=1
        
            
            #Calculo de las cuentas que se usan en Promedio
            if(activoTotal2 > 0):
                activoTotalPromedio = (activoTotal2 + activoTotal) / 2
            else:
                activoTotalPromedio = activoTotal

            if(patrimonio2 > 0):
                patrimonioPromedio = (patrimonio2 + patrimonio) / 2
            else:
                patrimonioPromedio = patrimonio
            
        else:
            #En caso que no haya registros de años anteriores
            activoTotalPromedio = activoTotal
            patrimonioPromedio = patrimonio
        
        #Calculo de los Ratios
        razonRentNetaPatr = (utilidadNeta / patrimonioPromedio) * 100

        razonRentActivo = (utilidadNeta / activoTotalPromedio) * 100

        razonRentVentas = (utilidadNeta / ingresos) * 100

        razonRentInv = ((ingresos - costoVentas) / costoVentas) * 100
        
        #razonRentxAccion = utilidadNeta / numeroAcciones
        

        #Guardar en BD los Ratios

        # -> Ratio Rentabilidad Neta del Patrimonio
        codRatio="RNP"
        comprobarRNP = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRNP) == 0):
            ratioRentNetaPatr = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRentNetaPatr , codEmpresa_id=codEmpresa, año=año)
            ratioRentNetaPatr.save()
        
        # -> Ratio Rentabilidad del Activo
        codRatio="RDAC"
        comprobarRDAC = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRDAC) == 0):
            ratioRentActivo = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRentActivo , codEmpresa_id=codEmpresa, año=año)
            ratioRentActivo.save()

        # -> Ratio Razon de Rentabilidad Sobre las Ventas
        codRatio="RSV"
        comprobarRSV = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRSV) == 0):
            ratioRentSobreVent= RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRentVentas , codEmpresa_id=codEmpresa, año=año)
            ratioRentSobreVent.save()
        
        # -> Ratio Razon de Rentabilidad Sobre la Inversión
        codRatio="RSI"
        comprobarRSI = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRSI) == 0):
            ratioRentSobreInv = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRentInv , codEmpresa_id=codEmpresa, año=año)
            ratioRentSobreInv.save()


    #FIN PROCEDIMIENTO DE CALCULO DE RATIOS.
        
        #Para imprimir los ratios de está razón
        recuperar = RatiosEmpresa.objects.filter(codEmpresa_id=codEmpresa, año=año).order_by('codRatio')
        empresa = Empresa.objects.get(codEmpresa=codEmpresa)
        razon = "REN"
        consulta=[]
        i=0
        while(i < len(recuperar)):
            prueba = recuperar[i].codRatio.codRazon_id
            if(  prueba == razon):
                consulta.append((recuperar[i]))
            i+=1

        contexto = {
            'queryset': queryset,
            'consulta': consulta, 
            'empresa': empresa,
            'año': año,
        }

        return render(
            request,
            'proyecto/ConsultaRazonRentabilidad.html', 
            contexto
        )


#--------------------------------------------------------------------------------------------------------------------------------------------


def consultarAnalisisDupont(request):
    return render(
        request,
        'proyecto/ConsultaAnalisisDupont.html'
    )



def analisisDupont(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']
        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año)

        #Por si no existe el balance de ese año que no me de error
        if (len(queryset) == 0):
            contexto = {
                'queryset': queryset, 
            }
            return render(
                request,
                'proyecto/ConsultaAnalisisDupont.html', contexto
            )

        #Obtengo los datos del año anterior para sacar Promedio
        año2 = int(año) - 1
        queryset2 = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año2)


    #PROCEDIMIENTO DE CALCULO DE RATIOS.

        #Recuperacion de valores para el año solicitado
        i=0
        while(i < len(queryset)):
            tipo = queryset[i].codCuenta.codTipoCuenta_id
            if(tipo == "EFEC"):
                efectivo = queryset[i].valor
            elif(tipo == "INV"):
                inventario = queryset[i].valor
            elif(tipo == "ACCIR"):
                actCirculante = queryset[i].valor
            elif(tipo == "PASTOT"):
                pasivoTotal = queryset[i].valor
            elif(tipo == "COSVEN"):
                costoVentas = queryset[i].valor
            elif(tipo == "CxC"):
                cuentasXCobrar = queryset[i].valor
            elif(tipo == "ACFI"):
                activoFijo = queryset[i].valor
            elif(tipo == "ACTO"):
                activoTotal = queryset[i].valor
            elif(tipo == "PASCIR"):
                pasivoCirc = queryset[i].valor
            elif(tipo == "CxP"):
                cuentasXPagar = queryset[i].valor
            elif(tipo == "PATR"):
                patrimonio = queryset[i].valor
            elif(tipo == "UTBR"):
                utilidadBruta = queryset[i].valor
            elif(tipo == "ING"):
                ingresos = queryset[i].valor
            elif(tipo == "UTOP"):
                utilidadOperativa = queryset[i].valor
            elif(tipo == "GASTFI"):
                gastosFijo = queryset[i].valor
            elif(tipo == "UTAI"):
                utilidadAntesImp = queryset[i].valor
            elif(tipo == "UTNET"):
                utilidadNeta = queryset[i].valor
                
            i+=1
        
        #Recuperacion de valores para el año anterior para sacar el Promedio
        if( len(queryset2) != 0):
            activoTotal2 = 0
            patrimonio2 = 0

            j=0
            while(j < len(queryset2)):
                tipo2 = queryset2[j].codCuenta.codTipoCuenta_id
                if(tipo2 == "EFEC"):
                    efectivo2 = queryset2[j].valor
                elif(tipo2 == "INV"):
                    inventario2 = queryset2[j].valor
                elif(tipo2 == "ACCIR"):
                    actCirculante2 = queryset2[j].valor
                elif(tipo2 == "PASTOT"):
                    pasivoTotal2 = queryset2[j].valor
                elif(tipo2 == "COSVEN"):
                    costoVentas2 = queryset2[j].valor
                elif(tipo2 == "CxC"):
                    cuentasXCobrar2 = queryset2[j].valor
                elif(tipo2 == "ACFI"):
                    activoFijo2 = queryset2[j].valor
                elif(tipo2 == "ACTO"):
                    activoTotal2 = queryset2[j].valor
                elif(tipo2 == "PASCIR"):
                    pasivoCirc2 = queryset2[j].valor
                elif(tipo2 == "CxP"):
                    cuentasXPagar2 = queryset2[j].valor
                elif(tipo2 == "PATR"):
                    patrimonio2 = queryset2[j].valor
                elif(tipo2 == "UTBR"):
                    utilidadBruta2 = queryset2[j].valor
                elif(tipo2 == "ING"):
                    ingresos2 = queryset2[j].valor
                elif(tipo2 == "UTOP"):
                    utilidadOperativa2 = queryset2[j].valor
                elif(tipo2 == "GASTFI"):
                    gastosFijo2 = queryset2[j].valor
                elif(tipo2 == "UTAI"):
                    utilidadAntesImp2 = queryset2[j].valor
                elif(tipo2 == "UTNET"):
                    utilidadNeta2 = queryset2[j].valor

                j+=1
        
            #Calculo de las cuentas que se usan en Promedio
            if(activoTotal2 > 0):
                activoTotalPromedio = (activoTotal2 + activoTotal) / 2
            else:
                activoTotalPromedio = activoTotal

            if(patrimonio2 > 0):
                patrimonioPromedio = (patrimonio2 + patrimonio) / 2
            else:
                patrimonioPromedio = patrimonio
            
        else:
            #En caso que no haya registros de años anteriores
            activoTotalPromedio = activoTotal
            patrimonioPromedio = patrimonio
        
        
        #Calculo de los Ratios
        margenNeto = utilidadNeta / ingresos

        rotacionActivos = ingresos / activoTotalPromedio

        multiplicadorCapital = activoTotalPromedio / patrimonioPromedio

        roe = margenNeto * rotacionActivos * multiplicadorCapital

        roa = utilidadNeta / activoTotalPromedio
        

        #Guardar en BD los Ratios

        # -> Ratio Margen Neto
        codRatio="MN"
        comprobarMN = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarMN) == 0):
            ratioMargenNeto = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=margenNeto, codEmpresa_id=codEmpresa, año=año)
            ratioMargenNeto.save()

        # -> Ratio Rotacion de Activos
        codRatio="RDA"
        comprobarRDA = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRDA) == 0):
            ratioRotacAct = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=rotacionActivos, codEmpresa_id=codEmpresa, año=año)
            ratioRotacAct.save()
        
        # -> Ratio Multiplicador de Capital
        codRatio="MDC"
        comprobarMDC = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarMDC) == 0):
            ratioMultCap = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=multiplicadorCapital, codEmpresa_id=codEmpresa, año=año)
            ratioMultCap.save()

        # -> ROE
        codRatio="ROE"
        comprobarROE = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarROE) == 0):
            ratioROE = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=roe, codEmpresa_id=codEmpresa, año=año)
            ratioROE.save()

        # -> ROA
        codRatio="ROA"
        comprobarROA = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarROA) == 0):
            ratioROA = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=roa, codEmpresa_id=codEmpresa, año=año)
            ratioROA.save()


    #FIN PROCEDIMIENTO DE CALCULO DE RATIOS.

        #Para imprimir los ratios de está razón
        recuperar = RatiosEmpresa.objects.filter(codEmpresa_id=codEmpresa, año=año).order_by('codRatio')
        empresa = Empresa.objects.get(codEmpresa=codEmpresa)
        razon = "AND"
        consulta=[]
        i=0
        while(i < len(recuperar)):
            prueba = recuperar[i].codRatio.codRazon_id
            print(prueba)
            if( prueba == razon):
                consulta.append((recuperar[i]))
                print(consulta)
            i+=1

        print(" ")
        print(consulta)

        contexto = {
            'queryset': queryset,
            'consulta': consulta, 
            'empresa': empresa,
            'año': año,
        }

        return render(
            request,
            'proyecto/ConsultaAnalisisDupont.html',
            contexto
        )


#--------------------------------------------------------------------------------------------------------------------------------------------


def consultarAnalisisHorizontal(request):
    return render(
        request,
        'proyecto/ConsultaAnalisisHorizontal.html'
    )



def analisisHorizontal(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']
        añoActual = int(año)
        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año)

        #Por si no existe el balance de ese año que no me de error
        if (len(queryset) == 0):
            contexto = {
                'queryset': queryset, 
            }
            return render(
                request,
                'proyecto/ConsultaAnalisisHorizontal.html', contexto
            )

        #Obtengo los datos del año anterior para sacar Promedio
        año2 = int(año) - 1
        queryset2 = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año2)

        #Por si no existe el balance del año anterior que termine
        if (len(queryset2) == 0):
            contexto = {
                'queryset2': queryset2, 
            }
            return render(
                request,
                'proyecto/ConsultaAnalisisHorizontal.html', contexto
            )


    #PROCEDIMIENTO DE CALCULO DE ANALISIS HORIZONTAL.

        #Recuperacion de valores para el año solicitado
        absoluta = []
        i=0
        while(i < len(queryset)):
            codCuenta = queryset[i].codCuenta

            valor1 = queryset[i].valor
            valor2 = queryset2[i].valor
            valorAbsoluto = valor1 - valor2
            valorRelativo = (valorAbsoluto / valor2) * 100
            #absoluta.append((valor, queryset[i].año, queryset[i].codEmpresa ))

            comprobar = AnalisisHorizontal.objects.filter(codEmpresa_id=codEmpresa, codCuenta_id=codCuenta, añoActual=año)
            if(len(comprobar) == 0):
                analisisHorizontal = AnalisisHorizontal(codEmpresa_id=codEmpresa, codCuenta_id=codCuenta, añoActual=añoActual, valorActual=valor1, añoAnterior=año2, valorAnterior=valor2, valorAbsoluto=valorAbsoluto, valorRelativo=valorRelativo)
                analisisHorizontal.save()
            
            i+=1
       
    #FIN PROCEDIMIENTO DE CALCULO DE ANALISIS HORIZONTAL.

        #Para Imprimir
        analHoriz = AnalisisHorizontal.objects.filter(codEmpresa=codEmpresa, añoActual=año).order_by('codCuenta')
        empresa = Empresa.objects.get(codEmpresa=codEmpresa)

        contexto = {
            'queryset': queryset,
            'analHoriz': analHoriz,
            'empresa': empresa,
            'año': año,
            'año2': año2,
        }

        return render(
            request,
            'proyecto/ConsultaAnalisisHorizontal.html',
            contexto
        )


#--------------------------------------------------------------------------------------------------------------------------------------------


def consultarAnalisisVertical(request):
    return render(
        request,
        'proyecto/ConsultaAnalisisVertical.html'
    )



def analisisVertical(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']
        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año)

        #Por si no existe el balance de ese año que no me de error
        if (len(queryset) == 0):
            contexto = {
                'queryset': queryset, 
            }
            return render(
                request,
                'proyecto/ConsultaAnalisisVertical.html', contexto
            )


    #PROCEDIMIENTO DE CALCULO DE ANALISIS VERTICAL.

        #Recuperacion de valores para el año solicitado
        i=0
        while(i < len(queryset)):
            tipo = queryset[i].codCuenta.codTipoCuenta_id
            if(tipo == "EFEC"):
                efectivo = queryset[i].valor
            elif(tipo == "INV"):
                inventario = queryset[i].valor
            elif(tipo == "ACCIR"):
                actCirculante = queryset[i].valor
            elif(tipo == "PASTOT"):
                pasivoTotal = queryset[i].valor
            elif(tipo == "COSVEN"):
                costoVentas = queryset[i].valor
            elif(tipo == "CxC"):
                cuentasXCobrar = queryset[i].valor
            elif(tipo == "ACFI"):
                activoFijo = queryset[i].valor
            elif(tipo == "ACTO"):
                activoTotal = queryset[i].valor
            elif(tipo == "PASCIR"):
                pasivoCirc = queryset[i].valor
            elif(tipo == "CxP"):
                cuentasXPagar = queryset[i].valor
            elif(tipo == "PATR"):
                patrimonio = queryset[i].valor
            elif(tipo == "UTBR"):
                utilidadBruta = queryset[i].valor
            elif(tipo == "ING"):
                ingresos = queryset[i].valor
            elif(tipo == "UTOP"):
                utilidadOperativa = queryset[i].valor
            elif(tipo == "GASTFI"):
                gastosFijo = queryset[i].valor
            elif(tipo == "UTAI"):
                utilidadAntesImp = queryset[i].valor
            elif(tipo == "UTNET"):
                utilidadNeta = queryset[i].valor
                
            i+=1

        #Recuperacion de valores para el año solicitado
        i=0
        while(i < len(queryset)):
            rubro = queryset[i].codCuenta.codRubro_id

            if(rubro == "ACT"):
                valor = queryset[i].valor
                cuenta = queryset[i].codCuenta
                resultado = (valor / activoTotal) * 100

                comprobar = AnalisisVertical.objects.filter(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año)
                if(len(comprobar) == 0):
                    analisisVertical = AnalisisVertical(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año, valor=resultado, codRubro_id=rubro)
                    analisisVertical.save()

            elif(rubro == "PAS"):
                valor = queryset[i].valor
                cuenta = queryset[i].codCuenta
                resultado = (valor / pasivoTotal) * 100

                comprobar = AnalisisVertical.objects.filter(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año)
                if(len(comprobar) == 0):
                    analisisVertical = AnalisisVertical(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año, valor=resultado, codRubro_id=rubro)
                    analisisVertical.save()

            elif(rubro == "UTL"):
                valor = queryset[i].valor
                cuenta = queryset[i].codCuenta
                resultado = (valor / ingresos) * 100

                comprobar = AnalisisVertical.objects.filter(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año)
                if(len(comprobar) == 0):
                    analisisVertical = AnalisisVertical(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año, valor=resultado, codRubro_id=rubro)
                    analisisVertical.save()
            
            i+=1

    #FIN PROCEDIMIENTO DE CALCULO DE ANALISIS VERTICAL.

        #Para Imprimir
        analVert = AnalisisVertical.objects.filter(codEmpresa=codEmpresa, año=año).order_by('codRubro', 'codCuenta')
        empresa = Empresa.objects.get(codEmpresa=codEmpresa)

        contexto = {
            'queryset': queryset,
            'analVert': analVert,
            'empresa': empresa,
            'año': año,
        }

        return render(
            request,
            'proyecto/ConsultaAnalisisVertical.html',
            contexto
        )


#--------------------------------------------------------------------------------------------------------------------------------------------
 #CATALAGO DE CUENTAS

#def catalago_view(request):
 #   if request.method == 'POST':
  #      form = CatalagoCuentaForm(request.POST)
   #     if form.is_valid():
    #        form.save()
     #   return redirect('index')
    #else:
     #   form = CatalagoCuentaForm()
#
 #   return render(request, 'proyecto/crearCatalogo.hmtl', {'form':form})


class CatalogoListado(ListView):
    model = CatalogoCuenta #Llamada a la clase "CatalogoCuenta" en el archivo models.py

class CatalogoCrear(SuccessMessageMixin, CreateView):
    model = CatalogoCuenta #Llamada a la clase "CatalogoCuenta" en el archivo models.py
    form = CatalogoCuentaForm #Definición del formulario ubicado en forms.py
    fields = "__all__" #Le decimos a Django que muestre todos los campos de la tabla de nuestra Base de Datos
    success_message='--Catalogo Creado Correctamente--' #Muestra el mensaje si se ha realizado correctamente la operación

    def get_success_url(self):
        return reverse('analisisFinanciero:catalogo')

class CatalogoDetalle(DetailView):
    model = CatalogoCuenta 

class CatalogoActualizar(SuccessMessageMixin, UpdateView): 
    model = CatalogoCuenta 
    form = CatalogoCuentaForm 
    fields = "__all__" 
    success_message = '--Catalogo Actualizado Correctamente--' 
 
    
    def get_success_url(self):               
        return reverse('analisisFinanciero:catalogo') 

class CatalogoEliminar(SuccessMessageMixin, DeleteView): 
    model = CatalogoCuenta
    form = CatalogoCuentaForm
    fields = "__all__"     
 
    # Redireccionamos a la página principal luego de eliminar un registro 
    def get_success_url(self): 
        success_message = '--Catalogo Eliminado Correctamente--' 
        messages.success (self.request, (success_message))       
        return reverse('analisisFinanciero:catalogo') 