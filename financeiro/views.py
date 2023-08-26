from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, ListView
from main.models import Pagamento, Partida
from django.contrib import messages

class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagamentos"] = Pagamento.objects.all()
        context["partidas"] = Partida.objects.all()
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
        messages.success(self.request, f'Pagamento de {pagamento.jogador.nome_jogador} confirmado!')
        return redirect('financeiro:pagamentos_pendentes')
