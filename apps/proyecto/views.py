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
from apps.usuario.models import *
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

def consultarBalance(request, username):

    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        querysetRA =Empresa.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        querysetRA= Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
            'querysetRA':querysetRA,
    } 
    return render(request,'proyecto/ConsultaBalance.html', contexto)

def filtrarBalance(request):
    if request.method == 'POST':

        codEmpresa = request.POST['codEmpresa']
        año = request.POST['año']

        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año).order_by('codCuenta')

        if (len(queryset) == 0):
            contexto = {
                'queryset': queryset, 
                'año': año,
            }

            return render(
                request,
                'proyecto/ConsultaBalance.html', contexto
            )
        else:
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

def consultarRazonActividad(request, username):

    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        querysetRA =Empresa.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        querysetRA= Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
            'querysetRA':querysetRA,
    } 
    return render(request,'proyecto/ConsultaRazonActividad.html', contexto)



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
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonRotInve
            obtenerRRI.save()
        
        # -> Ratio Razon de Dias de Inventario
        codRatio="RDI"
        comprobarRDI = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRDI) == 0):
            ratioRazDiasInven = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonDiasInve , codEmpresa_id=codEmpresa, año=año)
            ratioRazDiasInven.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonDiasInve
            obtenerRRI.save()

        # -> Ratio Razon de Rotacion C x C
        codRatio="RRCC"
        comprobarRRCC = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRRCC) == 0):
            ratioRazRotCxC = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRotCxC , codEmpresa_id=codEmpresa, año=año)
            ratioRazRotCxC.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonRotCxC
            obtenerRRI.save()
        
        # -> Ratio Razon de Periodo Medio de Cobranza
        codRatio="RPMC"
        comprobarRPMC = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRPMC) == 0):
            ratioRazPerMedCobr = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonPerMedCobro , codEmpresa_id=codEmpresa, año=año)
            ratioRazPerMedCobr.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonPerMedCobro
            obtenerRRI.save()
        
        # -> Ratio Razon de Rotacion de Cuentas por Pagar
        codRatio="RRCP"
        comprobarRRCP = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRRCP) == 0):
            ratioRazRotCxP = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRotCxP , codEmpresa_id=codEmpresa, año=año)
            ratioRazRotCxP.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonRotCxP
            obtenerRRI.save()

        # -> Ratio Razon de Periodo Medio de Pago
        codRatio="RPMP"
        comprobarRPMP = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRPMP) == 0):
            ratioRazPerMedPago = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonPerMedPago , codEmpresa_id=codEmpresa, año=año)
            ratioRazPerMedPago.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonPerMedPago
            obtenerRRI.save()

        # -> Ratio Razon de Indice de Rotacion de Activos Totales
        codRatio="IRAT"
        comprobarIRAT = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarIRAT) == 0):
            ratioIndiceRotActTot = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=indiceRotActTot , codEmpresa_id=codEmpresa, año=año)
            ratioIndiceRotActTot.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = indiceRotActTot
            obtenerRRI.save()
        
        # -> Ratio Razon de Indice de Rotacion de Activos Fijos
        codRatio="IRAF"
        comprobarIRAF = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarIRAF) == 0):
            ratioIndiceRotActFij = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=indiceRotActFij , codEmpresa_id=codEmpresa, año=año)
            ratioIndiceRotActFij.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = indiceRotActFij
            obtenerRRI.save()

        # -> Ratio Razon de Indice de Margen Bruto
        codRatio="IMB"
        comprobarIMB = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarIMB) == 0):
            ratioIndiceMargenBruto = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=indiceMargenBruto , codEmpresa_id=codEmpresa, año=año)
            ratioIndiceMargenBruto.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = indiceMargenBruto
            obtenerRRI.save()
        
        # -> Ratio Razon de Indice de Margen Operativo
        codRatio="IMO"
        comprobarIMO = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarIMO) == 0):
            ratioIndiceMargenOper = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=indiceMargenOperativo , codEmpresa_id=codEmpresa, año=año)
            ratioIndiceMargenOper.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = indiceMargenOperativo
            obtenerRRI.save()


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

def consultarRazonLiquidez(request, username):

    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        querysetRA =Empresa.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        querysetRA= Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
            'querysetRA':querysetRA,
    } 
    return render(request,'proyecto/ConsultaRazonLiquidez.html', contexto)


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
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonCirculante
            obtenerRRI.save()

        # -> Ratio Razon Rápida
        codRatio="RR"
        comprobarRR = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRR) == 0):
            ratioRazRapida = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRapida, codEmpresa_id=codEmpresa, año=año)
            ratioRazRapida.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonRapida
            obtenerRRI.save()
        
        # -> Ratio Razon de Capital de Trabajo
        codRatio="RCT"
        comprobarRCT = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRCT) == 0):
            ratioRazCaptTrab = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonCapitalTrabajo, codEmpresa_id=codEmpresa, año=año)
            ratioRazCaptTrab.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonCapitalTrabajo
            obtenerRRI.save()

        # -> Ratio Razon de Efectivo
        codRatio="RE"
        comprobarRE = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRE) == 0):
            ratioRazEfectivo = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonEfectivo, codEmpresa_id=codEmpresa, año=año)
            ratioRazEfectivo.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonEfectivo
            obtenerRRI.save()


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


def consultarRazonApalancamiento(request, username):

    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        querysetRA =Empresa.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        querysetRA= Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
            'querysetRA':querysetRA,
    } 
    return render(request,'proyecto/ConsultaRazonApalancamiento.html', contexto)



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
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = gradoEndeudamiento
            obtenerRRI.save()

        # -> Ratio Grado de Propiedad
        codRatio="GP"
        comprobarGP = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarGP) == 0):
            ratioGradoProp = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=gradoPropiedad, codEmpresa_id=codEmpresa, año=año)
            ratioGradoProp.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = gradoPropiedad
            obtenerRRI.save()
        
        # -> Ratio Razon de Cobertura de Gastos Financieros
        codRatio="RCGF"
        comprobarRCGF = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRCGF) == 0):
            ratioRazCobertGastFin = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonCoberturaGastFinanc, codEmpresa_id=codEmpresa, año=año)
            ratioRazCobertGastFin.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonCoberturaGastFinanc
            obtenerRRI.save()

        # -> Ratio Razon de Endeudamiento Patrimonial
        codRatio="REP"
        comprobarREP = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarREP) == 0):
            ratioRazEndeudaPatr = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonEndeudaPatrimonial, codEmpresa_id=codEmpresa, año=año)
            ratioRazEndeudaPatr.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonEndeudaPatrimonial
            obtenerRRI.save()


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


def consultarRazonRentabilidad(request, username):

    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        querysetRA =Empresa.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        querysetRA= Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
            'querysetRA':querysetRA,
    } 
    return render(request,'proyecto/ConsultaRazonRentabilidad.html', contexto)



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
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonRentNetaPatr
            obtenerRRI.save()
        
        # -> Ratio Rentabilidad del Activo
        codRatio="RDAC"
        comprobarRDAC = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRDAC) == 0):
            ratioRentActivo = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRentActivo , codEmpresa_id=codEmpresa, año=año)
            ratioRentActivo.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonRentActivo
            obtenerRRI.save()

        # -> Ratio Razon de Rentabilidad Sobre las Ventas
        codRatio="RSV"
        comprobarRSV = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRSV) == 0):
            ratioRentSobreVent= RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRentVentas , codEmpresa_id=codEmpresa, año=año)
            ratioRentSobreVent.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonRentVentas
            obtenerRRI.save()
        
        # -> Ratio Razon de Rentabilidad Sobre la Inversión
        codRatio="RSI"
        comprobarRSI = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRSI) == 0):
            ratioRentSobreInv = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRentInv , codEmpresa_id=codEmpresa, año=año)
            ratioRentSobreInv.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = razonRentInv
            obtenerRRI.save()


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


def consultarAnalisisDupont(request, username):

    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        querysetRA =Empresa.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        querysetRA= Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
            'querysetRA':querysetRA,
    } 
    return render(request,'proyecto/ConsultaAnalisisDupont.html', contexto)


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
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = margenNeto
            obtenerRRI.save()

        # -> Ratio Rotacion de Activos
        codRatio="RDA"
        comprobarRDA = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarRDA) == 0):
            ratioRotacAct = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=rotacionActivos, codEmpresa_id=codEmpresa, año=año)
            ratioRotacAct.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = rotacionActivos
            obtenerRRI.save()
        
        # -> Ratio Multiplicador de Capital
        codRatio="MDC"
        comprobarMDC = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarMDC) == 0):
            ratioMultCap = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=multiplicadorCapital, codEmpresa_id=codEmpresa, año=año)
            ratioMultCap.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = multiplicadorCapital
            obtenerRRI.save()

        # -> ROE
        codRatio="ROE"
        comprobarROE = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarROE) == 0):
            ratioROE = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=roe, codEmpresa_id=codEmpresa, año=año)
            ratioROE.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = roe
            obtenerRRI.save()

        # -> ROA
        codRatio="ROA"
        comprobarROA = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobarROA) == 0):
            ratioROA = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=roa, codEmpresa_id=codEmpresa, año=año)
            ratioROA.save()
        else:
            obtenerRRI = RatiosEmpresa.objects.get(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
            obtenerRRI.valorRatioEmpresa = roa
            obtenerRRI.save()


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


def consultarAnalisisHorizontal(request, username):

    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        querysetRA =Empresa.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        querysetRA= Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
            'querysetRA':querysetRA,
    } 
    return render(request,'proyecto/ConsultaAnalisisHorizontal.html', contexto)


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
            else:
                obtenerRRI = AnalisisHorizontal.objects.get(codEmpresa_id=codEmpresa, codCuenta_id=codCuenta, añoActual=año)
                obtenerRRI.valorActual = valor1
                obtenerRRI.añoAnterior = año2
                obtenerRRI.valorAnterior = valor2
                obtenerRRI.valorAbsoluto = valorAbsoluto
                obtenerRRI.valorRelativo = valorRelativo
                obtenerRRI.save()
            
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


def consultarAnalisisVertical(request, username):
    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        querysetRA =Empresa.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        querysetRA= Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
            'querysetRA':querysetRA,
    } 
    return render(request,'proyecto/ConsultaAnalisisVertical.html', contexto)



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
                else:
                    obtenerRRI = AnalisisVertical.objects.get(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año)
                    obtenerRRI.valor = resultado
                    obtenerRRI.save()

            elif(rubro == "PAS"):
                valor = queryset[i].valor
                cuenta = queryset[i].codCuenta
                resultado = (valor / pasivoTotal) * 100

                comprobar = AnalisisVertical.objects.filter(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año)
                if(len(comprobar) == 0):
                    analisisVertical = AnalisisVertical(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año, valor=resultado, codRubro_id=rubro)
                    analisisVertical.save()
                else:
                    obtenerRRI = AnalisisVertical.objects.get(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año)
                    obtenerRRI.valor = resultado
                    obtenerRRI.save()

            elif(rubro == "UTL"):
                valor = queryset[i].valor
                cuenta = queryset[i].codCuenta
                resultado = (valor / ingresos) * 100

                comprobar = AnalisisVertical.objects.filter(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año)
                if(len(comprobar) == 0):
                    analisisVertical = AnalisisVertical(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año, valor=resultado, codRubro_id=rubro)
                    analisisVertical.save()
                else:
                    obtenerRRI = AnalisisVertical.objects.get(codEmpresa_id=codEmpresa, codCuenta_id=cuenta, año=año)
                    obtenerRRI.valor = resultado
                    obtenerRRI.save()
            
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


def consultarInformes(request):
    sectorCons = ActividadEconomica.objects.all

    contexto = {
        'actividad': sectorCons,
    }

    return render(
        request,
        'proyecto/InformeAnalisis.html',
        contexto,
    )



def informeAnalisis(request):
    sectorCons = ActividadEconomica.objects.all

    contexto = {
        'actividad': sectorCons,
    }

    if request.method == 'POST':

        codActividadEconomica = request.POST['codActividadEconomica']
        año = request.POST['año']

        sector = ActividadEconomica.objects.filter(codActividadEconomica=codActividadEconomica)
        valRatioSector = RatiosSector.objects.filter(codActividadEconomica=codActividadEconomica)
        empresas = RatiosEmpresa.objects.filter(año=año)

        #CALCULO DEL PROMEDIO PARA CADA SECTOR

        #----LIQ-------
        sumaRC = 0
        sumaRCT = 0
        sumaRE = 0
        sumaRR = 0
        sumaRDAC = 0
        #----ACT-------
        sumaIMB = 0
        sumaIMO = 0
        sumaIRAF = 0
        sumaIRAT = 0
        sumaRDI = 0
        sumaRPMC = 0
        sumaRPMP = 0
        sumaRRCC = 0
        sumaRRCP = 0
        sumaRRI = 0
        #----APA--------
        sumaGE = 0
        sumaGP = 0
        sumaRCGF = 0
        sumaREP = 0
        #----REN--------
        sumaRDAC = 0
        sumaRNP = 0
        sumaRSI = 0
        sumaRSV = 0


        #-------------
        contRC = 1
        contRCT = 1
        contRE = 1
        contRR = 1
        contRDAC = 1
        #-------------
        contIMB = 1
        contIMO = 1
        contIRAF = 1
        contIRAT = 1
        contRDI = 1
        contRPMC = 1
        contRPMP = 1
        contRRCC = 1
        contRRCP = 1
        contRRI = 1
        #-------------
        contGE = 1
        contGP = 1
        contRCGF = 1
        contREP = 1
        #-------------
        contRDAC = 1
        contRNP = 1
        contRSI = 1
        contRSV = 1


        #Guardo la Suma del valor de ese ratio de todas las empresas
        i=0
        while(i < len(empresas)):
            sectorEmpresa = empresas[i].codEmpresa.codActividadEconomica_id
            valorRatio = empresas[i].valorRatioEmpresa
            tipoRatio = empresas[i].codRatio_id

            if(sectorEmpresa == codActividadEconomica):
                if(tipoRatio == "RC"):
                    sumaRC = sumaRC + valorRatio
                    contRC+=1
                elif(tipoRatio == "RCT"):
                    sumaRCT = sumaRCT + valorRatio
                    contRCT+=1
                elif(tipoRatio == "RR"):
                    sumaRR = sumaRE + valorRatio
                    contRR+=1
                elif(tipoRatio == "RE"):
                    sumaRE = sumaRE + valorRatio
                    contRE+=1
                elif(tipoRatio == "RDAC"):
                    sumaRDAC = sumaRDAC + valorRatio
                    contRDAC+=1
                #----------------------------------------
                elif(tipoRatio == "IMB"):
                    sumaIMB = sumaIMB + valorRatio
                    contIMB+=1
                elif(tipoRatio == "IMO"):
                    sumaIMO = sumaIMO + valorRatio
                    contIMO+=1
                elif(tipoRatio == "IRAF"):
                    sumaIRAF = sumaIRAF + valorRatio
                    contIRAF+=1
                elif(tipoRatio == "IRAT"):
                    sumaIRAT = sumaIRAT + valorRatio
                    contIRAT+=1
                elif(tipoRatio == "RDI"):
                    sumaRDI = sumaRDI + valorRatio
                    contRDI+=1
                elif(tipoRatio == "RPMC"):
                    sumaRPMC = sumaRPMC + valorRatio
                    contRPMC+=1
                elif(tipoRatio == "RPMP"):
                    sumaRPMP = sumaRPMP + valorRatio
                    contRPMP+=1
                elif(tipoRatio == "RRCC"):
                    sumaRRCC = sumaRRCC + valorRatio
                    contRRCC+=1
                elif(tipoRatio == "RRCP"):
                    sumaRRCP = sumaRRCP + valorRatio
                    contRRCP+=1
                elif(tipoRatio == "RRI"):
                    sumaRRI = sumaRRI + valorRatio
                    contRRI+=1
                #----------------------------------------
                elif(tipoRatio == "GE"):
                    sumaGE = sumaGE + valorRatio
                    contGE+=1
                elif(tipoRatio == "GP"):
                    sumaGP = sumaGP + valorRatio
                    contGP+=1
                elif(tipoRatio == "RCGF"):
                    sumaRCGF = sumaRCGF + valorRatio
                    contRCGF+=1
                elif(tipoRatio == "REP"):
                    sumaREP = sumaREP + valorRatio
                    contREP+=1
                #----------------------------------------
                elif(tipoRatio == "RDAC"):
                    sumaRDAC = sumaRDAC + valorRatio
                    contRDAC+=1
                elif(tipoRatio == "RNP"):
                    sumaRNP = sumaRNP + valorRatio
                    contRNP+=1
                elif(tipoRatio == "RSI"):
                    sumaRSI = sumaRSI + valorRatio
                    contRSI+=1
                elif(tipoRatio == "RSV"):
                    sumaRSV = sumaRSV + valorRatio
                    contRSV+=1
            i+=1

        # Calculo del Promedio de las empresas
        # Le resto 1 porque lo inicalice a 1 para que no de error de Div/0 cuando no se use en el while
        if(contRC > 1):
            promedioRC = sumaRC / (contRC - 1)
        if(contRCT > 1):
            promedioRCT = sumaRCT / (contRCT - 1)
        if(contRE > 1):
            promedioRE = sumaRE / (contRE - 1)
        if(contRR > 1):
            promedioRR = sumaRR / (contRR - 1)
        if(contRDAC > 1):
            promedioRDAC = sumaRDAC / (contRDAC - 1)
        #-----------------------------------------------
        if(contIMB > 1):
            promedioIMB = sumaIMB / (contIMB - 1)
        if(contIMO > 1):
            promedioIMO = sumaIMO / (contIMO - 1)
        if(contIRAF > 1):
            promedioIRAF = sumaIRAF / (contIRAF - 1)
        if(contIRAT > 1):
            promedioIRAT = sumaIRAT / (contIRAT - 1)
        if(contRDI > 1):
            promedioRDI = sumaRDI / (contRDI - 1)
        if(contRPMC > 1):
            promedioRPMC = sumaRPMC / (contRPMC - 1)
        if(contRPMP > 1):
            promedioRPMP = sumaRPMP / (contRPMP - 1)
        if(contRRCC > 1):
            promedioRRCC = sumaRRCC / (contRRCC - 1)
        if(contRRCP > 1):
            promedioRRCP = sumaRRCP / (contRRCP - 1)
        if(contRRI > 1):
            promedioRRI = sumaRRI / (contRRI - 1)
        #-----------------------------------------------
        if(contGE > 1):
            promedioGE = sumaGE / (contGE - 1)
        if(contGP > 1):
            promedioGP = sumaGP / (contGP - 1)
        if(contRCGF > 1):
            promedioRCGF = sumaRCGF / (contRCGF - 1)
        if(contREP > 1):
            promedioREP = sumaREP / (contREP - 1)
        #-----------------------------------------------
        if(contRDAC > 1):
            promedioRDAC = sumaRDAC / (contRDAC - 1)
        if(contRNP > 1):
            promedioRNP = sumaRNP / (contRNP - 1)
        if(contRSI > 1):
            promedioRSI = sumaRSI / (contRSI - 1)
        if(contRSV > 1):
            promedioRSV = sumaRSV / (contRSV - 1)


        cumplenRC = ""
        cumplenRCT = ""
        cumplenRR = ""
        cumplenRE = ""
        cumplenRDAC = ""
        #--------------------
        cumplenIMB = ""
        cumplenIMO = ""
        cumplenIRAF = ""
        cumplenIRAT = ""
        cumplenRDI = ""
        cumplenRPMC = ""
        cumplenRRCC = ""
        cumplenRRCP = ""
        cumplenRRI = ""
        #--------------------
        cumplenGE = ""
        cumplenGP = ""
        cumplenRCGF = ""
        cumplenREP = ""
        #--------------------
        cumplenRDAC = ""
        cumplenRNP = ""
        cumplenRSI = ""
        cumplenRSV = ""


        #---------------------
        noCumpleRC = ""
        noCumpleRCT = ""
        noCumpleRR = ""
        noCumpleRE = ""
        noCumpleRDAC = ""
        #---------------------
        noCumpleIMB = ""
        noCumpleIMO = ""
        noCumpleIRAF = ""
        noCumpleIRAT = ""
        noCumpleRDI = ""
        noCumpleRPMC = ""
        noCumpleRRCC = ""
        noCumpleRRCP = ""
        noCumpleRRI = ""
        #---------------------
        noCumpleGE = ""
        noCumpleGP = ""
        noCumpleRCGF = ""
        noCumpleREP = ""
        #--------------------
        noCumpleRDAC = ""
        noCumpleRNP = ""
        noCumpleRSI = ""
        noCumpleRSV = ""

        #Verificacion de las empresas que son mayores que el ratio segun Promedio de Empresa.
        j=0
        while(j < len(empresas)):
            sectorEmpresa = empresas[j].codEmpresa.codActividadEconomica_id
            valorRatio = empresas[j].valorRatioEmpresa
            tipoRatio = empresas[j].codRatio_id

            if(sectorEmpresa == codActividadEconomica):
                if(tipoRatio == "RC"):
                    if(valorRatio >= promedioRC):
                        cumplenRC = cumplenRC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRC = noCumpleRC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RCT"):
                    if(valorRatio >= promedioRCT):
                        cumplenRCT = cumplenRCT + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRCT = noCumpleRCT + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RR"):
                    if(valorRatio >= promedioRR):
                        cumplenRR = cumplenRR + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRR = noCumpleRR + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RE"):
                    if(valorRatio >= promedioRE):
                        cumplenRE = cumplenRE + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRE = noCumpleRE + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RDAC"):
                    if(valorRatio >= promedioRDAC):
                        cumplenRDAC = cumplenRDAC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRDAC = noCumpleRDAC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                #--------------------------------------------------------------------------------------------
                elif(tipoRatio == "IMB"):
                    if(valorRatio >= promedioIMB):
                        cumplenIMB = cumplenIMB + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleIMB = noCumpleIMB + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "IMO"):
                    if(valorRatio >= promedioIMO):
                        cumplenIMO = cumplenIMO + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleIMO = noCumpleIMO + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]     "
                elif(tipoRatio == "IRAF"):
                    if(valorRatio >= promedioIRAF):
                        cumplenIRAF = cumplenIRAF + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleIRAF = noCumpleIRAF + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "IRAT"):
                    if(valorRatio >= promedioIRAT):
                        cumplenIRAT = cumplenIRAT + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleIRAT = noCumpleIRAT + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RDI"):
                    if(valorRatio >= promedioRDI):
                        cumplenRDI = cumplenRDI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRDI = noCumpleRDI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RPMC"):
                    if(valorRatio >= promedioRPMC):
                        cumplenRPMC = cumplenRPMC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRPMC = noCumpleRPMC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RRCC"):
                    if(valorRatio >= promedioRRCC):
                        cumplenRRCC = cumplenRRCC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRRCC = noCumpleRRCC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RRCP"):
                    if(valorRatio >= promedioRRCP):
                        cumplenRRCP = cumplenRRCP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRRCP = noCumpleRRCP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RRI"):
                    if(valorRatio >= promedioRRI):
                        cumplenRRI = cumplenRRI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRRI = noCumpleRRI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                #--------------------------------------------------------------------------------------------
                elif(tipoRatio == "GE"):
                    if(valorRatio >= promedioGE):
                        cumplenGE = cumplenGE + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleGE = noCumpleGE + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "GP"):
                    if(valorRatio >= promedioGP):
                        cumplenGP = cumplenGP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleGP = noCumpleGP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RCGF"):
                    if(valorRatio >= promedioRCGF):
                        cumplenRCGF = cumplenRCGF + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRCGF = noCumpleRCGF + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "REP"):
                    if(valorRatio >= promedioREP):
                        cumplenREP = cumplenREP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleREP = noCumpleREP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                #--------------------------------------------------------------------------------------------
                elif(tipoRatio == "RDAC"):
                    if(valorRatio >= promedioRDAC):  
                        cumplenRDAC = cumplenRDAC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRDAC = noCumpleRDAC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RNP"):
                    if(valorRatio >= promedioRNP):
                        cumplenRNP = cumplenRNP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRNP = noCumpleRNP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RSI"):
                    if(valorRatio >= promedioRSI):
                        cumplenRSI = cumplenRSI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRSI = noCumpleRSI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                elif(tipoRatio == "RSV"):
                    if(valorRatio >= promedioRSV):
                        cumplenRSV = cumplenRSV + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleRSV = noCumpleRSV + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
            j+=1


        #----LIQ-------
        valSectorRC = 0
        valSectorRCT = 0
        valSectorRE = 0
        valSectorRR = 0
        valSectorRDAC = 0
        #----ACT-------
        valSectorIMB = 0
        valSectorIMO = 0
        valSectorIRAF = 0
        valSectorIRAT = 0
        valSectorRDI = 0
        valSectorRPMC = 0
        valSectorRPMP = 0
        valSectorRRCC = 0
        valSectorRRCP = 0
        valSectorRRI = 0
        #----APA--------
        valSectorGE = 0
        valSectorGP = 0
        valSectorRCGF = 0
        valSectorREP = 0
        #----REN--------
        valSectorRDAC = 0
        valSectorRNP = 0
        valSectorRSI = 0
        valSectorRSV = 0

        #Recuperacion del valor de cada Ratio de la tabla Ratio Empresa segun el Tipo de Ratio
        z=0
        while(z < len(valRatioSector)):
            valSectorTipoRatio = valRatioSector[z].codRatio_id
            valSectorActEco = valRatioSector[z].codActividadEconomica_id

            if(valSectorActEco == codActividadEconomica):
                if(valSectorTipoRatio == "RC"):
                    valSectorRC = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RCT"):
                    valSectorRCT = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RR"):
                    valSectorRR = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RE"):
                    valSectorRE = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RDAC"):
                    valSectorRDAC = valRatioSector[z].parametroComparacion
                #-----------------------------------------------------------------
                elif(valSectorTipoRatio == "IMB"):
                    valSectorIMB = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "IMO"):
                    valSectorIMO = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "IRAF"):
                    valSectorIRAF = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "IRAT"):
                    valSectorIRAT = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RDI"):
                    valSectorRDI = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RPMC"):
                    valSectorRPMC = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RPMP"):
                    valSectorRPMP = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RRCC"):
                    valSectorRRCC = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RRCP"):
                    valSectorRRCP = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RRI"):
                    valSectorRRI = valRatioSector[z].parametroComparacion
                #-----------------------------------------------------------------
                elif(valSectorTipoRatio == "GE"):
                    valSectorGE = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "GP"):
                    valSectorGP = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RCGF"):
                    valSectorRCGF = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "REP"):
                    valSectorREP = valRatioSector[z].parametroComparacion
                #-----------------------------------------------------------------
                elif(valSectorTipoRatio == "RDAC"):
                    valSectorRDAC = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RNP"):
                    valSectorRNP = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RSI"):
                    valSectorRSI = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RSV"):
                    valSectorRSV = valRatioSector[z].parametroComparacion
            z+=1


        cumplenSectorRC = ""
        cumplenSectorRCT = ""
        cumplenSectorRR = ""
        cumplenSectorRE = ""
        cumplenSectorRDAC = ""
        #--------------------
        cumplenSectorIMB = ""
        cumplenSectorIMO = ""
        cumplenSectorIRAF = ""
        cumplenSectorIRAT = ""
        cumplenSectorRDI = ""
        cumplenSectorRPMC = ""
        cumplenSectorRRCC = ""
        cumplenSectorRRCP = ""
        cumplenSectorRRI = ""
        #--------------------
        cumplenSectorGE = ""
        cumplenSectorGP = ""
        cumplenSectorRCGF = ""
        cumplenSectorREP = ""
        #--------------------
        cumplenSectorRDAC = ""
        cumplenSectorRNP = ""
        cumplenSectorRSI = ""
        cumplenSectorRSV = ""


        noCumpleSectorRC = ""
        noCumpleSectorRCT = ""
        noCumpleSectorRR = ""
        noCumpleSectorRE = ""
        noCumpleSectorRDAC = ""
        #---------------------
        noCumpleSectorIMB = ""
        noCumpleSectorIMO = ""
        noCumpleSectorIRAF = ""
        noCumpleSectorIRAT = ""
        noCumpleSectorRDI = ""
        noCumpleSectorRPMC = ""
        noCumpleSectorRRCC = ""
        noCumpleSectorRRCP = ""
        noCumpleSectorRRI = ""
        #---------------------
        noCumpleSectorGE = ""
        noCumpleSectorGP = ""
        noCumpleSectorRCGF = ""
        noCumpleSectorREP = ""
        #--------------------
        noCumpleSectorRDAC = ""
        noCumpleSectorRNP = ""
        noCumpleSectorRSI = ""
        noCumpleSectorRSV = ""


        #Verificacion de las empresas que son mayores que el ratio segun el Ratio de Empresa.
        x=0
        while(x < len(empresas)):
            sectorEmpresa = empresas[x].codEmpresa.codActividadEconomica_id
            valorRatio = empresas[x].valorRatioEmpresa
            tipoRatio = empresas[x].codRatio_id

            if(sectorEmpresa == codActividadEconomica):
                if(tipoRatio == "RC"):
                    if(valorRatio >= valSectorRC):
                        cumplenSectorRC = cumplenSectorRC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRC = noCumpleSectorRC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RCT"):
                    if(valorRatio >= valSectorRCT):
                        cumplenSectorRCT = cumplenSectorRCT + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRCT = noCumpleSectorRCT + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RR"):
                    if(valorRatio >= valSectorRR):
                        cumplenSectorRR = cumplenSectorRR + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRR = noCumpleSectorRR + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RE"):
                    if(valorRatio >= valSectorRE):
                        cumplenSectorRE = cumplenSectorRE + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRE = noCumpleSectorRE + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RDAC"):
                    if(valorRatio >= valSectorRDAC):
                        cumplenSectorRDAC = cumplenSectorRDAC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRDAC = noCumpleSectorRDAC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                #----------------------------------------------------------------------------------------------------------
                elif(tipoRatio == "IMB"):
                    if(valorRatio >= valSectorIMB):
                        cumplenSectorIMB = cumplenSectorIMB + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorIMB = noCumpleSectorIMB + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "IMO"):
                    if(valorRatio >= valSectorIMO):
                        cumplenSectorIMO = cumplenSectorIMO + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorIMO = noCumpleSectorIMO + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "IRAF"):
                    if(valorRatio >= valSectorIRAF):
                        cumplenSectorIRAF = cumplenSectorIRAF + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorIRAF = noCumpleSectorIRAF + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "IRAT"):
                    if(valorRatio >= valSectorIRAT):
                        cumplenSectorIRAT = cumplenSectorIRAT + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorIRAT = noCumpleSectorIRAT + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RDI"):
                    if(valorRatio >= valSectorRDI):
                        cumplenSectorRDI = cumplenSectorRDI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRDI = noCumpleSectorRDI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RPMC"):
                    if(valorRatio >= valSectorRPMC):
                        cumplenSectorRPMC = cumplenSectorRPMC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRPMC = noCumpleSectorRPMC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RRCC"):
                    if(valorRatio >= valSectorRRCC):
                        cumplenSectorRRCC = cumplenSectorRRCC+ " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRRCC = noCumpleSectorRRCC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RRCP"):
                    if(valorRatio >= valSectorRRCP):
                        cumplenSectorRRCP = cumplenSectorRRCP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRRCP = noCumpleSectorRRCP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RRI"):
                    if(valorRatio >= valSectorRRI):
                        cumplenSectorRRI = cumplenSectorRRI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRRI = noCumpleSectorRRI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                #----------------------------------------------------------------------------------------------------------
                elif(tipoRatio == "GE"):
                    if(valorRatio >= valSectorGE):
                        cumplenSectorGE = cumplenSectorGE + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorGE = noCumpleSectorGE + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "GP"):
                    if(valorRatio >= valSectorGP):
                        cumplenSectorGP = cumplenSectorGP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorGP = noCumpleSectorGP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RCGF"):
                    if(valorRatio >= valSectorRCGF):
                        cumplenSectorRCGF = cumplenSectorRCGF + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRCGF = noCumpleSectorRCGF + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "REP"):
                    if(valorRatio >= valSectorREP):
                        cumplenSectorREP = cumplenSectorREP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorREP = noCumpleSectorREP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                #----------------------------------------------------------------------------------------------------------
                elif(tipoRatio == "RDAC"):
                    if(valorRatio >= valSectorRDAC):
                        cumplenSectorRDAC = cumplenSectorRDAC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRDAC = noCumpleSectorRDAC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RNP"):
                    if(valorRatio >= valSectorRNP):
                        cumplenSectorRNP = cumplenSectorRNP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRNP = noCumpleSectorRNP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RSI"):
                    if(valorRatio >= valSectorRSI):
                        cumplenSectorRSI = cumplenSectorRSI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRSI = noCumpleSectorRSI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                elif(tipoRatio == "RSV"):
                    if(valorRatio >= valSectorRSV):
                        cumplenSectorRSV = cumplenSectorRSV + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                    else:
                        noCumpleSectorRSV = noCumpleSectorRSV + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
            x+=1

        
        #Guardar en la Base de Datos los registros para ver que empresas son las que cumplen.
        k=0
        while(k < len(empresas)):
            sectorEmpresa = empresas[k].codEmpresa.codActividadEconomica_id
            valorRatio = empresas[k].valorRatioEmpresa
            tipoRatio = empresas[k].codRatio_id

            if(sectorEmpresa == codActividadEconomica):
                if(tipoRatio == "RC"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRC = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRC, promEmpresas=promedioRC, empresasCumplenEmpresa=cumplenRC, empresasCumplenSector=cumplenSectorRC)
                        ratiosEmpresaSectorRC.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRC
                        obtener.promEmpresas=promedioRC
                        obtener.empresasCumplenEmpresa=cumplenRC
                        obtener.empresasCumplenSector=cumplenSectorRC
                        obtener.save()

                elif(tipoRatio == "RCT"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRCT = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRCT, promEmpresas=promedioRCT, empresasCumplenEmpresa=cumplenRCT, empresasCumplenSector=cumplenSectorRCT)
                        ratiosEmpresaSectorRCT.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRCT
                        obtener.promEmpresas=promedioRCT
                        obtener.empresasCumplenEmpresa=cumplenRCT
                        obtener.empresasCumplenSector=cumplenSectorRCT
                        obtener.save()
                elif(tipoRatio == "RR"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRR = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRR, promEmpresas=promedioRR, empresasCumplenEmpresa=cumplenRR, empresasCumplenSector=cumplenSectorRR)
                        ratiosEmpresaSectorRR.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRR
                        obtener.promEmpresas=promedioRR
                        obtener.empresasCumplenEmpresa=cumplenRR
                        obtener.empresasCumplenSector=cumplenSectorRR
                        obtener.save()
                elif(tipoRatio == "RE"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRE = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRE, promEmpresas=promedioRE, empresasCumplenEmpresa=cumplenRE, empresasCumplenSector=cumplenSectorRE)
                        ratiosEmpresaSectorRE.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRE
                        obtener.promEmpresas=promedioRE
                        obtener.empresasCumplenEmpresa=cumplenRE
                        obtener.empresasCumplenSector=cumplenSectorRE
                        obtener.save()
                elif(tipoRatio == "RDAC"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRDAC = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRDAC, promEmpresas=promedioRDAC, empresasCumplenEmpresa=cumplenRDAC, empresasCumplenSector=cumplenSectorRDAC)
                        ratiosEmpresaSectorRDAC.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRDAC
                        obtener.promEmpresas=promedioRDAC
                        obtener.empresasCumplenEmpresa=cumplenRDAC
                        obtener.empresasCumplenSector=cumplenSectorRDAC
                        obtener.save()
                #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                elif(tipoRatio == "IMB"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorIMB = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorIMB, promEmpresas=promedioIMB, empresasCumplenEmpresa=cumplenIMB, empresasCumplenSector=cumplenSectorIMB)
                        ratiosEmpresaSectorIMB.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorIMB
                        obtener.promEmpresas=promedioIMB
                        obtener.empresasCumplenEmpresa=cumplenIMB
                        obtener.empresasCumplenSector=cumplenSectorIMB
                        obtener.save()
                elif(tipoRatio == "IMO"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorIMO = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorIMO, promEmpresas=promedioIMO, empresasCumplenEmpresa=cumplenIMO, empresasCumplenSector=cumplenSectorIMO)
                        ratiosEmpresaSectorIMO.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorIMO
                        obtener.promEmpresas=promedioIMO
                        obtener.empresasCumplenEmpresa=cumplenIMO
                        obtener.empresasCumplenSector=cumplenSectorIMO
                        obtener.save()
                elif(tipoRatio == "IRAF"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorIRAF = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorIRAF, promEmpresas=promedioIRAF, empresasCumplenEmpresa=cumplenIRAF, empresasCumplenSector=cumplenSectorIRAF)
                        ratiosEmpresaSectorIRAF.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorIRAF
                        obtener.promEmpresas=promedioIRAF
                        obtener.empresasCumplenEmpresa=cumplenIRAF
                        obtener.empresasCumplenSector=cumplenSectorIRAF
                        obtener.save()
                elif(tipoRatio == "IRAT"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorIRAT = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorIRAT, promEmpresas=promedioIRAT, empresasCumplenEmpresa=cumplenIRAT, empresasCumplenSector=cumplenSectorIRAT)
                        ratiosEmpresaSectorIRAT.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorIRAT
                        obtener.promEmpresas=promedioIRAT
                        obtener.empresasCumplenEmpresa=cumplenIRAT
                        obtener.empresasCumplenSector=cumplenSectorIRAT
                        obtener.save()
                elif(tipoRatio == "RDI"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRDI = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRDI, promEmpresas=promedioRDI, empresasCumplenEmpresa=cumplenRDI, empresasCumplenSector=cumplenSectorRDI)
                        ratiosEmpresaSectorRDI.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRDI
                        obtener.promEmpresas=promedioRDI
                        obtener.empresasCumplenEmpresa=cumplenRDI
                        obtener.empresasCumplenSector=cumplenSectorRDI
                        obtener.save()
                elif(tipoRatio == "RPMC"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRPMC = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRPMC, promEmpresas=promedioRPMC, empresasCumplenEmpresa=cumplenRPMC, empresasCumplenSector=cumplenSectorRPMC)
                        ratiosEmpresaSectorRPMC.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRPMC
                        obtener.promEmpresas=promedioRPMC
                        obtener.empresasCumplenEmpresa=cumplenRPMC
                        obtener.empresasCumplenSector=cumplenSectorRPMC
                        obtener.save()
                elif(tipoRatio == "RRCC"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRRCC = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRRCC, promEmpresas=promedioRRCC, empresasCumplenEmpresa=cumplenRRCC, empresasCumplenSector=cumplenSectorRRCC)
                        ratiosEmpresaSectorRRCC.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRRCC
                        obtener.promEmpresas=promedioRRCC
                        obtener.empresasCumplenEmpresa=cumplenRRCC
                        obtener.empresasCumplenSector=cumplenSectorRRCC
                        obtener.save()
                elif(tipoRatio == "RRCP"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRRCP = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRRCP, promEmpresas=promedioRRCP, empresasCumplenEmpresa=cumplenRRCP, empresasCumplenSector=cumplenSectorRRCP)
                        ratiosEmpresaSectorRRCP.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRRCP
                        obtener.promEmpresas=promedioRRCP
                        obtener.empresasCumplenEmpresa=cumplenRRCP
                        obtener.empresasCumplenSector=cumplenSectorRRCP
                        obtener.save()
                elif(tipoRatio == "RRI"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRRI = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRRI, promEmpresas=promedioRRI, empresasCumplenEmpresa=cumplenRRI, empresasCumplenSector=cumplenSectorRRI)
                        ratiosEmpresaSectorRRI.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRRI
                        obtener.promEmpresas=promedioRRI
                        obtener.empresasCumplenEmpresa=cumplenRRI
                        obtener.empresasCumplenSector=cumplenSectorRRI
                        obtener.save()
                #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                elif(tipoRatio == "GE"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorGE = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorGE, promEmpresas=promedioGE, empresasCumplenEmpresa=cumplenGE, empresasCumplenSector=cumplenSectorGE)
                        ratiosEmpresaSectorGE.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorGE
                        obtener.promEmpresas=promedioGE
                        obtener.empresasCumplenEmpresa=cumplenGE
                        obtener.empresasCumplenSector=cumplenSectorGE
                        obtener.save()
                elif(tipoRatio == "GP"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorGP = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorGP, promEmpresas=promedioGP, empresasCumplenEmpresa=cumplenGP, empresasCumplenSector=cumplenSectorGP)
                        ratiosEmpresaSectorGP.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorGP
                        obtener.promEmpresas=promedioGP
                        obtener.empresasCumplenEmpresa=cumplenGP
                        obtener.empresasCumplenSector=cumplenSectorGP
                        obtener.save()
                elif(tipoRatio == "RCGF"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRCGF = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRCGF, promEmpresas=promedioRCGF, empresasCumplenEmpresa=cumplenRCGF, empresasCumplenSector=cumplenSectorRCGF)
                        ratiosEmpresaSectorRCGF.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRCGF
                        obtener.promEmpresas=promedioRCGF
                        obtener.empresasCumplenEmpresa=cumplenRCGF
                        obtener.empresasCumplenSector=cumplenSectorRCGF
                        obtener.save()
                elif(tipoRatio == "REP"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorREP = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorREP, promEmpresas=promedioREP, empresasCumplenEmpresa=cumplenREP, empresasCumplenSector=cumplenSectorREP)
                        ratiosEmpresaSectorREP.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorREP
                        obtener.promEmpresas=promedioREP
                        obtener.empresasCumplenEmpresa=cumplenREP
                        obtener.empresasCumplenSector=cumplenSectorREP
                        obtener.save()
                #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                elif(tipoRatio == "RDAC"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRDAC = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRDAC, promEmpresas=promedioRDAC, empresasCumplenEmpresa=cumplenRDAC, empresasCumplenSector=cumplenSectorRDAC)
                        ratiosEmpresaSectorRDAC.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRDAC
                        obtener.promEmpresas=promedioRDAC
                        obtener.empresasCumplenEmpresa=cumplenRDAC
                        obtener.empresasCumplenSector=cumplenSectorRDAC
                        obtener.save()
                elif(tipoRatio == "RNP"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRNP = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRNP, promEmpresas=promedioRNP, empresasCumplenEmpresa=cumplenRNP, empresasCumplenSector=cumplenSectorRNP)
                        ratiosEmpresaSectorRNP.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRNP
                        obtener.promEmpresas=promedioRNP
                        obtener.empresasCumplenEmpresa=cumplenRNP
                        obtener.empresasCumplenSector=cumplenSectorRNP
                        obtener.save()
                elif(tipoRatio == "RSI"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRSI = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRSI, promEmpresas=promedioRSI, empresasCumplenEmpresa=cumplenRSI, empresasCumplenSector=cumplenSectorRSI)
                        ratiosEmpresaSectorRSI.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRSI
                        obtener.promEmpresas=promedioRSI
                        obtener.empresasCumplenEmpresa=cumplenRSI
                        obtener.empresasCumplenSector=cumplenSectorRSI
                        obtener.save()
                elif(tipoRatio == "RSV"):
                    comprobar = RatiosEmpresaSector.objects.filter(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                    if(len(comprobar) == 0):
                        ratiosEmpresaSectorRSV = RatiosEmpresaSector(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio, valorSector=valSectorRSV, promEmpresas=promedioRSV, empresasCumplenEmpresa=cumplenRSV, empresasCumplenSector=cumplenSectorRSV)
                        ratiosEmpresaSectorRSV.save()
                    else:
                        obtener = RatiosEmpresaSector.objects.get(codActividadEconomica_id=sectorEmpresa, año=año, codRatio_id=tipoRatio)
                        obtener.valorSector=valSectorRSV
                        obtener.promEmpresas=promedioRSV
                        obtener.empresasCumplenEmpresa=cumplenRSV
                        obtener.empresasCumplenSector=cumplenSectorRSV
                        obtener.save()
            k+=1


        #FIN DEL CALCULO DEL PROMEDIO DE CADA SECTOR

        queryset = RatiosEmpresaSector.objects.filter(codActividadEconomica=codActividadEconomica, año=año)

        contexto = {
            'queryset': queryset,
            'sector': sector,
            'actividad': sectorCons,
            'año': año,
        }

        return render(
            request,
            'proyecto/InformeAnalisis.html',
            contexto
        )


#-------------------------------------------------------------------------------------------------------


def consultarInformeEmpresa(request, username):
    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        querysetRA =Empresa.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        querysetRA= Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
            'querysetRA':querysetRA,
    } 
    return render(request,'proyecto/analisisEmpresa.html', contexto)

def informeAnalisisEmpresa(request):
    if request.method == 'POST':
        #codActividadEconomica = request.POST['codActividadEconomica']
        año = request.POST['año']
        codEmpresa = request.POST['codEmpresa']

        sector = Empresa.objects.filter(codEmpresa=codEmpresa)
        i=0
        while(i < len(sector)):
            codActividadEconomica = sector[i].codActividadEconomica_id
            codActividadEconomicaNombre = sector[i].codActividadEconomica.nombreActividadEconomica
            i+=1

        empresa = Empresa.objects.filter(codEmpresa=codEmpresa)

        valRatioSector = RatiosSector.objects.filter(codActividadEconomica=codActividadEconomica)
        empresas = RatiosEmpresa.objects.filter(año=año)


        #CALCULO DEL PROMEDIO PARA CADA SECTOR

        #----LIQ-------
        sumaRC = 0
        sumaRCT = 0
        sumaRE = 0
        sumaRR = 0
        sumaRDAC = 0
        #----ACT-------
        sumaIMB = 0
        sumaIMO = 0
        sumaIRAF = 0
        sumaIRAT = 0
        sumaRDI = 0
        sumaRPMC = 0
        sumaRPMP = 0
        sumaRRCC = 0
        sumaRRCP = 0
        sumaRRI = 0
        #----APA--------
        sumaGE = 0
        sumaGP = 0
        sumaRCGF = 0
        sumaREP = 0
        #----REN--------
        sumaRDAC = 0
        sumaRNP = 0
        sumaRSI = 0
        sumaRSV = 0


        #-------------
        contRC = 1
        contRCT = 1
        contRE = 1
        contRR = 1
        contRDAC = 1
        #-------------
        contIMB = 1
        contIMO = 1
        contIRAF = 1
        contIRAT = 1
        contRDI = 1
        contRPMC = 1
        contRPMP = 1
        contRRCC = 1
        contRRCP = 1
        contRRI = 1
        #-------------
        contGE = 1
        contGP = 1
        contRCGF = 1
        contREP = 1
        #-------------
        contRDAC = 1
        contRNP = 1
        contRSI = 1
        contRSV = 1


        #Guardo la Suma del valor de ese ratio de todas las empresas
        i=0
        while(i < len(empresas)):
            sectorEmpresa = empresas[i].codEmpresa.codActividadEconomica_id
            valorRatio = empresas[i].valorRatioEmpresa
            tipoRatio = empresas[i].codRatio_id

            if(sectorEmpresa == codActividadEconomica):
                if(tipoRatio == "RC"):
                    sumaRC = sumaRC + valorRatio
                    contRC+=1
                elif(tipoRatio == "RCT"):
                    sumaRCT = sumaRCT + valorRatio
                    contRCT+=1
                elif(tipoRatio == "RR"):
                    sumaRR = sumaRE + valorRatio
                    contRR+=1
                elif(tipoRatio == "RE"):
                    sumaRE = sumaRE + valorRatio
                    contRE+=1
                elif(tipoRatio == "RDAC"):
                    sumaRDAC = sumaRDAC + valorRatio
                    contRDAC+=1
                #----------------------------------------
                elif(tipoRatio == "IMB"):
                    sumaIMB = sumaIMB + valorRatio
                    contIMB+=1
                elif(tipoRatio == "IMO"):
                    sumaIMO = sumaIMO + valorRatio
                    contIMO+=1
                elif(tipoRatio == "IRAF"):
                    sumaIRAF = sumaIRAF + valorRatio
                    contIRAF+=1
                elif(tipoRatio == "IRAT"):
                    sumaIRAT = sumaIRAT + valorRatio
                    contIRAT+=1
                elif(tipoRatio == "RDI"):
                    sumaRDI = sumaRDI + valorRatio
                    contRDI+=1
                elif(tipoRatio == "RPMC"):
                    sumaRPMC = sumaRPMC + valorRatio
                    contRPMC+=1
                elif(tipoRatio == "RPMP"):
                    sumaRPMP = sumaRPMP + valorRatio
                    contRPMP+=1
                elif(tipoRatio == "RRCC"):
                    sumaRRCC = sumaRRCC + valorRatio
                    contRRCC+=1
                elif(tipoRatio == "RRCP"):
                    sumaRRCP = sumaRRCP + valorRatio
                    contRRCP+=1
                elif(tipoRatio == "RRI"):
                    sumaRRI = sumaRRI + valorRatio
                    contRRI+=1
                #----------------------------------------
                elif(tipoRatio == "GE"):
                    sumaGE = sumaGE + valorRatio
                    contGE+=1
                elif(tipoRatio == "GP"):
                    sumaGP = sumaGP + valorRatio
                    contGP+=1
                elif(tipoRatio == "RCGF"):
                    sumaRCGF = sumaRCGF + valorRatio
                    contRCGF+=1
                elif(tipoRatio == "REP"):
                    sumaREP = sumaREP + valorRatio
                    contREP+=1
                #----------------------------------------
                elif(tipoRatio == "RDAC"):
                    sumaRDAC = sumaRDAC + valorRatio
                    contRDAC+=1
                elif(tipoRatio == "RNP"):
                    sumaRNP = sumaRNP + valorRatio
                    contRNP+=1
                elif(tipoRatio == "RSI"):
                    sumaRSI = sumaRSI + valorRatio
                    contRSI+=1
                elif(tipoRatio == "RSV"):
                    sumaRSV = sumaRSV + valorRatio
                    contRSV+=1
            i+=1

        # Calculo del Promedio de las empresas
        # Le resto 1 porque lo inicalice a 1 para que no de error de Div/0 cuando no se use en el while
        if(contRC > 1):
            promedioRC = sumaRC / (contRC - 1)
        if(contRCT > 1):
            promedioRCT = sumaRCT / (contRCT - 1)
        if(contRE > 1):
            promedioRE = sumaRE / (contRE - 1)
        if(contRR > 1):
            promedioRR = sumaRR / (contRR - 1)
        if(contRDAC > 1):
            promedioRDAC = sumaRDAC / (contRDAC - 1)
        #-----------------------------------------------
        if(contIMB > 1):
            promedioIMB = sumaIMB / (contIMB - 1)
        if(contIMO > 1):
            promedioIMO = sumaIMO / (contIMO - 1)
        if(contIRAF > 1):
            promedioIRAF = sumaIRAF / (contIRAF - 1)
        if(contIRAT > 1):
            promedioIRAT = sumaIRAT / (contIRAT - 1)
        if(contRDI > 1):
            promedioRDI = sumaRDI / (contRDI - 1)
        if(contRPMC > 1):
            promedioRPMC = sumaRPMC / (contRPMC - 1)
        if(contRPMP > 1):
            promedioRPMP = sumaRPMP / (contRPMP - 1)
        if(contRRCC > 1):
            promedioRRCC = sumaRRCC / (contRRCC - 1)
        if(contRRCP > 1):
            promedioRRCP = sumaRRCP / (contRRCP - 1)
        if(contRRI > 1):
            promedioRRI = sumaRRI / (contRRI - 1)
        #-----------------------------------------------
        if(contGE > 1):
            promedioGE = sumaGE / (contGE - 1)
        if(contGP > 1):
            promedioGP = sumaGP / (contGP - 1)
        if(contRCGF > 1):
            promedioRCGF = sumaRCGF / (contRCGF - 1)
        if(contREP > 1):
            promedioREP = sumaREP / (contREP - 1)
        #-----------------------------------------------
        if(contRDAC > 1):
            promedioRDAC = sumaRDAC / (contRDAC - 1)
        if(contRNP > 1):
            promedioRNP = sumaRNP / (contRNP - 1)
        if(contRSI > 1):
            promedioRSI = sumaRSI / (contRSI - 1)
        if(contRSV > 1):
            promedioRSV = sumaRSV / (contRSV - 1)


        cumplenRC = ""
        cumplenRCT = ""
        cumplenRR = ""
        cumplenRE = ""
        cumplenRDAC = ""
        #--------------------
        cumplenIMB = ""
        cumplenIMO = ""
        cumplenIRAF = ""
        cumplenIRAT = ""
        cumplenRDI = ""
        cumplenRPMC = ""
        cumplenRRCC = ""
        cumplenRRCP = ""
        cumplenRRI = ""
        #--------------------
        cumplenGE = ""
        cumplenGP = ""
        cumplenRCGF = ""
        cumplenREP = ""
        #--------------------
        cumplenRDAC = ""
        cumplenRNP = ""
        cumplenRSI = ""
        cumplenRSV = ""


        #---------------------
        noCumpleRC = ""
        noCumpleRCT = ""
        noCumpleRR = ""
        noCumpleRE = ""
        noCumpleRDAC = ""
        #---------------------
        noCumpleIMB = ""
        noCumpleIMO = ""
        noCumpleIRAF = ""
        noCumpleIRAT = ""
        noCumpleRDI = ""
        noCumpleRPMC = ""
        noCumpleRRCC = ""
        noCumpleRRCP = ""
        noCumpleRRI = ""
        #---------------------
        noCumpleGE = ""
        noCumpleGP = ""
        noCumpleRCGF = ""
        noCumpleREP = ""
        #--------------------
        noCumpleRDAC = ""
        noCumpleRNP = ""
        noCumpleRSI = ""
        noCumpleRSV = ""

        #Verificacion de las empresas que son mayores que el ratio segun Promedio de Empresa.

        j=0
        while(j < len(empresas)):
            sectorEmpresa = empresas[j].codEmpresa.codActividadEconomica_id
            valorRatio = empresas[j].valorRatioEmpresa
            tipoRatio = empresas[j].codRatio_id
            emp = empresas[j].codEmpresa_id
            msjEmpresa = "La empresa cumple con el valor promedio de empresas."
            msjEmpresaNO = "ADVERTENCIA: No satisface el valor promedio de empresas."

            if(sectorEmpresa == codActividadEconomica):
                if(tipoRatio == "RC"):
                    if(valorRatio >= promedioRC):
                        cumplenRC = cumplenRC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "

                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRC
                            obtener.save()

                    else:
                        noCumpleRC = noCumpleRC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "

                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRC
                            obtener.save()

                elif(tipoRatio == "RCT"):
                    if(valorRatio >= promedioRCT):
                        cumplenRCT = cumplenRCT + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "

                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRCT)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRCT
                            obtener.save()

                    else:
                        noCumpleRCT = noCumpleRCT + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRCT)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRCT
                            obtener.save()

                elif(tipoRatio == "RR"):
                    if(valorRatio >= promedioRR):
                        cumplenRR = cumplenRR + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "

                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRR)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRR
                            obtener.save()

                    else:
                        noCumpleRR = noCumpleRR + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRR)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRR
                            obtener.save()

                elif(tipoRatio == "RE"):
                    if(valorRatio >= promedioRE):
                        cumplenRE = cumplenRE + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "

                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRE)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRE
                            obtener.save()

                    else:
                        noCumpleRE = noCumpleRE + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRE)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRE
                            obtener.save()

                elif(tipoRatio == "RDAC"):
                    if(valorRatio >= promedioRDAC):
                        cumplenRDAC = cumplenRDAC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "

                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRDAC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRDAC
                            obtener.save()

                    else:
                        noCumpleRDAC = noCumpleRDAC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRDAC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRDAC
                            obtener.save()

                #--------------------------------------------------------------------------------------------
                elif(tipoRatio == "IMB"):
                    if(valorRatio >= promedioIMB):
                        cumplenIMB = cumplenIMB + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioIMB)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioIMB
                            obtener.save()

                    else:
                        noCumpleIMB = noCumpleIMB + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioIMB)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioIMB
                            obtener.save()

                elif(tipoRatio == "IMO"):
                    if(valorRatio >= promedioIMO):
                        cumplenIMO = cumplenIMO + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioIMO)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioIMO
                            obtener.save()

                    else:
                        noCumpleIMO = noCumpleIMO + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]     "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioIMO)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioIMO
                            obtener.save()

                elif(tipoRatio == "IRAF"):
                    if(valorRatio >= promedioIRAF):
                        cumplenIRAF = cumplenIRAF + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioIRAF)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioIRAF
                            obtener.save()

                    else:
                        noCumpleIRAF = noCumpleIRAF + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioIRAF)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioIRAF
                            obtener.save()

                elif(tipoRatio == "IRAT"):
                    if(valorRatio >= promedioIRAT):
                        cumplenIRAT = cumplenIRAT + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioIRAT)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioIRAT
                            obtener.save()

                    else:
                        noCumpleIRAT = noCumpleIRAT + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioIRAT)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioIRAT
                            obtener.save()

                elif(tipoRatio == "RDI"):
                    if(valorRatio >= promedioRDI):
                        cumplenRDI = cumplenRDI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRDI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRDI
                            obtener.save()

                    else:
                        noCumpleRDI = noCumpleRDI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRDI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRDI
                            obtener.save()

                elif(tipoRatio == "RPMC"):
                    if(valorRatio >= promedioRPMC):
                        cumplenRPMC = cumplenRPMC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRPMC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRPMC
                            obtener.save()

                    else:
                        noCumpleRPMC = noCumpleRPMC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRPMC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRPMC
                            obtener.save()

                elif(tipoRatio == "RRCC"):
                    if(valorRatio >= promedioRRCC):
                        cumplenRRCC = cumplenRRCC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRRCC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRRCC
                            obtener.save()

                    else:
                        noCumpleRRCC = noCumpleRRCC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRRCC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRRCC
                            obtener.save()

                elif(tipoRatio == "RRCP"):
                    if(valorRatio >= promedioRRCP):
                        cumplenRRCP = cumplenRRCP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRRCP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRRCP
                            obtener.save()

                    else:
                        noCumpleRRCP = noCumpleRRCP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRRCP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRRCP
                            obtener.save()

                elif(tipoRatio == "RRI"):
                    if(valorRatio >= promedioRRI):
                        cumplenRRI = cumplenRRI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRRI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRRI
                            obtener.save()

                    else:
                        noCumpleRRI = noCumpleRRI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRRI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRRI
                            obtener.save()

                #--------------------------------------------------------------------------------------------
                elif(tipoRatio == "GE"):
                    if(valorRatio >= promedioGE):
                        cumplenGE = cumplenGE + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioGE)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioGE
                            obtener.save()

                    else:
                        noCumpleGE = noCumpleGE + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioGE)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioGE
                            obtener.save()

                elif(tipoRatio == "GP"):
                    if(valorRatio >= promedioGP):
                        cumplenGP = cumplenGP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioGP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioGP
                            obtener.save()

                    else:
                        noCumpleGP = noCumpleGP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioGP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioGP
                            obtener.save()

                elif(tipoRatio == "RCGF"):
                    if(valorRatio >= promedioRCGF):
                        cumplenRCGF = cumplenRCGF + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRCGF)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRCGF
                            obtener.save()

                    else:
                        noCumpleRCGF = noCumpleRCGF + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRCGF)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRCGF
                            obtener.save()

                elif(tipoRatio == "REP"):
                    if(valorRatio >= promedioREP):
                        cumplenREP = cumplenREP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioREP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioREP
                            obtener.save()

                    else:
                        noCumpleREP = noCumpleREP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioREP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioREP
                            obtener.save()

                #--------------------------------------------------------------------------------------------
                elif(tipoRatio == "RDAC"):
                    if(valorRatio >= promedioRDAC):  
                        cumplenRDAC = cumplenRDAC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRDAC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRDAC
                            obtener.save()

                    else:
                        noCumpleRDAC = noCumpleRDAC + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRDAC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRDAC
                            obtener.save()

                elif(tipoRatio == "RNP"):
                    if(valorRatio >= promedioRNP):
                        cumplenRNP = cumplenRNP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRNP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRNP
                            obtener.save()

                    else:
                        noCumpleRNP = noCumpleRNP + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRNP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRNP
                            obtener.save()

                elif(tipoRatio == "RSI"):
                    if(valorRatio >= promedioRSI):
                        cumplenRSI = cumplenRSI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRSI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRSI
                            obtener.save()

                    else:
                        noCumpleRSI = noCumpleRSI + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRSI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRSI
                            obtener.save()

                elif(tipoRatio == "RSV"):
                    if(valorRatio >= promedioRSV):
                        cumplenRSV = cumplenRSV + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresa, promEmpresas=promedioRSV)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresa
                            obtener.promEmpresas=promedioRSV
                            obtener.save()

                    else:
                        noCumpleRSV = noCumpleRSV + " ["+ empresas[j].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ") " +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio, valorEmpresa=valorRatio, mensajePromedio=msjEmpresaNO, promEmpresas=promedioRSV)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.valorEmpresa=valorRatio
                            obtener.mensajePromedio=msjEmpresaNO
                            obtener.promEmpresas=promedioRSV
                            obtener.save()

            j+=1


        #----LIQ-------
        valSectorRC = 0
        valSectorRCT = 0
        valSectorRE = 0
        valSectorRR = 0
        valSectorRDAC = 0
        #----ACT-------
        valSectorIMB = 0
        valSectorIMO = 0
        valSectorIRAF = 0
        valSectorIRAT = 0
        valSectorRDI = 0
        valSectorRPMC = 0
        valSectorRPMP = 0
        valSectorRRCC = 0
        valSectorRRCP = 0
        valSectorRRI = 0
        #----APA--------
        valSectorGE = 0
        valSectorGP = 0
        valSectorRCGF = 0
        valSectorREP = 0
        #----REN--------
        valSectorRDAC = 0
        valSectorRNP = 0
        valSectorRSI = 0
        valSectorRSV = 0

        #Recuperacion del valor de cada Ratio de la tabla Ratio Empresa segun el Tipo de Ratio
        z=0
        while(z < len(valRatioSector)):
            valSectorTipoRatio = valRatioSector[z].codRatio_id
            valSectorActEco = valRatioSector[z].codActividadEconomica_id

            if(valSectorActEco == codActividadEconomica):
                if(valSectorTipoRatio == "RC"):
                    valSectorRC = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RCT"):
                    valSectorRCT = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RR"):
                    valSectorRR = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RE"):
                    valSectorRE = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RDAC"):
                    valSectorRDAC = valRatioSector[z].parametroComparacion
                #-----------------------------------------------------------------
                elif(valSectorTipoRatio == "IMB"):
                    valSectorIMB = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "IMO"):
                    valSectorIMO = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "IRAF"):
                    valSectorIRAF = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "IRAT"):
                    valSectorIRAT = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RDI"):
                    valSectorRDI = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RPMC"):
                    valSectorRPMC = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RPMP"):
                    valSectorRPMP = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RRCC"):
                    valSectorRRCC = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RRCP"):
                    valSectorRRCP = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RRI"):
                    valSectorRRI = valRatioSector[z].parametroComparacion
                #-----------------------------------------------------------------
                elif(valSectorTipoRatio == "GE"):
                    valSectorGE = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "GP"):
                    valSectorGP = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RCGF"):
                    valSectorRCGF = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "REP"):
                    valSectorREP = valRatioSector[z].parametroComparacion
                #-----------------------------------------------------------------
                elif(valSectorTipoRatio == "RDAC"):
                    valSectorRDAC = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RNP"):
                    valSectorRNP = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RSI"):
                    valSectorRSI = valRatioSector[z].parametroComparacion
                elif(valSectorTipoRatio == "RSV"):
                    valSectorRSV = valRatioSector[z].parametroComparacion
            z+=1


        cumplenSectorRC = ""
        cumplenSectorRCT = ""
        cumplenSectorRR = ""
        cumplenSectorRE = ""
        cumplenSectorRDAC = ""
        #--------------------
        cumplenSectorIMB = ""
        cumplenSectorIMO = ""
        cumplenSectorIRAF = ""
        cumplenSectorIRAT = ""
        cumplenSectorRDI = ""
        cumplenSectorRPMC = ""
        cumplenSectorRRCC = ""
        cumplenSectorRRCP = ""
        cumplenSectorRRI = ""
        #--------------------
        cumplenSectorGE = ""
        cumplenSectorGP = ""
        cumplenSectorRCGF = ""
        cumplenSectorREP = ""
        #--------------------
        cumplenSectorRDAC = ""
        cumplenSectorRNP = ""
        cumplenSectorRSI = ""
        cumplenSectorRSV = ""


        noCumpleSectorRC = ""
        noCumpleSectorRCT = ""
        noCumpleSectorRR = ""
        noCumpleSectorRE = ""
        noCumpleSectorRDAC = ""
        #---------------------
        noCumpleSectorIMB = ""
        noCumpleSectorIMO = ""
        noCumpleSectorIRAF = ""
        noCumpleSectorIRAT = ""
        noCumpleSectorRDI = ""
        noCumpleSectorRPMC = ""
        noCumpleSectorRRCC = ""
        noCumpleSectorRRCP = ""
        noCumpleSectorRRI = ""
        #---------------------
        noCumpleSectorGE = ""
        noCumpleSectorGP = ""
        noCumpleSectorRCGF = ""
        noCumpleSectorREP = ""
        #--------------------
        noCumpleSectorRDAC = ""
        noCumpleSectorRNP = ""
        noCumpleSectorRSI = ""
        noCumpleSectorRSV = ""

        #Verificacion de las empresas que son mayores que el ratio segun el Ratio de Empresa.
        x=0
        while(x < len(empresas)):
            sectorEmpresa = empresas[x].codEmpresa.codActividadEconomica_id
            valorRatio = empresas[x].valorRatioEmpresa
            tipoRatio = empresas[x].codRatio_id
            emp = empresas[x].codEmpresa_id
            msjSector = "La empresa cumple con el valor estandar del sector."
            msjSectorNO = "ADVERTENCIA: No satisface el valor estandar del sector."

            if(sectorEmpresa == codActividadEconomica):
                if(tipoRatio == "RC"):
                    if(valorRatio >= valSectorRC):
                        cumplenSectorRC = cumplenSectorRC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRC
                            obtener.save()

                    else:
                        noCumpleSectorRC = noCumpleSectorRC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRC
                            obtener.save()

                elif(tipoRatio == "RCT"):
                    if(valorRatio >= valSectorRCT):
                        cumplenSectorRCT = cumplenSectorRCT + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRCT)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRCT
                            obtener.save()

                    else:
                        noCumpleSectorRCT = noCumpleSectorRCT + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRCT)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRCT
                            obtener.save()

                elif(tipoRatio == "RR"):
                    if(valorRatio >= valSectorRR):
                        cumplenSectorRR = cumplenSectorRR + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRR)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRR
                            obtener.save()

                    else:
                        noCumpleSectorRR = noCumpleSectorRR + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRR)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRR
                            obtener.save()

                elif(tipoRatio == "RE"):
                    if(valorRatio >= valSectorRE):
                        cumplenSectorRE = cumplenSectorRE + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRE)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRE
                            obtener.save()

                    else:
                        noCumpleSectorRE = noCumpleSectorRE + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRE)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRE
                            obtener.save()

                elif(tipoRatio == "RDAC"):
                    if(valorRatio >= valSectorRDAC):
                        cumplenSectorRDAC = cumplenSectorRDAC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRDAC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRDAC
                            obtener.save()

                    else:
                        noCumpleSectorRDAC = noCumpleSectorRDAC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRDAC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRDAC
                            obtener.save()

                #----------------------------------------------------------------------------------------------------------
                elif(tipoRatio == "IMB"):
                    if(valorRatio >= valSectorIMB):
                        cumplenSectorIMB = cumplenSectorIMB + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorIMB)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorIMB
                            obtener.save()

                    else:
                        noCumpleSectorIMB = noCumpleSectorIMB + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorIMB)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorIMB
                            obtener.save()

                elif(tipoRatio == "IMO"):
                    if(valorRatio >= valSectorIMO):
                        cumplenSectorIMO = cumplenSectorIMO + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorIMO)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorIMO
                            obtener.save()

                    else:
                        noCumpleSectorIMO = noCumpleSectorIMO + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorIMO)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorIMO
                            obtener.save()

                elif(tipoRatio == "IRAF"):
                    if(valorRatio >= valSectorIRAF):
                        cumplenSectorIRAF = cumplenSectorIRAF + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorIRAF)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorIRAF
                            obtener.save()

                    else:
                        noCumpleSectorIRAF = noCumpleSectorIRAF + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorIRAF)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorIRAF
                            obtener.save()

                elif(tipoRatio == "IRAT"):
                    if(valorRatio >= valSectorIRAT):
                        cumplenSectorIRAT = cumplenSectorIRAT + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorIRAT)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorIRAT
                            obtener.save()

                    else:
                        noCumpleSectorIRAT = noCumpleSectorIRAT + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorIRAT)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorIRAT
                            obtener.save()

                elif(tipoRatio == "RDI"):
                    if(valorRatio >= valSectorRDI):
                        cumplenSectorRDI = cumplenSectorRDI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRDI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRDI
                            obtener.save()

                    else:
                        noCumpleSectorRDI = noCumpleSectorRDI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRDI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRDI
                            obtener.save()

                elif(tipoRatio == "RPMC"):
                    if(valorRatio >= valSectorRPMC):
                        cumplenSectorRPMC = cumplenSectorRPMC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRPMC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRPMC
                            obtener.save()

                    else:
                        noCumpleSectorRPMC = noCumpleSectorRPMC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRPMC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRPMC
                            obtener.save()

                elif(tipoRatio == "RRCC"):
                    if(valorRatio >= valSectorRRCC):
                        cumplenSectorRRCC = cumplenSectorRRCC+ " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRRCC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRRCC
                            obtener.save()

                    else:
                        noCumpleSectorRRCC = noCumpleSectorRRCC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRRCC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRRCC
                            obtener.save()

                elif(tipoRatio == "RRCP"):
                    if(valorRatio >= valSectorRRCP):
                        cumplenSectorRRCP = cumplenSectorRRCP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRRCP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRRCP
                            obtener.save()

                    else:
                        noCumpleSectorRRCP = noCumpleSectorRRCP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRRCP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRRCP
                            obtener.save()

                elif(tipoRatio == "RRI"):
                    if(valorRatio >= valSectorRRI):
                        cumplenSectorRRI = cumplenSectorRRI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRRI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRRI
                            obtener.save()

                    else:
                        noCumpleSectorRRI = noCumpleSectorRRI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRRI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRRI
                            obtener.save()

                #----------------------------------------------------------------------------------------------------------
                elif(tipoRatio == "GE"):
                    if(valorRatio >= valSectorGE):
                        cumplenSectorGE = cumplenSectorGE + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorGE)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorGE
                            obtener.save()

                    else:
                        noCumpleSectorGE = noCumpleSectorGE + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorGE)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorGE
                            obtener.save()

                elif(tipoRatio == "GP"):
                    if(valorRatio >= valSectorGP):
                        cumplenSectorGP = cumplenSectorGP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorGP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorGP
                            obtener.save()

                    else:
                        noCumpleSectorGP = noCumpleSectorGP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorGP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorGP
                            obtener.save()

                elif(tipoRatio == "RCGF"):
                    if(valorRatio >= valSectorRCGF):
                        cumplenSectorRCGF = cumplenSectorRCGF + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRCGF)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRCGF
                            obtener.save()

                    else:
                        noCumpleSectorRCGF = noCumpleSectorRCGF + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRCGF)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRCGF
                            obtener.save()

                elif(tipoRatio == "REP"):
                    if(valorRatio >= valSectorREP):
                        cumplenSectorREP = cumplenSectorREP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorREP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorREP
                            obtener.save()

                    else:
                        noCumpleSectorREP = noCumpleSectorREP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorREP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorREP
                            obtener.save()

                #----------------------------------------------------------------------------------------------------------
                elif(tipoRatio == "RDAC"):
                    if(valorRatio >= valSectorRDAC):
                        cumplenSectorRDAC = cumplenSectorRDAC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRDAC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRDAC
                            obtener.save()

                    else:
                        noCumpleSectorRDAC = noCumpleSectorRDAC + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRDAC)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRDAC
                            obtener.save()

                elif(tipoRatio == "RNP"):
                    if(valorRatio >= valSectorRNP):
                        cumplenSectorRNP = cumplenSectorRNP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRNP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRNP
                            obtener.save()

                    else:
                        noCumpleSectorRNP = noCumpleSectorRNP + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRNP)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRNP
                            obtener.save()

                elif(tipoRatio == "RSI"):
                    if(valorRatio >= valSectorRSI):
                        cumplenSectorRSI = cumplenSectorRSI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRSI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRSI
                            obtener.save()

                    else:
                        noCumpleSectorRSI = noCumpleSectorRSI + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRSI)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRSI
                            obtener.save()

                elif(tipoRatio == "RSV"):
                    if(valorRatio >= valSectorRSV):
                        cumplenSectorRSV = cumplenSectorRSV + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"]   "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSector, valorSector=valSectorRSV)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSector
                            obtener.valorSector=valSectorRSV
                            obtener.save()

                    else:
                        noCumpleSectorRSV = noCumpleSectorRSV + " ["+ empresas[x].codEmpresa.nombreEmpresa +" (" +str(valorRatio)+ ")" +"] "
                        
                        comprobar = AnalisisEmpresaSector.objects.filter(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                        if(len(comprobar) == 0):
                            analisisEmpresaSector = AnalisisEmpresaSector(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio,  valorEmpresa=valorRatio, mensajeSector=msjSectorNO, valorSector=valSectorRSV)
                            analisisEmpresaSector.save()
                        else:
                            obtener = AnalisisEmpresaSector.objects.get(codEmpresa_id=emp, año=año, codRatio_id=tipoRatio)
                            obtener.mensajeSector=msjSectorNO
                            obtener.valorSector=valSectorRSV
                            obtener.save()

            x+=1


        queryset = AnalisisEmpresaSector.objects.filter(codEmpresa_id=codEmpresa, año=año)

        contexto = {
            'queryset': queryset,
            'año': año,
            'empresa': empresa,
            'sector': codActividadEconomicaNombre,
        }

        return render(
            request,
            'proyecto/analisisEmpresa.html',
            contexto
        )


#---------------------------CRUD DE LA TABLA proyecto_ratiossector----------------------------------------------------------------------------


def insertarRatioSector(request):
    existe=""
    if request.method == 'POST':

        actividadEco = request.POST['actividades']
        ratioEco = request.POST['ratios']
        valorRatio = request.POST['valorRatio']
        
        if actividadEco and ratioEco and valorRatio:
            regfilter1 = ActividadEconomica.objects.filter(codActividadEconomica=actividadEco)
            regfilter2 = Ratio.objects.filter(codRatio=ratioEco)

            if regfilter1 and regfilter2:
                regFilter = RatiosSector.objects.filter(codRatio=ratioEco, codActividadEconomica=actividadEco)  

                if regFilter:
                    existe="Ya existe un registro con los datos ingresados!!!"
                else:
                    queryset = RatiosSector(
                        codRatio=Ratio.objects.get(codRatio=ratioEco), 
                        codActividadEconomica=ActividadEconomica.objects.get(codActividadEconomica=actividadEco), 
                        parametroComparacion=valorRatio
                    )
                    queryset.save()
                    existe="Registro guardado satisfactoriamente!!!"              
                

    actividad = ActividadEconomica.objects.all
    ratio = Ratio.objects.all

    contexto = {
        'actividad':actividad,
        'ratio':ratio,
        'exist':existe,
    }

    return render(request,'proyecto/insertarRatioSector.html', contexto)



def consultarRatioSector(request):
    actividad = ActividadEconomica.objects.all
    ratio = Ratio.objects.all
    queryset = RatiosSector.objects.all

    contexto = {
            'actividad':actividad,
            'ratio':ratio,
            'queryset':queryset,
    }

    if request.method=='POST':

        actividadEco = request.POST['actividades']
        ratioEco = request.POST['ratios']           

        if actividadEco and ratioEco:
            queryset = RatiosSector.objects.filter(codActividadEconomica=actividadEco, codRatio=ratioEco)

            if queryset:              
                contexto = {
                    'actividad':actividad,
                    'ratio':ratio,
                    'queryset':queryset,
                }       
            
    return render(request, 'proyecto/consultarRatioSector.html', contexto)



def actualizarRatioSector(request):   
    ca = request.POST['codAct']
    cr = request.POST['codRat']
         
    if ca and cr:            
        regFilter = RatiosSector.objects.get(codActividadEconomica=ca, codRatio=cr)  
        contexto = {                
            'queryset':regFilter,
        } 

    return render(request, 'proyecto/actualizarRatioSector.html', contexto)



def guardarModificacionRatioSector(request):
    ca = request.POST['codAct']
    cr = request.POST['codRat']
    valor = request.POST['valorRatio']

    regFilter = RatiosSector.objects.filter(codActividadEconomica=ca, codRatio=cr)

    if regFilter:
        queryset = RatiosSector.objects.get(codActividadEconomica=ca, codRatio=cr)  
        queryset.parametroComparacion = valor
        queryset.save()
             
    #return render(request, 'proyecto/consultarRatioSector.html', contexto)
    return redirect('analisisFinanciero:consultarRatioSector')



def eliminarRatioSector(request):
    ca = request.POST['codAct']
    cr = request.POST['codRat']

    if ca and cr:        
        regDelete = RatiosSector.objects.filter(codActividadEconomica=ca, codRatio=cr)
        
        if regDelete:
            regDelete = RatiosSector.objects.get(codActividadEconomica=ca, codRatio=cr)
            regDelete.delete()


    #return render(request, 'proyecto/consultarRatioSector.html', contexto)
    return redirect('analisisFinanciero:consultarRatioSector')


#-----------------------------------------------------------------------------------------------------------------


#---------------------------CRUD DE LA TABLA proyecto_empresa----------------------------------------------------------------------------


def insertarEmpresa(request):
    existe=""
    if request.method == 'POST':

        actividadEco = request.POST['actividades']
        codEmpresa = request.POST['codE']
        nomEmpresa = request.POST['nomE']
        descripcion = request.POST['descE']
        
        if actividadEco and codEmpresa and nomEmpresa:
            regfilter1 = ActividadEconomica.objects.filter(codActividadEconomica=actividadEco)

            if regfilter1:            
                regfilter = Empresa.objects.filter(codEmpresa=codEmpresa, codActividadEconomica=actividadEco)
            
                if regfilter:
                    existe="Ya existe un registro con los datos ingresados!!!"

                else:
                    queryset = Empresa(
                        codEmpresa=codEmpresa,
                        codActividadEconomica=ActividadEconomica.objects.get(codActividadEconomica=actividadEco),
                        nombreEmpresa=nomEmpresa, 
                        descripcionEmpresa=descripcion
                    )
                    queryset.save()
                    existe="Registro guardado satisfactoriamente!!!"


    actividad = ActividadEconomica.objects.all

    contexto = {
        'actividad':actividad,
        'exist':existe
    }

    return render(request,'proyecto/insertarEmpresa.html', contexto)



def consultarEmpresa(request, username):
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        i+=1
    emp = Empresa.objects.filter(codEmpresa=codEmp)
    contexto = {
            'empresas':emp,
    } 
    return render(request, 'proyecto/consultarEmpresa.html', contexto)

def consultarEmpresa(request, username):

    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        i+=1

    emp = Empresa.objects.filter(codEmpresa=codEmp)
    queryset= Empresa.objects.filter(codEmpresa=codEmp)


    contexto = {
            'empresas':emp,
            'queryset':queryset,
    }

    if request.method=='POST':

        empresa = request.POST['empresas']          

        if empresa:
            queryset = Empresa.objects.filter(codEmpresa=empresa)

            if queryset:              
                contexto = {   
                    'empresas':emp,                 
                    'queryset':queryset,
                }  
    
    return render(request, 'proyecto/consultarEmpresa.html', contexto)

def consultarEmpresaAdmin(request):

    emp = Empresa.objects.all
    queryset =Empresa.objects.all

    contexto = {
            'empresas':emp,
            'queryset':queryset,
    }

    if request.method=='POST':

        empresa = request.POST['empresas']          

        if empresa:
            queryset = Empresa.objects.filter(codEmpresa=empresa)

            if queryset:              
                contexto = {   
                    'empresas':emp,                 
                    'queryset':queryset,
                }       
    
    return render(request, 'proyecto/consultarEmpresa.html', contexto)



def actualizarEmpresa(request):   
    codEm = request.GET['codE']

    contexto = {}
         
    if codEm:            
        regFilter = Empresa.objects.get(codEmpresa=codEm)  
        contexto = {  
            'queryset':regFilter,
        } 

    return render(request, 'proyecto/actualizarEmpresa.html', contexto)



def guardarModificacionEmpresa(request):
    codEm = request.POST['codE']
    nomEm = request.POST['nomE']
    descripcion = request.POST['descE']

    regFilter = Empresa.objects.filter(codEmpresa=codEm)

    if regFilter:
        queryset = Empresa.objects.get(codEmpresa=codEm)
        queryset.nombreEmpresa = nomEm
        queryset.descripcionEmpresa = descripcion
        queryset.save()
             
    #return render(request, 'proyecto/consultarRatioSector.html', contexto)
    return redirect('analisisFinanciero:consultarEmpresaAdmin')


def actualizarEmpresa2(request):   
    codEm = request.GET['codE']

    contexto = {}
         
    if codEm:            
        regFilter = Empresa.objects.get(codEmpresa=codEm)  
        contexto = {  
            'queryset':regFilter,
        } 

    return render(request, 'proyecto/actualizarEmpresa2.html', contexto)



def guardarModificacionEmpresa2(request):
    codEm = request.POST['codE']
    nomEm = request.POST['nomE']
    descripcion = request.POST['descE']

    regFilter = Empresa.objects.filter(codEmpresa=codEm)

    if regFilter:
        queryset = Empresa.objects.get(codEmpresa=codEm)
        queryset.nombreEmpresa = nomEm
        queryset.descripcionEmpresa = descripcion
        queryset.save()
             
    #return render(request, 'proyecto/consultarRatioSector.html', contexto)
    return redirect('analisisFinanciero:index')



def eliminarEmpresa(request):
    codEm = request.POST['codE']

    if codEm:        
        regDelete = Empresa.objects.filter(codEmpresa=codEm)
        
        if regDelete:
            regDelete = Empresa.objects.get(codEmpresa=codEm)
            regDelete.delete()    
            

    #return render(request, 'proyecto/consultarRatioSector.html', contexto)
    return redirect('analisisFinanciero:consultarEmpresaAdmin')


#-----------------------------------------------------------------------------------------------------------------
class CatalogoListado(ListView):
    model = CatalogoCuenta #Llamada a la clase "CatalogoCuenta" en el archivo models.py
    
    
def consultarCatalogo(request, username):

    #Obtener el codigo de la empresa del Usuario
    usuarioRec = Usuario.objects.filter(username=username)
    i=0
    while(i<len(usuarioRec)):
        codEmp = usuarioRec[i].codEmpresa
        rol =usuarioRec[i].rol
        i+=1

    if rol == 'ADM':
        emp = Empresa.objects.all()
        queryset =CatalogoCuenta.objects.all()
    else:
        emp = Empresa.objects.filter(codEmpresa=codEmp)
        queryset= CatalogoCuenta.objects.filter(codEmpresa=codEmp)        
       
    contexto = {
            'empresas':emp,
            'queryset':queryset,
    }

    if request.method=='POST':
        empresa = request.POST['empresas']          
        if empresa:
            queryset = CatalogoCuenta.objects.filter(codEmpresa=empresa)
            if queryset:              
                contexto = {   
                    'empresas':emp,                 
                    'queryset':queryset,
                }      

    return render(request, 'proyecto/ConsultarCatalogo.html', contexto)



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


class CatalogoActualizar2(SuccessMessageMixin, UpdateView): 
    model = CatalogoCuenta 
    form = CatalogoCuentaForm 
    fields = "__all__" 
    success_message = '--Catalogo Actualizado Correctamente--'  
    
    def get_success_url(self):               
        return reverse('analisisFinanciero:index') 



class CatalogoEliminar(SuccessMessageMixin, DeleteView): 
    model = CatalogoCuenta
    form = CatalogoCuentaForm
    fields = "__all__"     
 
    # Redireccionamos a la página principal luego de eliminar un registro 
    def get_success_url(self): 
        success_message = '--Catalogo Eliminado Correctamente--' 
        messages.success (self.request, (success_message))       
        return reverse('analisisFinanciero:index') 


#----------------------------------------------------------------------------------------------------


def actualizarBalance(request):   
    codEmpresa = request.POST['codEmpresa']
    codCuenta = request.POST['codCuenta']
    año = request.POST['año']
         
    if codEmpresa and codCuenta and año:            
        regFilter = CuentaBalance.objects.get(codEmpresa=codEmpresa, año=año, codCuenta=codCuenta)
        contexto = {                
            'queryset':regFilter,
        } 

    return render(request, 'proyecto/actualizarBalance.html', contexto)



def guardarModificacionBalance(request):
    codEmpresa = request.POST['codEmpresa']
    codCuenta = request.POST['codCuenta']
    año = request.POST['año']
    valor = request.POST['valorBalance']

    regFilter = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año, codCuenta=codCuenta)

    if regFilter:
        queryset = CuentaBalance.objects.get(codEmpresa=codEmpresa, año=año, codCuenta=codCuenta)
        queryset.valor = valor
        queryset.save()
             
    return redirect('analisisFinanciero:index')
