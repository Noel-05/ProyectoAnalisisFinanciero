from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'analisisFinanciero'

urlpatterns = [
    path('', index),
    path('analisisFinanciero/index/', index, name='index'),
    path('analisisFinanciero/subirBalance/', subirBalance, name="subirBalance"),
    path('analisisFinanciero/consultaBalance', consultarBalance, name="consultarBalance"),
    path('analisisFinanciero/Balances', filtrarBalance, name="filtrarBalance"),

]
