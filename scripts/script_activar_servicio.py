import routeros_api

##FUNCION PARA ACTIVAR EL SERVICIO DE CLIENTES
# PARAMETROS
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# nombre: lista de nombres de los clientes a cortar
# ids_activar: lista de ids a eliminar de la address-list de cortes
# ids_proxy: lista de ids a eliminar en el web proxy
# NOTA: El orden de los datos entre los parámetros de entrada nombre e ids_activar deben ser simétricos.
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero.
def activar_servicio(ip_host, user, pwd, port, nombre, ids_activar, ids_proxy):
    try:
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        addresslist = api.get_resource("/ip/firewall/address-list")
        proxy = api.get_resource("ip/proxy/access")
        i = 0
        datos_actualizar = []
        for Id in ids_activar:
            info = addresslist.get(comment=nombre[i]) # Obtiene toda la informacion del item creado
            item = info[0] # Se guarda la información esencial
            IDfr = item['id']  # Obtenemos el id del item creado en el address-list al momento que se le hizo el corte
            info2 = proxy.get(comment=nombre[i] + "-Moroso")  # Obtiene la informacion del item proxy creado
            item2 = info2[0]
            IDfr2 = item2['id']
            if Id == IDfr and ids_proxy[i] == IDfr2: # Se compara el id obtenido desde el router con el ingresado desde la base de datos
                addresslist.remove(id=Id) # Si es el mismo, se realiza la activación
                proxy.remove(id=ids_proxy[i])
            elif Id != IDfr and ids_proxy[i] == IDfr2:
                addresslist.remove(id=IDfr) # Caso contrario realiza realiza la activación igualmente pero se controla si hay un error
                proxy.remove(id=ids_proxy[i])
                dic_id_actual = {IDfr: nombre[i], "id_proxy": ids_proxy[i]} # Se relaciona el id correcto con el nombre y se crea un diccionario
                datos_actualizar.append(dic_id_actual) # Se crea una lista con un diccionario por cliente a actualizar en la base de datos.
            elif Id == IDfr and ids_proxy[i] != IDfr2:
                addresslist.remove(id=Id)
                proxy.remove(id=IDfr2)
                dic_id_actual = {Id: nombre[i], "id_proxy": IDfr2}  # Se relaciona el id correcto con el nombre y se crea un diccionario
                datos_actualizar.append(dic_id_actual)  # Se crea una lista con un diccionario por cliente a actualizar en la base de datos.
            i = i + 1  # Acumulador que sirve como indexación en la lista de nombres
        status = "Cliente activado exitosamente"
        if len(datos_actualizar) != 0:
            return status, datos_actualizar # Si existe un elemento en la lista de datos a actualizar, la función retorna la lista
        else:
            return status
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha podido realizar el o los cortes debido a un error de conexión."
        return status
