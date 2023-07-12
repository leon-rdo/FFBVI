from django.contrib import admin
from main.models import *

class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 0

class PartidaAdmin(admin.ModelAdmin):
    inlines = [PagamentoInline]

class UserAdmin(admin.ModelAdmin):
    list_filter = ('tipo',)

admin.site.register(User, UserAdmin)
admin.site.register(Partida, PartidaAdmin)
admin.site.register(Patrocinador)
admin.site.register(Configuracao)