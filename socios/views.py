"""
VISTAS DEL SISTEMA DE SOCIOS
==============================
CRUD completo: Alta, Baja, Modificación, Lectura
Control de roles: solo admins acceden, cada admin ve sus socios
"""

from django.shortcuts import render, get_object_or_404, redirect            # atajos para renderizar plantillas, obtener objetos o redirigir
from django.contrib.auth.decorators import login_required, user_passes_test  #decoradores para controlar acceso: login_required y user_passes_test con función personalizada
from django.contrib import messages
from django.db.models import Q, Sum, Count
from .models import Socio
from .forms import SocioForm

 
def es_admin(user):
    """Verifica que el usuario sea staff/admin."""
    return user.is_authenticated and user.is_staff


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────

@login_required    # Solo usuarios autenticados pueden acceder al dashboard
def dashboard(request):
    socios = Socio.objects.filter(admin=request.user)
    total = socios.count()
    activos = socios.filter(estado='activo').count()
    morosos = socios.filter(estado='moroso').count()
    vip = socios.filter(tipo='vip').count()

    # Ingresos mensuales estimados usando polimorfismo
    ingresos = sum(s.calcular_cuota() for s in socios.filter(estado='activo'))

    contexto = {    #diccionario creado para pasar datos a la plantilla del dashboard
        'total_socios': total,
        'socios_activos': activos,
        'socios_morosos': morosos,
        'socios_vip': vip,
        'ingresos_mensuales': ingresos,
        'socios_recientes': socios.order_by('-fecha_alta')[:5],
    }
    return render(request, 'socios/dashboard.html', contexto)   #mew devuelve al html del dashboard con el contexto para mostrar las estadísticas y lista de socios recientes


# ─────────────────────────────────────────────
# LECTURA: lista y detalle
# ─────────────────────────────────────────────

@login_required
def lista_socios(request):
    socios = Socio.objects.filter(admin=request.user)  #me vuelve a filtrar los socios para mostrar solo los del admin logueado

    # Filtros
    q = request.GET.get('q', '')          #filtro de búsqueda general que se obtiene de los parámetros GET, con valor por defecto '' si no se proporciona
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')

    if q:
        socios = socios.filter(
            Q(nombre__icontains=q) |  # búsqueda en nombre, apellido, email o DNI y el icontains hace que sea case-insensitive y busque coincidencias parciales
            Q(apellido__icontains=q) |
            Q(email__icontains=q) |
            Q(dni__icontains=q)
        )
    if tipo:
        socios = socios.filter(tipo=tipo)
    if estado:
        socios = socios.filter(estado=estado)

    contexto = {
        'socios': socios,
        'q': q,
        'tipo_sel': tipo,
        'estado_sel': estado,
        'total': socios.count(),
    }
    return render(request, 'socios/lista.html', contexto)


@login_required
def detalle_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk, admin=request.user)  # obtiene el socio por su clave primaria (pk) y verifica que pertenezca al admin logueado, si no lo encuentra devuelve un error 404
    objeto_poo = socio.como_objeto_poo()
    contexto = {
        'socio': socio,
        'cuota': socio.calcular_cuota(),
        'descripcion': objeto_poo.obtener_descripcion(),
        'habilitado': socio.esta_habilitado(),  #se implementa el método de negocio esta_habilitado() para mostrar si el socio puede acceder a los servicios o no, basado en su estado y fecha de alta
    }
    return render(request, 'socios/detalle.html', contexto)


# ─────────────────────────────────────────────
# ALTA: crear socio
# ─────────────────────────────────────────────

@login_required
def crear_socio(request):
    if request.method == 'POST':
        form = SocioForm(request.POST)
        if form.is_valid():
            socio = form.save(commit=False) #el método save(commit=False) se utiliza para crear una instancia del modelo Socio a partir de los datos del formulario sin guardarla inmediatamente en la base de datos, lo que permite asignar el admin antes de guardar
            socio.admin = request.user
            socio.save()
            messages.success(request, f"Socio '{socio.nombre_completo()}' creado correctamente.")
            return redirect('socios:lista') #utilizo el redirect para enviar al usuario a la lista de socios después de crear uno nuevo, en lugar de renderizar una plantilla directamente, lo que es una buena práctica para evitar problemas de reenvío de formularios
    else:
        form = SocioForm()

    return render(request, 'socios/formulario.html', {
        'form': form,
        'titulo': 'Nuevo socio',
        'accion': 'Crear',
    })


# ─────────────────────────────────────────────
# MODIFICACIÓN: editar socio
# ─────────────────────────────────────────────

@login_required
def editar_socio(request, pk):  #este es el método para editar un socio existente, recibe la pk del socio a editar, obtiene el objeto socio y verifica que pertenezca al admin logueado, luego maneja el formulario de edición similar al de creación pero con la instancia del socio para prellenar los datos
    socio = get_object_or_404(Socio, pk=pk, admin=request.user)

    if request.method == 'POST':
        form = SocioForm(request.POST, instance=socio)
        if form.is_valid():
            form.save()
            messages.success(request, f"Socio '{socio.nombre_completo()}' actualizado correctamente.")
            return redirect('socios:detalle', pk=pk)
    else:
        form = SocioForm(instance=socio)

    return render(request, 'socios/formulario.html', {
        'form': form,
        'socio': socio,
        'titulo': f'Editar — {socio.nombre_completo()}',
        'accion': 'Guardar cambios',
    })


# ─────────────────────────────────────────────
# BAJA: eliminar socio
# ─────────────────────────────────────────────

@login_required
def eliminar_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk, admin=request.user)

    if request.method == 'POST':
        nombre = socio.nombre_completo()
        socio.delete()
        messages.success(request, f"Socio '{nombre}' eliminado correctamente.")
        return redirect('socios:lista')

    return render(request, 'socios/confirmar_baja.html', {'socio': socio})


# ─────────────────────────────────────────────
# MÉTODO SET desde POO: cambiar estado vía objeto
# ─────────────────────────────────────────────

@login_required
def cambiar_estado_socio(request, pk):
    """
    Demuestra el uso del setter cambiar_estado() del objeto POO
    antes de persistir el cambio en la base de datos.
    """
    socio = get_object_or_404(Socio, pk=pk, admin=request.user)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        try:
            obj = socio.como_objeto_poo()
            obj.cambiar_estado(nuevo_estado)        # setter con @registrar_accion
            socio.estado = obj.estado               # sincronizar con BD
            socio.save(update_fields=['estado', 'fecha_modificacion'])
            messages.success(request, f"Estado actualizado a '{nuevo_estado}'.")
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('socios:detalle', pk=pk)
