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

        queryset = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año)

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

        #Obtengo los datos del año anterior
        año2 = int(año) - 1
        queryset2 = CuentaBalance.objects.filter(codEmpresa=codEmpresa, año=año2)

    #PROCEDIMIENTO DE CALCULO DE RATIOS.

        #Recuperacion de valores para el año solicitado
        i=0
        while(i < len(queryset)):
            tipo = queryset[i].codCuenta.codTipoCuenta_id
            print(tipo)
            if(tipo == "EFEC"):
                efectivo = queryset[i].valor
                print(efectivo)
            elif(tipo == "INV"):
                inventario = queryset[i].valor
                print(inventario)
            elif(tipo == "ACCIR"):
                actCirculante = queryset[i].valor
                print(actCirculante)
            elif(tipo == "COSVEN"):
                costoVentas = queryset[i].valor
                print(costoVentas)
            i+=1

        print(" ")
        #print(efectivo)
        print(inventario)
        #print(actCirculante)
        print(costoVentas)
        print(" ")

        #Recuperacion de valores para el año anterior para sacar el Promedio
        if( len(queryset2) != 0):
            j=0
            while(j < len(queryset2)):
                tipo2 = queryset2[j].codCuenta.codTipoCuenta_id
                print(tipo2)
                if(tipo2 == "EFEC"):
                    efectivo2 = queryset2[j].valor
                    print(efectivo2)
                elif(tipo2 == "INV"):
                    inventario2 = queryset2[j].valor
                    print(inventario2)
                elif(tipo2 == "ACCIR"):
                    actCirculante2 = queryset2[j].valor
                    print(actCirculante2)
                elif(tipo2 == "COSVEN"):
                    costoVentas2 = queryset2[j].valor
                    print(costoVentas2)
                j+=1
        
            #Calculo de Inventario Promedio
            if(inventario2 >= 0):
                inventarioPromedio = (inventario2 + inventario) / 2
        else:
            inventarioPromedio = inventario
        
        #Calculo del Ratio
        razonRotInve = costoVentas / inventarioPromedio
        
        print(" ")
        print(razonRotInve)
        print(" ")
        #print(inventario2)
        #print(costoVentas2)

        #Calculos de los ratios
        codRatio="RRI"
        comprobar = RatiosEmpresa.objects.filter(codRatio_id=codRatio, codEmpresa_id=codEmpresa, año=año)
        if(len(comprobar) == 0):
            ratioRazRotInv = RatiosEmpresa(codRatio_id=codRatio, valorRatioEmpresa=razonRotInve , codEmpresa_id=codEmpresa, año=año)
            ratioRazRotInv.save()
        
    #FIN PROCEDIMIENTO DE CALCULO DE RATIOS.

        consulta = RatiosEmpresa.objects.filter(codEmpresa_id=codEmpresa, año=año)

        contexto = {
            'queryset': queryset,
            'consulta': consulta, 
        }

        return render(
            request,
            'proyecto/ConsultaRazonActividad.html', contexto
        )



