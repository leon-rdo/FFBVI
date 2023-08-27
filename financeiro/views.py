from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, YearArchiveView, MonthArchiveView, CreateView
from main.models import Pagamento, Partida
from .models import Saida
from django.contrib import messages

class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagamentos"] = Pagamento.objects.all()
        context["partidas"] = Partida.objects.all()
        context['saidas'] = Saida.objects.all()
        return context
    
class PagamentosPendentesView(ListView):
    model = Pagamento
    template_name = "confirmar_pagamento.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagamentos"] = Pagamento.objects.filter(confirmado=False)
        return context

class ConfirmarPagamentoView(View):
    def get(self, request, pk):
        pagamento = Pagamento.objects.get(pk=pk)
        pagamento.confirmado = True
        pagamento.save()
        messages.success(self.request, f'Pagamento de {pagamento.jogador.nome_jogador} em {pagamento.data} confirmado!')
        return redirect('financeiro:pagamentos_pendentes')


class SaidaCreateView(CreateView):
    model = Saida
    template_name = "lancar_saida.html"
    fields = ['descricao', 'valor', 'partida']
    success_url = reverse_lazy('financeiro:menu_financeiro')
    
    def form_valid(self, form):
        messages.success(self.request, f'Saída lançada!')
        return super().form_valid(form)


class PagamentoYearArchiveView(YearArchiveView):
    queryset = Pagamento.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/pagamentos_por_ano.html'
    context_object_name = 'pagamentos'

class PagamentoMonthArchiveView(MonthArchiveView):
    queryset = Pagamento.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/pagamentos_por_mes.html'
    context_object_name = 'pagamentos'
