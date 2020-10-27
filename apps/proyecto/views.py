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
from .models import *
from .forms import *
from django.conf import settings

import tablib
from tablib import Dataset
from .resources import *


#Vista para el menu base
def index(request):
    return render(
        request,
        'base/base.html'
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



def consultarBalance(request):
    return render(
        request,
        'proyecto/ConsultaBalance.html'
    )



def filtrarBalance(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']

        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año).order_by('codCuenta')

        contexto = {
            'queryset': queryset, 
        }

        return render(
            request,
            'proyecto/ConsultaBalance.html', contexto
        )



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

        consulta = RatiosEmpresa.objects.filter(codEmpresa_id=codEmpresa, año=año).order_by('codRatio')

        contexto = {
            'queryset': queryset,
            'consulta': consulta, 
        }

        return render(
            request,
            'proyecto/ConsultaRazonActividad.html', contexto
        )



