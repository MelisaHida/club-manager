from abc import ABC, abstractmethod
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import functools

def registrar_accion(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[REGISTRO] {func.__name__}")
        resultado = func(*args, **kwargs)
        return resultado
    return wrapper

class Domicilio:
    def __init__(self, calle="", ciudad="", provincia=""):
        self.__calle = calle
        self.__ciudad = ciudad
        self.__provincia = provincia
    @property
    def calle(self): return self.__calle
    @property
    def ciudad(self): return self.__ciudad
    @property
    def provincia(self): return self.__provincia
    @calle.setter
    def calle(self, v): self.__calle = v.strip()
    def direccion_completa(self):
        return ", ".join(p for p in [self.__calle, self.__ciudad, self.__provincia] if p)
    def __str__(self): return self.direccion_completa() or "Sin domicilio"

class Persona(ABC):
    def __init__(self, nombre, apellido, email, dni):
        self._nombre = nombre
        self._apellido = apellido
        self._email = email
        self._dni = dni
    @property
    def nombre(self): return self._nombre
    @property
    def apellido(self): return self._apellido
    @property
    def email(self): return self._email
    @property
    def dni(self): return self._dni
    @nombre.setter
    def nombre(self, v):
        if not v.strip(): raise ValueError("Nombre vacío")
        self._nombre = v.strip()
    def nombre_completo(self): return f"{self._nombre} {self._apellido}"
    @abstractmethod
    def calcular_cuota(self): pass
    @abstractmethod
    def obtener_descripcion(self): pass
    def __str__(self): return self.nombre_completo()

class SocioBase(Persona):
    ESTADOS_VALIDOS = ("activo", "inactivo", "moroso")
    def __init__(self, nombre, apellido, email, dni, telefono="", estado="activo", domicilio=None):
        super().__init__(nombre, apellido, email, dni)
        self.__telefono = telefono
        self.__estado = estado
        self.__fecha_modificacion = datetime.now()
        self.domicilio = domicilio or Domicilio()
    @property
    def telefono(self): return self.__telefono
    @property
    def estado(self): return self.__estado
    @telefono.setter
    def telefono(self, v):
        self.__telefono = v.strip()
        self.__fecha_modificacion = datetime.now()
    @registrar_accion
    def cambiar_estado(self, nuevo):
        if nuevo not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {nuevo}")
        self.__estado = nuevo
        self.__fecha_modificacion = datetime.now()
    def esta_habilitado(self): return self.__estado == "activo"

class SocioRegularPOO(SocioBase):
    CUOTA_BASE = 30000.0
    def calcular_cuota(self): return self.CUOTA_BASE
    def obtener_descripcion(self): return "Socio Regular: acceso basico al club."

class SocioVIPPOO(SocioBase):
    CUOTA_BASE = 45000.0
    RECARGO_VIP = 0.5
    def calcular_cuota(self): return self.CUOTA_BASE * (1 + self.RECARGO_VIP)
    def obtener_descripcion(self): return "Socio VIP: acceso total con beneficios premium."

class SocioFamiliarPOO(SocioBase):
    CUOTA_BASE = 30000.0
    COSTO_POR_FAMILIAR = 15000.0
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

class FabricaSocio:
    _mapa = {"regular": SocioRegularPOO, "vip": SocioVIPPOO, "familiar": SocioFamiliarPOO}
    @staticmethod
    def crear(tipo, **kwargs):
        clase = FabricaSocio._mapa.get(tipo)
        if not clase: raise ValueError(f"Tipo desconocido: {tipo}")
        return clase(**kwargs)
    @classmethod
    def tipos_disponibles(cls): return list(cls._mapa.keys())

class Socio(models.Model):
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
    def como_objeto_poo(self):
        d = Domicilio(self.calle, self.ciudad, self.provincia)
        kw = dict(nombre=self.nombre, apellido=self.apellido, email=self.email,
                  dni=self.dni, telefono=self.telefono, estado=self.estado, domicilio=d)
        if self.tipo == "familiar":
            kw["cantidad_familiares"] = self.cantidad_familiares
        return FabricaSocio.crear(self.tipo, **kw)
    def calcular_cuota(self): return self.como_objeto_poo().calcular_cuota()
    def esta_habilitado(self): return self.estado == "activo"
