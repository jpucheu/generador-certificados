import requests

def lotw_qso_report(username, password, callsign, banda, modo):
    """
    Realiza una consulta a la API de ARRL Logbook of the World (LoTW) para obtener un reporte de contactos.

    Args:
        username (str): Nombre de usuario de LoTW.
        password (str): Contraseña de LoTW.
        callsign (str): Indicativo de llamada del usuario.
        banda (str): Banda de frecuencia (en MHz) de los contactos a consultar. Debe ser '2m', '1.25m', '70cm', o '23cm'.
        modo (str): Modo de operación de los contactos a consultar. Debe ser uno de los valores permitidos por la API de LoTW.

    Returns:
        dict: Diccionario de datos con la respuesta de la consulta.
    """
    allowed_modes = ['CW', 'DIGITAL', 'PHONE', 'IMAGE', 'MCW', 'RTTY']
    
    # Validación de los argumentos
    if not all([username, password, callsign]) or not str(username).isalnum() or not str(password).isalnum() or not str(callsign).isalnum():
        raise ValueError("El nombre de usuario, contraseña y callsign deben ser cadenas no vacías y alfanuméricas.")
    if banda not in ['2m', '1.25m', '70cm', '23cm']:
        raise ValueError("El valor de qso_band debe ser '2m', '1.25m', '70cm' o '23cm'.")
    if modo not in allowed_modes:
        raise ValueError(f"El modo debe ser uno de los siguientes valores: {', '.join(allowed_modes)}")
    
    # Parámetros para la consulta a la API de LoTW
    params = {
        'USERNAME': username,
        'PASSWORD': password,
        'qso_owncall': callsign,
        'qso_qsl': 'yes',
        'qso_mode': modo,
        'qso_band': banda,
        'qso_qsldetail': 'yes',
        'qso_mydetail': 'yes'
    }
    
    # Realizar la consulta y obtener la respuesta
    try:
        response = requests.get('https://lotw.arrl.org/lotwuser/lotwreport.adi', params=params, timeout=10)
        response.raise_for_status()
    except (requests.exceptions.Timeout, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(f"Se produjo un error al intentar realizar la consulta a la API de LoTW: {e}")
        return {}
    
    # Procesar la respuesta
    result = {}
    for line in response.iter_lines():
        line = line.decode('utf-8')
        if line.startswith('<eoh>'):
            fields = line.strip().split(':')
            if len(fields) == 2 and fields[0] in ['GRIDSQUARE', 'MY_GRIDSQUARE']:
                result[fields[0]] = fields[1]
        elif line.startswith('<eor>'):
            yield result
            result = {}
        else:
            fields = line.strip().split(':')
            if len(fields) == 2 and fields[0] in ['GRIDSQUARE', 'MY_GRIDSQUARE']:
                result[fields[0]] = fields[1]
    
    return result
