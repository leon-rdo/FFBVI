from django.urls import path
from .views import *

app_name = 'main'
urlpatterns = [
    path('', IndexView.as_view(), name='homepage'),
    path('federados/', FederadosView.as_view(), name='federados'),
    path('regras/', RegrasView.as_view(), name='regras'),
    path('meu-perfil/', MeuPerfilView.as_view(), name='meu_perfil'),
    path('meu-perfil/mudar-senha/', ChangePasswordView.as_view(), name='mudar_senha'),
    path('adicionar-federado/', AdicionarFederadoView.as_view(), name='adicionar_federado'),
    path('partidas/', PartidasView.as_view(), name='partidas'),
    path('partidas/criar-partida/', CriarPartidaView.as_view(), name='criar_partida'),
    path('partidas/<slug:slug>/', PartidaView.as_view(), name='partida'),
    path('partidas/<slug:slug>/pagamentos/', PagamentosView.as_view(), name='pagamentos'),
    path('partidas/<slug:slug>/adicionar-convidado/novo', AdicionarConvidadoView.as_view(), name='adicionar_convidado'),
    path('partidas/<slug:slug>/adicionar-convidado/existente', AdicionarConvidadoExistenteView.as_view(), name='convidado_existente'),
    path('partidas/<slug:slug>/excluir/', PartidaDeleteView.as_view(), name='excluir_partida'),
    path('partidas/<slug:slug>/pagamento/', PagamentoView.as_view(), name='pagamento'),
    path('partidas/<slug:slug>/pagamento-convidado/<str:convidado_id>', PagamentoConvidadoView.as_view(), name='pagamento_convidado'),
    path('gerenciar-federados/', GerenciarFederadosView.as_view(), name='gerenciar_federados'),
    path('gerenciar-federados/<slug:slug>', GerenciarFederadoView.as_view(), name='gerenciar_federado'),
    path('patrocinadores/', PatrocinadoresView.as_view(), name='patrocinadores'),
]

