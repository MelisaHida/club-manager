from abc import ABC, abstractmethod # Para definir la clase base abstracta Persona
from datetime import datetime
from django.db import models  # NECESARIO PARA DEFINIR MODELOS DE DJANGO, TABLAS EN LA BASE DE DATOS, ETC.
from django.contrib.auth.models import User  #Almacena los superusuarios que pueden administrar los socios, y se relaciona con cada socio para saber quién lo creó o administra.
import functools # sirve para crear decoradores que registren acciones importantes, como cambios de estado, para facilitar el seguimiento y depuración.

def registrar_accion(func):  
    @functools.wraps(func)
    def wrapper(*args, **kwargs):   # Este decorador se puede usar para registrar acciones importantes, como cambios de estado, para facilitar el seguimiento y depuración.
        print(f"[REGISTRO] {func.__name__}")
        resultado = func(*args, **kwargs)
        return resultado
    return wrapper  

class Domicilio:
    def __init__(self, calle="", ciudad="", provincia=""):
        self.__calle = calle  # Atributo privado para almacenar la calle, con un getter y setter para control de acceso.
        self.__ciudad = ciudad  # Atributo privado para almacenar la ciudad, con un getter para acceso controlado.
        self.__provincia = provincia  # Atributo privado para almacenar la provincia, con un getter para acceso controlado.
    @property
    def calle(self): return self.__calle
    @property                             #los property permiten acceder a los atributos privados de forma controlada, evitando acceso directo y permitiendo validaciones o transformaciones si es necesario.
    def ciudad(self): return self.__ciudad
    @property
    def provincia(self): return self.__provincia
    @calle.setter                          # El setter para calle permite asignar un valor a la calle, con validación para evitar valores vacíos o con espacios innecesarios.
    def calle(self, v): self.__calle = v.strip()
    def direccion_completa(self):             # Este método devuelve la dirección completa en formato "calle, ciudad, provincia", omitiendo partes vacías para evitar comas innecesarias.
        return ", ".join(p for p in [self.__calle, self.__ciudad, self.__provincia] if p)
    def __str__(self): return self.direccion_completa() or "Sin domicilio"  # El método __str__ devuelve la dirección completa o "Sin domicilio" si no se ha proporcionado ninguna información de dirección.

class Persona(ABC):   # La clase Persona es una clase base abstracta que define los atributos y métodos comunes para todas las personas, como nombre, apellido, email y dni, así como métodos abstractos para calcular la cuota y obtener una descripción del tipo de socio.
    def __init__(self, nombre, apellido, email, dni): 
        self._nombre = nombre  # Atributo protegido para almacenar el nombre, con un getter y setter para control de acceso.
        self._apellido = apellido
        self._email = email
        self._dni = dni
    @property    # Los property permiten acceder a los atributos protegidos de forma controlada, evitando acceso directo y permitiendo validaciones o transformaciones si es necesario.
    def nombre(self): return self._nombre
    @property
    def apellido(self): return self._apellido
    @property
    def email(self): return self._email
    @property
    def dni(self): return self._dni
    @nombre.setter
    def nombre(self, v):
        if not v.strip(): raise ValueError("Nombre vacío")  # El setter para nombre valida que el nombre no esté vacío o solo contenga espacios, y asigna el valor limpio al atributo protegido _nombre.
        self._nombre = v.strip()
    def nombre_completo(self): return f"{self._nombre} {self._apellido}"  # El método nombre_completo devuelve el nombre completo de la persona en formato "Nombre Apellido".
    @abstractmethod
    def calcular_cuota(self): pass  # El método calcular_cuota es un método abstracto que debe ser implementado por las clases derivadas para calcular la cuota correspondiente según el tipo de socio.
    @abstractmethod
    def obtener_descripcion(self): pass  # El método obtener_descripcion es un método abstracto que debe ser implementado por las clases derivadas para proporcionar una descripción del tipo de socio, como "Socio Regular: acceso básico al club." o "Socio VIP: acceso total con beneficios premium.".
    def __str__(self): return self.nombre_completo()

class SocioBase(Persona):              # La clase SocioBase es una clase base concreta que hereda de Persona y agrega atributos y métodos comunes para todos los tipos de socios, como teléfono, estado, fecha de modificación y domicilio, así como métodos para cambiar el estado y verificar si el socio está habilitado.
    ESTADOS_VALIDOS = ("activo", "inactivo", "moroso") # La tupla ESTADOS_VALIDOS define los estados válidos que un socio puede tener, como "activo", "inactivo" o "moroso", y se utiliza para validar los cambios de estado en el método cambiar_estado.
    def __init__(self, nombre, apellido, email, dni, telefono="", estado="activo", domicilio=None):
        super().__init__(nombre, apellido, email, dni)
        self.__telefono = telefono
        self.__estado = estado
        self.__fecha_modificacion = datetime.now()
        self.domicilio = domicilio or Domicilio()
    @property   # Los property permiten acceder a los atributos privados de forma controlada, evitando acceso directo y permitiendo validaciones o transformaciones si es necesario.
    def telefono(self): return self.__telefono
    @property
    def estado(self): return self.__estado
    @telefono.setter
    def telefono(self, v):   # El setter para teléfono valida que el número no esté vacío o solo contenga espacios, y asigna el valor limpio al atributo privado __telefono, además de actualizar la fecha de modificación para reflejar el cambio.
        self.__telefono = v.strip()
        self.__fecha_modificacion = datetime.now()
    @registrar_accion
    def cambiar_estado(self, nuevo):
        if nuevo not in self.ESTADOS_VALIDOS:  # El método cambiar_estado valida que el nuevo estado sea uno de los estados válidos definidos en ESTADOS_VALIDOS, y si es válido, actualiza el estado del socio y la fecha de modificación para reflejar el cambio.
            raise ValueError(f"Estado inválido: {nuevo}")
        self.__estado = nuevo
        self.__fecha_modificacion = datetime.now()
    def esta_habilitado(self): return self.__estado == "activo" # El método esta_habilitado verifica si el estado del socio es "activo", lo que indica que el socio está habilitado para acceder a los servicios del club, y devuelve True si el estado es "activo" o False en caso contrario.

class SocioRegularPOO(SocioBase): # La clase SocioRegularPOO hereda de SocioBase y representa a los socios regulares, con una cuota base fija y proporciona una descripción específica para este tipo de socio.
    CUOTA_BASE = 5000.0
    def calcular_cuota(self): return self.CUOTA_BASE
    def obtener_descripcion(self): return "Socio Regular: acceso basico al club."

class SocioVIPPOO(SocioBase):   # La clase SocioVIPPOO hereda de SocioBase y representa a los socios VIP, con una cuota base más alta que la de los socios regulares debido a los beneficios premium que ofrecen, y proporciona una descripción específica para este tipo de socio.
    CUOTA_BASE = 5000.0
    RECARGO_VIP = 1.0
    def calcular_cuota(self): return self.CUOTA_BASE * (1 + self.RECARGO_VIP)
    def obtener_descripcion(self): return "Socio VIP: acceso total con beneficios premium."

class SocioFamiliarPOO(SocioBase): 
    CUOTA_BASE = 5000.0
    COSTO_POR_FAMILIAR = 1500.0
    def __init__(self, cantidad_familiares=1, **kwargs):
        super().__init__(**kwargs)
        self.__cantidad_familiares = max(1, cantidad_familiares)
    @property
    def cantidad_familiares(self): return self.__cantidad_familiares
    @cantidad_familiares.setter
    def cantidad_familiares(self, v):
        if v < 1: raise ValueError("Minimo 1 familiar")
        self.__cantidad_familiares = v
    def calcular_cuota(self): return self.CUOTA_BASE + self.__cantidad_familiares * self.COSTO_POR_FAMILIAR
    def obtener_descripcion(self): return f"Socio Familiar: titular + {self.__cantidad_familiares} familiar(es)."

class FabricaSocio:  # La clase FabricaSocio es una fábrica que se encarga de crear instancias de los diferentes tipos de socios (Regular, VIP, Familiar) a partir de un tipo especificado y los datos necesarios para cada tipo, utilizando un mapa interno para asociar cada tipo con su clase correspondiente.
    _mapa = {"regular": SocioRegularPOO, "vip": SocioVIPPOO, "familiar": SocioFamiliarPOO}
    @staticmethod
    def crear(tipo, **kwargs):  #
        clase = FabricaSocio._mapa.get(tipo) #Buscamos crear la clase correspondiente al tipo solicitado en el mapa interno, y si no se encuentra, se lanza una excepción indicando que el tipo es desconocido.
        if not clase: raise ValueError(f"Tipo desconocido: {tipo}")
        return clase(**kwargs)
    @classmethod
    def tipos_disponibles(cls): return list(cls._mapa.keys()) # El método tipos_disponibles devuelve una lista de los tipos de socios disponibles en la fábrica, lo que permite conocer qué tipos se pueden crear utilizando la fábrica.

class Socio(models.Model):  # La clase Socio es un modelo de Django que representa a los socios en la base de datos, con campos para almacenar información como el nombre, apellido, email, teléfono, tipo de socio, estado, domicilio y fechas de alta y modificación, además de métodos para convertir la instancia a un objeto POO y calcular la cuota correspondiente según el tipo de socio.
    TIPOS = [("regular","Regular"),("vip","VIP"),("familiar","Familiar")]
    ESTADOS = [("activo","Activo"),("inactivo","Inactivo"),("moroso","Moroso")]
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="socios")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    dni = models.CharField(max_length=20)
    tipo = models.CharField(max_length=10, choices=TIPOS, default="regular")
    estado = models.CharField(max_length=10, choices=ESTADOS, default="activo")
    cantidad_familiares = models.PositiveIntegerField(default=0)
    calle = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Socio"
        verbose_name_plural = "Socios"
        ordering = ["apellido", "nombre"]
    def __str__(self): return f"{self.nombre} {self.apellido}"
    def nombre_completo(self): return f"{self.nombre} {self.apellido}"
    def como_objeto_poo(self):                 # El método como_objeto_poo convierte la instancia del modelo Socio en un objeto de la clase correspondiente según el tipo de socio, creando un objeto Domicilio con los datos de dirección y utilizando la fábrica para crear el objeto POO con los datos necesarios.
        d = Domicilio(self.calle, self.ciudad, self.provincia)
        kw = dict(nombre=self.nombre, apellido=self.apellido, email=self.email,
                  dni=self.dni, telefono=self.telefono, estado=self.estado, domicilio=d)
        if self.tipo == "familiar":
            kw["cantidad_familiares"] = self.cantidad_familiares
        return FabricaSocio.crear(self.tipo, **kw)
    def calcular_cuota(self): return self.como_objeto_poo().calcular_cuota()
    def esta_habilitado(self): return self.estado == "activo"
