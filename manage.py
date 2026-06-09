#!/usr/bin/env python
import os  #Importo los modulos necesarios para ejecutar el proyecto, en este caso os y sys
import sys  #Sys es necesario para manejar los argumentos de la línea de comandos como por ejemplo "runserver" o "migrate" para correr el servidor o crear las tablas en la base de datos respectivamente.

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'club_manager.settings')  # le indicamos a django que el archivo de config se encuentra en la carpeta club_manager y se llama settings.py
    try:
        from django.core.management import execute_from_command_line  # Importamos la función execute_from_command_line que se encarga de ejecutar los comandos de la línea  
    except ImportError as exc:                                        # de comandos de Django, como "runserver" o "migrate". Si no se puede importar, se lanza una excepción.

        raise ImportError("No se pudo importar Django.") from exc      #Si no se puede importar Django, se lanza una excepción con un mensaje de error.

    execute_from_command_line(sys.argv)                              #Llamamos a la función execute_from_command_line con los argumentos de la línea de comandos, lo que permite ejecutar los comandos de Django.

if __name__ == '__main__':  
    main()
