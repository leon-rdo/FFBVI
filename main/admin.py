from django.contrib import admin
from main.models import *


admin.site.site_header = 'Administração da FFBVI'
admin.site.index_title = 'FFBVI'


@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    list_filter = ['partida']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['nome_jogador']
    search_fields = ['nome_jogador']
    list_display = ['nome_jogador', 'tipo', 'posicao']
    list_filter = ['tipo']
    readonly_fields = ['idade', 'gols_marcados', 'pontos', 'date_joined', 'last_login']


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['data', 'jogador', 'partida', 'confirmado']
    ordering = ['-data']
    readonly_fields = ['data']

    def confirmar_pagamento(self, request, queryset):
        queryset.update(confirmado=True)
        self.message_user(request, f'{queryset.count()} pagamentos confirmados com sucesso.')

    confirmar_pagamento.short_description = "Confirmar os pagamentos selecionados"

    actions = [confirmar_pagamento]


class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 0
    readonly_fields = ['jogador', 'data']
    

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    ordering = ['-data']
    list_filter = ['data', 'anulada']
    list_display = ['__str__', 'sorteada', 'anulada']
    
    inlines = [PagamentoInline]  
     

@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
    ordering = ['nome']
    list_display = ['nome', 'link']


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'texto']


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ['email_diretor', 'telefone_diretor', 'chave_pix', 'alerta_mensagem']