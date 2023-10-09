from django.views.generic import TemplateView, ListView, YearArchiveView, MonthArchiveView, CreateView
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from main.models import Pagamento
from .models import Saida

from django.db.models import Sum
import datetime


class IndexView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagamentos"] = Pagamento.objects.order_by('-data')[:7]
        context["saidas"] = Saida.objects.order_by('-data')[:7]
        context["current_year"] = datetime.datetime.today().year
        context["current_month"] = datetime.datetime.today().month
        return context

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'


class PagamentosPendentesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Pagamento
    template_name = "confirmar_pagamento.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagamentos"] = Pagamento.objects.filter(confirmado=False).order_by('-data')
        total_pendente = Pagamento.objects.filter(confirmado=False).aggregate(total=Sum('valor'))
        if total_pendente['total'] is None:
            context["pendente"] = "0,00"
        else:
            formatted_value = f"{total_pendente['total']:.2f}".replace('.', ',')
            context["pendente"] = formatted_value
        return context

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'


class ConfirmarPagamentoView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        pagamento = Pagamento.objects.get(pk=pk)
        pagamento.confirmado = True
        pagamento.save()
        if pagamento.jogador is not None:
            messages.success(self.request, f'Pagamento de {pagamento.jogador.nome_jogador} em {pagamento.data} confirmado!')
        else:
            messages.success(self.request, f'Pagamento em {pagamento.data} confirmado!')
        return redirect('financeiro:pagamentos_pendentes')

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'
    

class DeletarPagamentoView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        pagamento = Pagamento.objects.get(pk=pk)
        pagamento.delete()
        if pagamento.jogador is not None:
            messages.warning(self.request, f'Pagamento de {pagamento.jogador.nome_jogador} em {pagamento.data} foi deletado.')
        else:
            messages.warning(self.request, f'Pagamento em {pagamento.data} deletado!')
        return redirect('financeiro:pagamentos_pendentes')

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'


class SaidaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Saida
    template_name = "lancar_saida.html"
    fields = ['descricao', 'valor', 'partida']
    success_url = reverse_lazy('financeiro:menu_financeiro')
    
    def form_valid(self, form):
        messages.success(self.request, 'Saída lançada!')
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'


class LancarEntradaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'lancar_pagamento.html'
    model = Pagamento
    fields = ['comprovante', 'jogador', 'partida', 'em_dinheiro', 'valor', 'descricao']
    success_url = reverse_lazy('financeiro:pagamentos_pendentes')
    
    def form_valid(self, form):
        if not form.cleaned_data.get('comprovante'):
            form.instance.comprovante = None
        if not form.cleaned_data.get('jogador'):
            form.instance.jogador = None
        if not form.cleaned_data.get('partida'):
            form.instance.partida = None

        messages.success(self.request, 'Entrada lançada! Confirme-a.')

        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Algo deu errado!')
        return super().form_invalid(form)

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'


class PagamentoYearArchiveView(LoginRequiredMixin, UserPassesTestMixin, YearArchiveView):
    queryset = Pagamento.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/pagamentos_por_ano.html'
    context_object_name = 'pagamentos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_month"] = datetime.datetime.today().month
        return context

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'

class PagamentoMonthArchiveView(LoginRequiredMixin, UserPassesTestMixin, MonthArchiveView):
    queryset = Pagamento.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/pagamentos_por_mes.html'
    context_object_name = 'pagamentos'

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'

    
class SaidasYearArchiveView(LoginRequiredMixin, UserPassesTestMixin, YearArchiveView):
    queryset = Saida.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/saidas_por_ano.html'
    context_object_name = 'pagamentos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_month"] = datetime.datetime.today().month
        return context

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'


class SaidasMonthArchiveView(LoginRequiredMixin, UserPassesTestMixin, MonthArchiveView):
    queryset = Saida.objects.all()
    date_field = "data"
    make_object_list = True
    allow_future = True
    allow_empty = True
    template_name = 'arquivo/saidas_por_mes.html'
    context_object_name = 'pagamentos'

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'