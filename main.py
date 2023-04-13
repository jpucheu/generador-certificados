#!/usr/bin/env python3
import cgi
import html

# Obtener los argumentos de la solicitud CGI
arguments = cgi.FieldStorage()

# Obtener los valores de los argumentos y sanitizarlos
arg1 = html.escape(arguments.getvalue('arg1', ''))
arg2 = html.escape(arguments.getvalue('arg2', ''))
arg3 = html.escape(arguments.getvalue('arg3', ''))

# Validar que los argumentos sean alfanuméricos
if not arg1.isalnum() or not arg2.isalnum() or not arg3.isalnum():
    print("Content-type: text/html\n\n")
    print("Error: Los argumentos deben ser alfanuméricos")
else:
    # Crear el string de respuesta
    response_string = "Los argumentos recibidos fueron: {}, {}, {}".format(arg1, arg2, arg3)

    # Imprimir la cabecera de la respuesta HTTP
    print("Content-type: text/html\n\n")

    # Imprimir el string de respuesta
    print(response_string)