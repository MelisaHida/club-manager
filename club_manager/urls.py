from django.contrib import admin   #Importo el módulo admin para poder usar la interfaz de administración de Django
from django.urls import path, include  #Importo las funciones path e include para definir las rutas de URL de la aplicación
from socios import views as socio_views  #Importo las vistas del módulo socios y las renombro como socio_views para evitar conflictos de nombres con otras vistas

urlpatterns = [                                    # Defino la lista de rutas de URL para la aplicación
    path('admin/',      admin.site.urls),
    path('',            socio_views.dashboard,  name='dashboard'),  # La ruta raíz ('') se asigna a la vista dashboard del módulo socios, y se le da el nombre 'dashboard' para poder referenciarla fácilmente en otras partes de la aplicación
    path('socios/',     include('socios.urls')),
    path('usuarios/',   include('usuarios.urls')),     
]
