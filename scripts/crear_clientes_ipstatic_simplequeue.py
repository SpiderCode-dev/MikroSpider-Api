import routeros_api

##FUNCION PARA REALIZAR CONFIGURACIONES ADICIONALES AL MIKROTIK
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# nombres = Lista del o los clientes a añadir
# ips = lista de ips de cada cliente (la información debe ser simétrica en cuanto al orden de en los que se ubican los nombreS)
# plan = velocidad del plan del cliente (Por ejemplo: 45M, 65M etc...)
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero
# La función devolvera una lista con el id del item creado en el address-list y el id del item creado en la cola
def crearclientes_ipstatic_simplequeue(ip_host, user, pwd, port, nombres, ips, plan):
    try: # Estructura try para controlar el error si no se establece la conexión
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        address_list = api.get_resource("/ip/firewall/address-list")
        queuesimple = api.get_resource("/queue/simple")
        i = 0
        for ip in ips:
            address_list.add(address=ip, comment=nombres[i], list="ips_autorizadas_mikrospider")
            queuesimple.add(burst_limit=bl)
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha logrado conectar via api, revisar la información ingresada por favor."