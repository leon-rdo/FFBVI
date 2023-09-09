from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, FormView, DeleteView, CreateView, UpdateView
from django.contrib.auth.views import PasswordChangeView

from .models import *
from .forms import PagamentoForm, PartidaForm, UserUpdateForm, RegistrationForm, AdicionarConvidadoForm, AdicionarConvidadoExistenteForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages

import datetime
import random


class IndexView(ListView):
    template_name = "main/index.html"
    model = User
    context_object_name = "users"

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(tipo__in=['federado', 'admin'])
        randomized_queryset = list(filtered_queryset)
        random.shuffle(randomized_queryset)
        return randomized_queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        partida = None
        try:
            partida = Partida.objects.filter(data=today, sorteada=True).first()
        except IndexError:
            pass
        context['partida'] = partida
        context['alerta'] = Configuracao.objects.first()
        context['noticias'] = Noticia.objects.all()
        return context
   

class FederadosView(ListView):
    template_name = "main/federados.html"
    model = User
    context_object_name = "users"

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(tipo__in=['federado', 'admin'])
        randomized_queryset = list(filtered_queryset)
        random.shuffle(randomized_queryset)
        return randomized_queryset


class PatrocinadoresView(ListView):
    template_name = 'main/patrocinadores.html'
    model = Patrocinador


class RegrasView(TemplateView):
    template_name = "main/regras.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regras'] = Configuracao.objects.first()
        return context


class MeuPerfilView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "main/meu_perfil.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy('main:homepage')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user

        user.nome_completo = form.cleaned_data['nome_completo']
        user.nome_jogador = form.cleaned_data['nome_jogador']
        user.posicao = form.cleaned_data['posicao']
        user.email = form.cleaned_data['email']
        user.telefone = form.cleaned_data['telefone']
        user.time_coracao = form.cleaned_data['time_coracao']
        user.data_nascimento = form.cleaned_data['data_nascimento']
        user.uf_nascimento = form.cleaned_data['uf_nascimento']
        user.cidade_nascimento = form.cleaned_data['cidade_nascimento']
        user.altura = form.cleaned_data['altura']

        user.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form.errors:
            error_message = form.errors[field][0]
            messages.error(self.request, f'Erro no campo "{form.fields[field].label}": {error_message}')
            
        return super().form_invalid(form)


    def test_func(self):
        user = self.request.user
        return user.tipo != 'convidado'


class ChangePasswordView(LoginRequiredMixin, UserPassesTestMixin, PasswordChangeView):
    template_name = 'registration/mudar_senha.html'
    success_url = reverse_lazy('main:homepage')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['password_changed'] = True
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Senha atual errada.')
        return super().form_invalid(form)

    def test_func(self):
        user = self.request.user
        return user.tipo != 'convidado'


class GerenciarFederadosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "main/gerenciar_federados.html"
    model = User
    ordering = ['nome_jogador']
    context_object_name = "users"

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.exclude(tipo='convidado')
        return filtered_queryset


class GerenciarFederadoView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "main/gerenciar_federado.html"
    model = User
    context_object_name = "federado"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'


class AdicionarFederadoView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "main/adicionar_federado.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('main:gerenciar_federados')

    DEFAULT_PASSWORD = 'FFBVI@23'

    def form_valid(self, form):

        user = User()

        user.nome_jogador = form.cleaned_data['nome_jogador']
        user.posicao = form.cleaned_data['posicao']
        user.set_password(self.DEFAULT_PASSWORD)

        user.save()

        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'


class PartidasView(ListView):
    template_name = 'main/partidas.html'
    model = Partida
    context_object_name = 'partidas'
    ordering = ['-data']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.datetime.today()
        context['now'] = now
        partida_proxima = None
        try:
            partida_proxima = Partida.objects.filter(data__gte=now).order_by('data')[0]
        except IndexError:
            pass
        context['partida_proxima'] = partida_proxima
        return context


class PartidaView(DetailView, FormView):
    template_name = 'main/partida.html'
    model = Partida
    form_class = PartidaForm
    
    def get_partida(self):
        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])
        return partida

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partida = self.get_partida()
        user = self.request.user
        if not user.is_authenticated:
            user = None
        pagamento_usuario = Pagamento.objects.filter(jogador=user, partida=partida).exists()
        context["pagamento_usuario"] = pagamento_usuario
        now = datetime.datetime.today()
        context["now"] = datetime.datetime.today()
        dia_anterior = partida.data - datetime.timedelta(days=1)
        context["dia_anterior"] = dia_anterior
        porcentagem_lotacao = (partida.relacionados.count() / 18) * 100
        context["porcentagem"] = int(porcentagem_lotacao)
        partida_proxima = None
        try:
            partida_proxima = Partida.objects.filter(data__gte=now).order_by('data')[0]
        except IndexError:
            pass
        context['partida_proxima'] = partida_proxima
        return context

    def form_valid(self, form):
        partida = self.get_partida()
        partida.data = form.cleaned_data['data']
        partida.hora = form.cleaned_data['hora']
        partida.save()
        messages.success(self.request, 'Informações da partida alteradas com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocorreu um erro ao atualizar os dados da partida.')
        return super().form_invalid(form)

    def confirmar_presenca(self, request, *args, **kwargs):
        partida = self.get_partida()
        user = self.request.user

        if partida.relacionados.filter(id=user.id).exists():
            messages.warning(request, 'Você já está relacionado.')
            return self.get(request, *args, **kwargs)
        else:
            partida.relacionados.add(user)
            partida.save()
            messages.success(request, 'Você foi adicionado aos relacionados.')

        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'confirmar_presenca' in request.POST:
            return self.confirmar_presenca(request, *args, **kwargs)
        else:
            return super().post(request, *args, **kwargs)

    def get_success_url(self):
        partida = self.get_partida()
        return reverse_lazy('main:partida', kwargs={'slug': partida.slug})


class CaraDaPartidaView(UpdateView):
    model = Partida
    fields = ['...']
    success_url = reverse_lazy('main:...')
    template_name ='main/cara_da_partida.html'


class PagamentoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'main/pagamento.html'
    model = Pagamento
    form_class = PagamentoForm

    def form_valid(self, form):
        pagamento = form.save(commit=False)
        pagamento.jogador = self.request.user
        pagamento.partida = self.get_partida()

        em_dinheiro = form.cleaned_data['em_dinheiro']
        if em_dinheiro:
            pagamento.em_dinheiro = True
            pagamento.comprovante = None
        else:
            comprovante = self.request.FILES.get('comprovante')
            if comprovante:
                pagamento.comprovante = comprovante

        pagamento.save()
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return user.tipo != 'convidado'

    def get_partida(self):
        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])
        return partida

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partida = self.get_partida()
        user = self.request.user
        pagamento_usuario = Pagamento.objects.filter(jogador=user, partida=partida).exists()
        context["pagamento_usuario"] = pagamento_usuario
        context['partida'] = partida
        context['config'] = Configuracao.objects.first()
        return context

    def get_success_url(self):
        partida = self.get_partida()
        return reverse_lazy('main:partida', kwargs={'slug': partida.slug})


class AdicionarConvidadoView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'main/adicionar_convidado.html'
    model = User
    form_class = AdicionarConvidadoForm

    def get_partida(self):
        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])
        return partida

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["partida"] = self.get_partida()
        return context

    DEFAULT_PASSWORD = 'CONVIDADO@23'

    def form_valid(self, form):
        
        convidado = User()
        convidado.nome_jogador = form.cleaned_data['nome_jogador']
        convidado.posicao = form.cleaned_data['posicao']
        convidado.set_password(self.DEFAULT_PASSWORD)
        convidado.tipo = 'convidado'
        convidado.save()
        
        self.condidado = convidado
        
        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])

        if partida.relacionados.filter(id=convidado.id).exists():
            messages.warning(self.request, 'Convidado já está relacionado a esta partida.')
            return redirect('main:adicionar_convidado', slug=self.kwargs['slug'])

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Este nome já existe!')
        return super().form_invalid(form)
    
    def get_success_url(self):
        partida = self.get_partida()
        convidado_id = self.condidado.id
        return reverse_lazy('main:pagamento_convidado', kwargs={'slug': partida.slug, 'convidado_id': convidado_id})

    def test_func(self):
        user = self.request.user
        return user.tipo != 'convidado'


class AdicionarConvidadoExistenteView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'main/adicionar_convidado_existente.html'
    model = User
    form_class = AdicionarConvidadoExistenteForm

    def get_partida(self):
        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])
        return partida

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partida = self.get_partida()
        context["partida"] = partida
        return context

    def get_success_url(self):
        partida = self.get_partida()
        convidado_id = self.request.POST.get('convidado')
        return reverse_lazy('main:pagamento_convidado', kwargs={'slug': partida.slug, 'convidado_id': convidado_id})


    DEFAULT_PASSWORD = 'CONVIDADO@23'
    
    def form_valid(self, form):

        convidado_existente = form.cleaned_data['convidado']
        if convidado_existente is None:
            messages.warning(self.request, 'Selecione alguém!')
            return redirect('main:convidado_existente', slug=self.kwargs['slug'])
        
        convidado = User.objects.get(id=convidado_existente.id)

        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])

        if partida.relacionados.filter(id=convidado.id).exists():
            messages.warning(self.request, 'O convidado já está relacionado a esta partida.')
            return redirect('main:convidado_existente', slug=self.kwargs['slug'])

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Ocorreu um erro ao adicionar seu convidado.')
        return super().form_invalid(form)

    def test_func(self):
        user = self.request.user
        return user.tipo != 'convidado'


class PagamentoConvidadoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'main/pagamento_convidado.html'
    model = Pagamento
    form_class = PagamentoForm

    def dispatch(self, request, *args, **kwargs):
        convidado_id = kwargs.get('convidado_id')
        self.convidado = get_object_or_404(User, id=convidado_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        pagamento = form.save(commit=False)
        pagamento.jogador = self.convidado
        pagamento.partida = self.get_partida()
        em_dinheiro = form.cleaned_data['em_dinheiro']
        
        if em_dinheiro:
            pagamento.em_dinheiro = True
            pagamento.comprovante = None
        else:
            comprovante = self.request.FILES.get('comprovante')
            if comprovante:
                pagamento.comprovante = comprovante

        pagamento.save()
        
        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])

        if partida.relacionados.filter(id=self.convidado.id).exists():
            messages.warning(self.request, 'O convidado já está relacionado a esta partida.')
            return redirect('main:convidado_existente', slug=self.kwargs['slug'])

        partida.relacionados.add(self.convidado)

        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return user.tipo != 'convidado'

    def get_partida(self):
        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])
        return partida

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partida'] = self.get_partida()
        context['convidado'] = self.convidado
        context['config'] = Configuracao.objects.first()
        return context

    def get_success_url(self):
        partida = self.get_partida()
        return reverse_lazy('main:partida', kwargs={'slug': partida.slug})


class PagamentosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/pagamentos.html'
    model = Pagamento
    context_object_name = "pagamentos"

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        filtered_queryset = queryset.filter(partida=slug)
        return filtered_queryset

    def test_func(self):
        user = self.request.user
        return user.tipo != 'convidado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])
        context['partida'] = partida
        return context


class PartidaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Partida
    success_url = reverse_lazy('main:partidas')

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'


class CriarPartidaView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'main/criar_partida.html'
    model = Partida
    form_class = PartidaForm
    success_url = reverse_lazy('main:partidas')

    def form_valid(self, form):

        partida = Partida()

        partida.data = form.cleaned_data['data']
        partida.hora = form.cleaned_data['hora']

        partida.save()

        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return user.tipo == 'admin'