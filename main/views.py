from django.views.generic import TemplateView, ListView, DetailView, FormView, DeleteView, CreateView, UpdateView
from django.contrib.auth.views import PasswordChangeView

from .models import *
from .forms import GolForm, PagamentoForm, PartidaForm, UserUpdateForm, RegistrationForm, AdicionarConvidadoForm, AdicionarConvidadoExistenteForm

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

        context['alerta'] = Configuracao.objects.first()

        context['noticias'] = Noticia.objects.all()[:3]

        ultima_partida = Partida.objects.filter(data__lt=datetime.date.today()).order_by('-data').first()
        if ultima_partida:
            context['cara_da_partida'] = ultima_partida.cara_da_partida 
            context['artilheiro'] = ultima_partida.artilheiro

            partida_destaque = Partida.objects.filter(data__gte=datetime.date.today()).order_by('data').first() or ultima_partida

            context['partida_destaque'] = partida_destaque
            context['anterior'] = partida_destaque == ultima_partida

            context["votos_do_cara"] = Voto.objects.filter(partida=ultima_partida, votou_em=ultima_partida.cara_da_partida).count()

        context['current_year'] = datetime.date.today().year

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
        return self.request.user.tipo != 'convidado'


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
        return self.request.user.tipo != 'convidado'


class GerenciarFederadosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "main/gerenciar_federados.html"
    model = User
    ordering = ['nome_jogador']
    context_object_name = "users"

    def test_func(self):
        return self.request.user.is_admin

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
        return self.request.user.is_admin


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
        return self.request.user.is_admin


class PartidasView(ListView):
    template_name = 'main/partidas.html'
    model = Partida
    context_object_name = 'partidas'
    ordering = ['-data']
    paginate_by = 9


class PartidaView(DetailView, FormView):
    template_name = 'main/partida.html'
    model = Partida
    form_class = PartidaForm

    def get_object(self, queryset=None):
        return get_object_or_404(Partida, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partida = self.object
        user = self.request.user
        if not user.is_authenticated:
            user = None
        pagamento_usuario = Pagamento.objects.filter(jogador=user, partida=partida).first()
        context["pagamento_usuario"] = pagamento_usuario
        now = datetime.datetime.today()
        context["now"] = now
        dia_anterior = partida.data - datetime.timedelta(days=1)
        context["dia_anterior"] = dia_anterior
        porcentagem_lotacao = (partida.relacionados.count() / 18) * 100
        context["porcentagem"] = int(porcentagem_lotacao)
        partida_proxima = Partida.objects.filter(data__gte=now).order_by('data').first()
        context['partida_proxima'] = partida_proxima
        context["votos_do_cara"] = Voto.objects.filter(partida=partida, votou_em=partida.cara_da_partida).count()
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


class CaraDaPartidaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Voto
    fields = ['votou_em']
    template_name ='main/cara_da_partida.html'

    def test_func(self):
        return self.request.user.tipo != 'convidado'
    
    def get_partida(self):
        if not hasattr(self, '_partida'):
            self._partida = get_object_or_404(Partida, slug=self.kwargs['slug'])
        return self._partida

    def form_valid(self, form):
        partida = self.get_partida()
        usuario_ja_votou = Voto.objects.filter(partida=partida, jogador=self.request.user).first()
        
        if usuario_ja_votou:
            messages.warning(self.request, 'Você já votou nesta partida.')
            return redirect('main:partida', slug=partida.slug)
        elif (partida.data + datetime.timedelta(days=1)) < timezone.now().date():
            messages.error(self.request, 'O prazo para votar já expirou!')
            return redirect('main:partida', slug=partida.slug)
        
        voto = form.save(commit=False)
        voto.jogador = self.request.user
        voto.partida = partida

        if voto.jogador == voto.votou_em:
            messages.error(self.request, 'Um jogador não pode votar em si mesmo.')
            return redirect('main:cara_partida', slug=partida.slug)

        if voto.votou_em not in partida.relacionados.all():
            messages.error(self.request, 'O jogador votado não participou da partida.')
            return redirect('main:cara_partida', slug=partida.slug)

        voto.save()
        
        messages.success(self.request, f'Você votou em {voto.votou_em}.')
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partida = self.get_partida()
        context['slug'] = partida.slug
        user_vote = Voto.objects.filter(partida=partida, jogador=self.request.user).first()

        context['usuario_ja_votou'] = user_vote is not None

        if user_vote:
            context['voto_usuario'] = user_vote

        return context
    
    def get_success_url(self):
        partida_slug = self.kwargs['slug']
        return reverse_lazy('main:partida', kwargs={'slug': partida_slug})
    

class GolView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    model = Gol
    template_name = "main/gols.html"
    form_class = GolForm

    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_staff
    
    def form_valid(self, form):
        partida = get_object_or_404(Partida, slug=self.kwargs['slug'])
        gol, created = Gol.objects.get_or_create(
            jogador=form.cleaned_data['jogador'], 
            partida=partida, 
            defaults={'quantidade': form.cleaned_data['quantidade']}
        )
        if not created:
            gol.quantidade = form.cleaned_data['quantidade']
            gol.save()

        if created:
            messages.success(self.request, 'Gol(s) registrado(s)!')
        else:
            messages.success(self.request, 'Quantidade de gols atualizada!')

        return super().form_valid(form)

    def get_success_url(self):
        partida_slug = self.kwargs['slug']
        return reverse_lazy('main:gols', kwargs={'slug': partida_slug})  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gols'] = Gol.objects.filter(partida=self.kwargs['slug'])
        return context
  

class MudarVotoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Voto
    fields = ['votou_em']
    template_name = "main/mudar_voto.html"

    def test_func(self):
        """Verifica se o usuário não é um convidado."""
        return self.request.user.tipo != 'convidado'
    
    def get_success_url(self):
        """Retorna a URL de sucesso após a atualização do voto."""
        partida_slug = self.kwargs['slug']
        return reverse_lazy('main:partida', kwargs={'slug': partida_slug})
    
    def form_valid(self, form):
        """Verifica se a form é válida e se o prazo para votar ainda não expirou."""
        partida_slug = self.kwargs['slug']
        partida = get_object_or_404(Partida, slug=partida_slug)
        if self._prazo_votacao_expirou(partida.data):
            messages.error(self.request, 'O prazo para votar já expirou!')
            return redirect('main:partida', slug=partida_slug)
        return super().form_valid(form)
    
    def _prazo_votacao_expirou(self, data_partida):
        """Verifica se o prazo para votação expirou."""
        return (data_partida + datetime.timedelta(days=1)) < timezone.now().date()


class PagamentoView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'main/pagamento.html'
    model = Pagamento
    form_class = PagamentoForm

    def test_func(self):
        """Verifica se o usuário não é um convidado."""
        return self.request.user.tipo != 'convidado'

    def form_valid(self, form):
        pagamento = Pagamento()
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
        
        messages.success(self.request, 'Pagamento efetuado com sucesso! Ingresse na partida.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Erro no campo "{form.fields[field].label}". {error}')
        
        return super().form_invalid(form)

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

    def test_func(self):
        return self.request.user.tipo != 'convidado'

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


class AdicionarConvidadoExistenteView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'main/adicionar_convidado_existente.html'
    model = User
    form_class = AdicionarConvidadoExistenteForm

    def test_func(self):
        return self.request.user.tipo != 'convidado'

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


class PagamentoConvidadoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'main/pagamento_convidado.html'
    model = Pagamento
    form_class = PagamentoForm

    def test_func(self):
        return self.request.user.tipo != 'convidado'

    def dispatch(self, request, *args, **kwargs):
        convidado_id = kwargs.get('convidado_id')
        self.convidado = get_object_or_404(User, id=convidado_id)
        self.partida = self.get_partida()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.partida.relacionados.filter(id=self.convidado.id).exists():
            messages.warning(self.request, 'O convidado já está relacionado a esta partida.')
            return redirect('main:convidado_existente', slug=self.kwargs['slug'])

        pagamento = form.save(commit=False)
        pagamento.jogador = self.convidado
        pagamento.partida = self.partida
        em_dinheiro = form.cleaned_data['em_dinheiro']
        
        if em_dinheiro:
            pagamento.em_dinheiro = True
            pagamento.comprovante = None
        else:
            comprovante = self.request.FILES.get('comprovante')
            if not comprovante:
                messages.error(self.request, 'Comprovante não fornecido.')
                return self.form_invalid(form)
            pagamento.comprovante = comprovante

        pagamento.save()
        self.partida.relacionados.add(self.convidado)

        return super().form_valid(form)

    def get_partida(self):
        return get_object_or_404(Partida, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partida'] = self.partida
        context['convidado'] = self.convidado
        context['config'] = Configuracao.objects.first()
        return context

    def get_success_url(self):
        return reverse_lazy('main:partida', kwargs={'slug': self.partida.slug})


def desconfirmar_presenca(request, slug):
    partida = get_object_or_404(Partida, slug=slug)
    jogador = get_object_or_404(User, id=request.user.id)
    partida.relacionados.remove(jogador)
    messages.warning(request, 'Você foi removido dos relacionados.')
    return redirect('main:partida', slug=slug)


class PagamentosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/pagamentos.html'
    model = Pagamento
    context_object_name = "pagamentos"

    def test_func(self):
        return self.request.user.tipo != 'convidado'

    def get_queryset(self):
        slug = self.kwargs['slug']
        if not slug:
            return self.model.objects.none()
        return self.model.objects.filter(partida=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partida'] = get_object_or_404(Partida, slug=self.kwargs['slug'])
        return context


class PartidaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Partida
    success_url = reverse_lazy('main:partidas')

    def test_func(self):
        return self.request.user.is_admin


class CriarPartidaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'main/criar_partida.html'
    model = Partida
    form_class = PartidaForm
    success_url = reverse_lazy('main:partidas')

    def test_func(self):
        return self.request.user.is_admin