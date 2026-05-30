from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', '/socios/'))
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('usuarios:login')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Los nuevos usuarios registrados son staff (admin del club)
            user.is_staff = True
            user.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta fue creada.')
            return redirect('/socios/')
        else:
            messages.error(request, 'Por favor corregí los errores del formulario.')
    else:
        form = UserCreationForm()

    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def perfil_view(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})
