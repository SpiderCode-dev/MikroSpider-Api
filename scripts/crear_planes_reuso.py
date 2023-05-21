import routeros_api

##FUNCION PARA CRAR PLANES SIMPLE QUEUE CON REUSO
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# nombre: nombre del plan a crear
# velocidad: velocidad en Mbps
# cantidad: numero de planes padre a crear
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero y de los planes
# La función devolvera una lista con el id del item creado en el address-list y el id del item creado en la cola
def crear_plan_reuso(ip_host, user, pwd, port, nombre, velocidad, cantidad):
    try: # Estructura try para controlar el error si no se establece la conexión
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        cola = api.get_resource("/queue/simple")
        lat = str(velocidad) + "M"
        mli = str(velocidad) + "M"
        # Se crea la cola simple
        for i in range(cantidad):
            cola.add(limit_at=lat + "/" + lat, max_limit=mli + "/" + mli, queue="pcq-upload-default/pcq-download-default",
                     name="PLAN_REUSO_"+ str(velocidad) + "_" + str(i+1) + "_MIKROSPIDER", comment=nombre)
        status = "Planes creados exitosamente."
        return status
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha podido crear los planes debido a un error de conexión."
        return status