# Club Manager — Sistema de Administración de Socios
**Proyecto final — Programación Avanzada | Python + Django + SQLite/PostgreSQL**

---

## Conceptos de POO aplicados

| Concepto | Dónde se aplica |
|---|---|
| Abstracción | Clase `Persona` (ABC) — no instanciable directamente |
| Encapsulamiento | Atributos `__privados` con `@property` getters/setters |
| Herencia | `Persona → SocioBase → SocioRegular/VIP/Familiar` |
| Polimorfismo | `calcular_cuota()` en cada subclase |
| Composición | `Socio` tiene un `Domicilio` |
| Agregación | `Socio` referencia a un `User` (admin) |
| Metaclases | `ValidadorMeta` valida que las subclases definan `CUOTA_BASE` |
| Decoradores | `@registrar_accion`, `@validar_no_vacio` |
| Getters/Setters | `@property` y `@atributo.setter` en todas las clases |
| Atributos privados | `__telefono`, `__estado`, `__cantidad_familiares` |
| Atributos públicos | `CUOTA_BASE`, `ESTADOS_VALIDOS` |
| Roles | Admin (is_staff) y SuperAdmin (is_superuser) |
| CRUD completo | Alta, Baja, Modificación y Lectura de socios |

---

## Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU-USUARIO/club-manager.git
cd club-manager

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear base de datos
python manage.py migrate

# 5. Crear superusuario (opcional)
python manage.py createsuperuser

# 6. Correr el servidor
python manage.py runserver
```

Abrir en el navegador: http://127.0.0.1:8000

---

## Deploy en Railway (gratis)

1. Subir el proyecto a GitHub
2. Ir a [railway.app](https://railway.app) → **New Project → Deploy from GitHub**
3. Seleccionar el repositorio
4. Railway detecta el `Procfile` y despliega automáticamente
5. En Variables de entorno agregar:
   - `SECRET_KEY` → cualquier string largo y aleatorio
   - `DEBUG` → `False`

---

## Estructura del proyecto

```
club_manager/          ← configuración Django
socios/
  models.py            ← toda la jerarquía POO + modelos Django
  views.py             ← CRUD (Alta/Baja/Modificación/Lectura)
  forms.py             ← formularios con validación
  urls.py              ← rutas de socios
usuarios/
  views.py             ← login, logout, registro, perfil
  urls.py              ← rutas de autenticación
templates/
  base.html            ← diseño base con navbar
  socios/              ← todas las vistas de socios
  usuarios/            ← login, registro, perfil
```

---

## Diagrama UML
Ver archivo `UML.md` en la raíz del proyecto.
