from django.urls import path
from . import views

app_name = 'socios'

urlpatterns = [
    path('',                        views.lista_socios,        name='lista'),
    path('nuevo/',                  views.crear_socio,         name='crear'),
    path('<int:pk>/',               views.detalle_socio,       name='detalle'),
    path('<int:pk>/editar/',        views.editar_socio,        name='editar'),
    path('<int:pk>/eliminar/',      views.eliminar_socio,      name='eliminar'),
    path('<int:pk>/estado/',        views.cambiar_estado_socio,name='cambiar_estado'),
]
