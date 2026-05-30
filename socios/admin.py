from django.contrib import admin
from .models import Socio


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'email', 'tipo', 'estado', 'fecha_alta']
    list_filter = ['tipo', 'estado']
    search_fields = ['nombre', 'apellido', 'email', 'dni']
    readonly_fields = ['fecha_alta', 'fecha_modificacion']
