import routeros_api

##FUNCION PARA REALIZAR CONFIGURACIONES ADICIONALES AL MIKROTIK
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero
def config_adicional(ip_host, user, pwd, port):
    try: # Estructura try para controlar el error si no se establece la conexión
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        system1 = api.get_resource("/system/clock")
        system1.set(time_zone_name="America/Guayaquil")
        system2 =  api.get_resource("/system/ntp/server")
        system2.set(enabled="yes")
        system3 = api.get_resource("/system/ntp/client")
        system3.add(address="3.ec.pool.ntp.org")
        system3.add(address="2.south-america.pool.ntp.org")
        system3.add(address="1.south-america.pool.ntp.org")
        dns = api.get_resource("/ip/dns")
        dns.set(servers="8.8.8.8,8.8.4.4")
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha logrado conectar via api, revisar la información ingresada por favor."
    return status
