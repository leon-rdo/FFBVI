from django.urls import path
from .views import *

app_name = 'financeiro'
urlpatterns = [
    path('', IndexView.as_view(), name='menu_financeiro'),
    path('pagamentos-pendentes/', PagamentosPendentesView.as_view(), name='pagamentos_pendentes'),
    path('confirmar-pagamento/<int:pk>', ConfirmarPagamentoView.as_view(), name='confirmar_pagamento'),
    path('pagamentos/ano/<int:year>/', PagamentoYearArchiveView.as_view(), name='pagamento_year'),
    path('pagamentos/mes/<int:year>/<int:month>/', PagamentoMonthArchiveView.as_view(month_format="%m"), name='pagamento_month'),
    path('saidas/ano/<int:year>/', SaidasYearArchiveView.as_view(), name='saida_year'),
    path('saidas/mes/<int:year>/<int:month>/', SaidasMonthArchiveView.as_view(month_format="%m"), name='saida_month'),
    path('lancar-entrada/', LancarEntradaView.as_view(), name='lancar_entrada'),
    path('lancar-saida/', SaidaCreateView.as_view(), name='lancar_saida'),
]

