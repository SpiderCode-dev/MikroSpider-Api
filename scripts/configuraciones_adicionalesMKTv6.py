import routeros_api

##FUNCION PARA REALIZAR CONFIGURACIONES ADICIONALES AL MIKROTIK v6
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero
def config_adicionalv6(ip_host, user, pwd, port):
    try: # Estructura try para controlar el error si no se establece la conexión
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        system1 = api.get_resource("/system/clock") # Configura la zona horaria
        system1.set(time_zone_name="America/Guayaquil")
        system2 = api.get_resource("/system/ntp/client") #Configura los servidores ntp y dns
        system2.set(enabled="yes", primary_ntp="190.15.128.72", server_dns_names="inocar.ntp.ec")
        dns = api.get_resource("/ip/dns")
        dns.set(servers="8.8.8.8,8.8.4.4")
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha realizado los cambios, verificar la conexión con el router via api por favor."
    return status
