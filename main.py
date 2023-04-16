import getpass
import lotw_request

# Solicitar los datos de autenticación y los parámetros de consulta al usuario
username = input("Ingrese su nombre de usuario de LoTW: ")
password = getpass.getpass("Ingrese su contraseña de LoTW: ")
callsign = input("Ingrese su indicativo de llamada: ")
banda = input("Ingrese la banda de frecuencia a consultar ('2m', '1.25m', '70cm' o '23cm'): ")
modo = input("Ingrese el modo de operación a consultar ('CW', 'DIGITAL', 'PHONE', 'IMAGE', 'MCW' o 'RTTY'): ")

# Realizar la consulta a LoTW
try:
    results = lotw_qso_report(username, password, callsign, banda, modo)
except Exception as e:
    print("Error al realizar la consulta: ", str(e))
    exit()

# Imprimir los resultados
if not results:
    print("No se encontraron resultados.")
else:
    for result in results:
        print("Gridsquare:", result.get('GRIDSQUARE'))
        print("Mi gridsquare:", result.get('MY_GRIDSQUARE'))
        print("--------------------------")
