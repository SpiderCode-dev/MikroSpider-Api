import routeros_api

##FUNCION PARA CORTAR EL SERVICIO DE LOS CLIENTES
# PARAMETROS
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# nombre: lista de nombre de los clientes a cortar
# ips_cortar: lista de ips a agregar a la address-list de cortes
# interfaz: interfaz del mikrotik por el que tiene salida a internet o WAN (puede ser una interfaz o varias interfaces a modo de lista)
# NOTA: El orden de los datos entre los parámetros de entrada nombre e  ips_cortar deben ser simétricos.
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero
def cortes_servicio(ip_host, user, pwd, port, nombre, ips_cortar):
    try:
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        addresslist = api.get_resource("/ip/firewall/address-list")
        i = 0
        for ip in ips_cortar:
            addresslist.add(address=ip, comment=nombre[i], list="ips_sin_servicio")
            a = a + 1 # Acumulador que sirve como indexación en la lista de nombres
        status = "Corte de servicio realizado exitosamente"
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha podido realizar el o los cortes debido a un error de conexión."
    return  status
