import routeros_api

##FUNCION PARA REALIZAR ACTUALIZACIONES DE INFORMACION EN CLIENTES CREADOS CON IP ESTÁTICA SIN AMARRE Y COLA SIMPLE
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# nombres = Lista del o los clientes a añadir
# ips = lista de ips de cada cliente (la información debe ser simétrica en cuanto al orden de en los que se ubican los nombreS)
# plan = lista de velocidades del plan del cliente (Por ejemplo: 45, 65 etc...) en formato entero
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero y de los planes
# La función devolvera una lista con el id del item creado en el address-list y el id del item creado en la cola
def actualizar_info_ipstatic_queuesimple(ip_host, user, pwd, port, nombres, ips, plan):
    try: # Estructura try para controlar el error si no se establece la conexión
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        address_list = api.get_resource("/ip/firewall/address-list")
        queuesimple = api.get_resource("/queue/simple")
        i = 0
        lista_ids = []
        for ip in ips:
            address_list.get(comment=nombres[i])
            address_remove = address_list.get(comment=nombres[i])
            info_addrm = address_remove[0]
            idtorm = info_addrm['id']
            address_list.remove(id=idtorm) # Remueve el item en la address list
            address_list.add(address=ip, comment=nombres[i], list="ips_autorizadas_mikrospider") #Agrega la nueva ip en el address_list
            # Se elimina la antigua cola
            cola_rm = queuesimple.get(name=nombres[i])
            info_colarm = cola_rm[0]
            idtorm2 = info_colarm['id']
            queuesimple.remove(id=idtorm2)
            # Se calcula parámetros de la cola simple
            bl = str(plan[i]+5) + "M"
            bth = str(round(plan[i]/2)) + "M"
            bti = "16s"
            lat = str(round(plan[i]/2)-1) + "M"
            mli = str(plan[i]) + "M"
            # Se crea la nueva cola simple
            queuesimple.add(burst_limit=bl+"/"+bl, burst_threshold=bth+"/"+bth, burst_time=bti+"/"+bti,
                            limit_at=lat + "/" + lat, max_limit=mli+"/"+mli, name=nombres[i], target=ip+"/32")
            # Se obtiene la información (id) de los items creados en el mikrptik
            info_addlist = address_list.get(comment=nombres[i])
            info_queue = queuesimple.get(name=nombres[i])
            item1 = info_addlist[0]
            item2 = info_queue[0]
            id_addlist = item1['id']
            id_queue = item2['id']
            # Se crea un diccionario con los ids correspondientes y se va añadiendo a una lista la cual será resultado de la función
            ids = {"id_address_list": id_addlist, "id_queue_simple": id_queue}
            lista_ids.append(ids)
            i = i + 1
        if len(lista_ids) == 1:
            status = "Cliente activado exitosamente"
            return status, lista_ids
        else:
            status = "Clientes activados exitosamente"
            return status, lista_ids
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha podido realizar el o los cortes debido a un error de conexión."
        return status