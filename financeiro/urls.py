from django.urls import path
from .views import *

app_name = 'financeiro'
urlpatterns = [
    path('', IndexView.as_view(), name='menu_financeiro'),
    path('pagamentos-pendentes/', PagamentosPendentesView.as_view(), name='pagamentos_pendentes'),
    path('confirmar-pagamento/<int:pk>', ConfirmarPagamentoView.as_view(), name='confirmar_pagamento'),
]

