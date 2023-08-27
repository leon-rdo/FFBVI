from django.contrib import admin
from .models import Saida

@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    ordering = ['-data']
    list_display = ['__str__', 'valor', 'data']
    readonly_fields = ['data']
