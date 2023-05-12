import routeros_api

##FUNCION DE VERIFICACIÓN DE CONEXIÓN AL MIKROTIK VIA API
# PARAMETROS
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero
def test_conexion(ip_host, user, pwd, port):
    try: # Estructura try para controlar el error si no se establece la conexión
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        status = "La conexión via api se ha realizado exitosamente."
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha logrado conectar via api, revisar la información ingresada por favor."
    return status
