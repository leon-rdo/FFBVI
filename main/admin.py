from django.contrib import admin
from main.models import *

class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 0
    readonly_fields = ['jogador']

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    ordering = ['-data']
    list_filter = ['data']
    list_display = ['__str__', 'sorteada']
    
    inlines = [PagamentoInline]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['nome_jogador']
    search_fields = ['nome_jogador']
    list_display = ['nome_jogador', 'tipo', 'posicao']
    list_filter = ['tipo']
    readonly_fields = ['idade', 'gols_marcados', 'pontos', 'date_joined', 'last_login']
    
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
    
admin.site.site_header = 'Administração da FFBVI'
admin.site.index_title = 'FFBVI'