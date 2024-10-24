import datetime

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, YearArchiveView, MonthArchiveView, CreateView

from main.models import Pagamento
from .models import Saida


class IndexView(UserPassesTestMixin, TemplateView):
    template_name = "index.html"

    def test_func(self):
        return self.request.user.tipo == 'admin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagamentos"] = Pagamento.objects.order_by('-data')[:7]
        context["saidas"] = Saida.objects.order_by('-data')[:7]
        today = datetime.datetime.today()
        context["current_year"] = today.year
        context["current_month"] = today.month
        return context


class PagamentosPendentesView(UserPassesTestMixin, ListView):
    model = Pagamento
    template_name = "confirmar_pagamento.html"

    def test_func(self):
        return self.request.user.is_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagamentos_pendentes = Pagamento.objects.filter(confirmado=False).order_by('-data')
        context["pagamentos"] = pagamentos_pendentes
        total_pendente = pagamentos_pendentes.aggregate(total=Coalesce(Sum('valor'), Value(0), output_field=DecimalField()))
        formatted_value = f"{total_pendente['total']:.2f}".replace('.', ',')
        context["pendente"] = formatted_value
        return context


class ConfirmarPagamentoView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_admin
    
    def get(self, request, pk):
        rows_updated = Pagamento.objects.filter(pk=pk).update(confirmado=True)
        if rows_updated == 0:
            raise Http404("Pagamento não encontrado")
        pagamento = Pagamento.objects.get(pk=pk)
        jogador_nome = pagamento.jogador.nome_jogador if pagamento.jogador else ''
        messages.success(self.request, f'Pagamento de {jogador_nome} em {pagamento.data} confirmado!')
        return redirect('financeiro:pagamentos_pendentes')
    

class DeletarPagamentoView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_admin
    
    def get(self, request, pk):
        try:
            pagamento = Pagamento.objects.get(pk=pk)
            jogador_nome = pagamento.jogador.nome_jogador if pagamento.jogador else None
            data_pagamento = pagamento.data
            pagamento.delete()
            if jogador_nome:
                messages.warning(self.request, f'Pagamento de {jogador_nome} em {data_pagamento} foi deletado.')
            else:
                messages.warning(self.request, f'Pagamento em {data_pagamento} deletado!')
        except Pagamento.DoesNotExist:
            raise Http404("Pagamento não encontrado")
        return redirect('financeiro:pagamentos_pendentes')


class SaidaCreateView(UserPassesTestMixin, CreateView):
    model = Saida
    template_name = "lancar_saida.html"
    fields = ['descricao', 'valor', 'partida']
    success_url = reverse_lazy('financeiro:menu_financeiro')

    def test_func(self):
        return self.request.user.is_admin
    
    def form_valid(self, form):
        valor = form.cleaned_data.get('valor')
        if valor <= 0:
            messages.error(self.request, 'O valor da saída deve ser positivo.')
            return self.form_invalid(form)
        messages.success(self.request, 'Saída lançada!')
        return super().form_valid(form)


class LancarEntradaView(UserPassesTestMixin, CreateView):
    template_name = 'lancar_pagamento.html'
    model = Pagamento
    fields = ['comprovante', 'jogador', 'partida', 'em_dinheiro', 'valor', 'descricao']
    success_url = reverse_lazy('financeiro:pagamentos_pendentes')

    def test_func(self):
        return self.request.user.is_admin
    
    def form_valid(self, form):
        valor = form.cleaned_data.get('valor')
        if valor <= 0:
            messages.error(self.request, 'O valor do pagamento deve ser positivo.')
            return self.form_invalid(form)
        messages.success(self.request, 'Entrada lançada! Confirme-a.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Algo deu errado!')
        return super().form_invalid(form)


class PagamentoYearArchiveView(UserPassesTestMixin, YearArchiveView):
    queryset = Pagamento.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/pagamentos_por_ano.html'
    context_object_name = 'pagamentos'

    def test_func(self):
        return self.request.user.is_admin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_month"] = datetime.datetime.today().month
        return context


class PagamentoMonthArchiveView(UserPassesTestMixin, MonthArchiveView):
    queryset = Pagamento.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/pagamentos_por_mes.html'
    context_object_name = 'pagamentos'

    def test_func(self):
        return self.request.user.is_admin

    
class SaidasYearArchiveView(UserPassesTestMixin, YearArchiveView):
    queryset = Saida.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/saidas_por_ano.html'
    context_object_name = 'pagamentos'

    def test_func(self):
        return self.request.user.is_admin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_month"] = datetime.datetime.today().month
        return context


class SaidasMonthArchiveView(UserPassesTestMixin, MonthArchiveView):
    queryset = Saida.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/saidas_por_mes.html'
    context_object_name = 'pagamentos'

    def test_func(self):
        return self.request.user.is_admin