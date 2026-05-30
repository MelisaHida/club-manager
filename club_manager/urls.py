from django.contrib import admin
from django.urls import path, include
from socios import views as socio_views

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('',            socio_views.dashboard,  name='dashboard'),
    path('socios/',     include('socios.urls')),
    path('usuarios/',   include('usuarios.urls')),
]
