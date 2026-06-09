import os  # Para manejar variables de entorno  como SECRET_KEY y DEBUG de manera segura
from pathlib import Path  # Para manejar rutas de archivos de manera más limpia

BASE_DIR = Path(__file__).resolve().parent.parent                  #Calcula la ruta base del proyecto  que es la carpeta raíz del proyecto Django

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-cambia-esto-en-produccion-2024')    # Obtiene la clave secreta de las variables de entorno, o usa un valor por defecto inseguro para desarrollo. En producción, siempre se debe establecer SECRET_KEY en las variables de entorno y no usar el valor por defecto.

DEBUG = os.environ.get('DEBUG', 'True') == 'True'  #Determina el entorno de ejecucion en desarrollo 

ALLOWED_HOSTS = ['*']   # Permite todas las hostnames. En producción, se recomienda especificar los dominios permitidos para mejorar la seguridad.

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') #Sirve como mecanismo de seguridad para proteger contra ataques CSRF   Esta configuración especifica una lista de orígenes confiables desde los cuales se aceptarán solicitudes POST.

INSTALLED_APPS = [     # Lista de aplicaciones instaladas en el proyecto Django. Incluye las aplicaciones predeterminadas de Django y las aplicaciones personalizadas 'socios' y 'usuarios'.
    'django.contrib.admin', 
    'django.contrib.auth',
    'django.contrib.contenttypes', # Permite el uso de modelos genéricos y relaciones entre modelos.
    'django.contrib.sessions', # Permite el uso de sesiones para almacenar información específica del usuario entre solicitudes.
    'django.contrib.messages', 
    'django.contrib.staticfiles', 
    'socios',
    'usuarios',
]

MIDDLEWARE = [      #Sirve para procesar las solicitudes y respuestas HTTP. Cada middleware realiza una función específica, como manejar la seguridad, las sesiones, la autenticación, etc.
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'club_manager.urls'   #Especifica el módulo de URL principal del proyecto, que es donde se definen las rutas URL para la aplicación Django. En este caso, se apunta a 'club_manager.urls'

TEMPLATES = [   #Configura el sistema de plantillas de Django. Define cómo se deben cargar y procesar las plantillas HTML. En este caso, se utiliza el backend de plantillas de Django, se especifica un directorio para las plantillas personalizadas y se habilita la búsqueda de plantillas dentro de las aplicaciones instaladas.
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Especifica un directorio adicional para buscar plantillas personalizadas. En este caso, se busca en la carpeta 'templates' dentro del directorio base del proyecto.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'club_manager.wsgi.application' # conecta a django con servidores web compatibles con wsgi.

# Base de datos: SQLite por defecto, PostgreSQL si DATABASE_URL está definida
DATABASE_URL = os.environ.get('DATABASE_URL', '')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}# 
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [     # Configura validadores de contraseña para mejorar la seguridad. Estos validadores verifican que las contraseñas no sean demasiado similares a los atributos del usuario, tengan una longitud mínima, no sean contraseñas comunes y no sean completamente numéricas.
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'   # Define la URL base para servir archivos estáticos (CSS, JavaScript, imágenes, etc.). En este caso, se establece en '/static/'.
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'    # Especifica el tipo de campo de clave primaria predeterminado para los modelos de Django. En este caso, se establece en 'BigAutoField', que es un campo de clave primaria que utiliza un entero de 64 bits.

LOGIN_URL = '/usuarios/login/'   # Especifica la URL a la que se redirigirá a los usuarios no autenticados cuando intenten acceder a una vista protegida por el decorador @login_required. En este caso, se establece en '/usuarios/login/'.
LOGIN_REDIRECT_URL = '/socios/'
LOGOUT_REDIRECT_URL = '/usuarios/login/'
