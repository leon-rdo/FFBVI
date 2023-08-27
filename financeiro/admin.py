from django.contrib import admin
from .models import Saida

@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    ordering = ['-data']
    list_display = ['_str_', 'valor', 'data']
    readonly_fields = ['data']
