import routeros_api

##FUNCION PARA ACTUALIZAR INFO DE CLIENTES IP DINAMICA PPPoE + QUEUE ESTÁTICAS + ARP MARK STATIC
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# nombres = Lista del o los clientes a añadir
# ips = lista de ips de cada cliente (la información debe ser simétrica en cuanto al orden de en los que se ubican los nombreS)
# macaddress = lista de direccion o direcciones mac del equipo cliente
# interfaz = lista de la interfaz lan en la que se encuenta el cliente o clientes
# plan = lista de velocidades del plan del cliente (Por ejemplo: 45, 65 etc...) en formato entero
# localip = lista de ip local o gateway del pool de ip donde pertenece el cliente
# user_pppoe = lista de usuarios pppoe
# pwd_pppoe = lista de contraseñas de pppoe
# perfil_pppoe = lista del nombre de perfil asignado al servidor PPPoE
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero y de los planes
# La función devolvera una lista con el id del item creado en el address-list y el id del item creado en la cola
def actualizar_cliente_amarreip_pppoe(ip_host, user, pwd, port, nombres, ips, macaddress, interfaz, plan, localip, user_pppoe, pwd_pppoe, perfil_pppoe):
    try: # Estructura try para controlar el error si no se establece la conexión
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        i = 0
        lista_ids = []
        # Recursos del mikrotik a utilizar
        ppp = api.get_resource("/ppp/secret")
        arp = api.get_resource("/ip/arp")
        cola = api.get_resource("/queue/simple")
        add_list = api.get_resource("/ip/firewall/address-list")
        for ip in ips:
            # Eliminar información anterior del cliente en el mikrotik
            delete_arp = arp.get(comment=nombres[i])
            delete_addlist = add_list.get(comment=nombres[i])
            delete_queue = cola.get(name=nombres[i])
            delete_pppoe = ppp.get(comment=nombres[i])
            item_arp = delete_arp[0]
            item_addlist = delete_addlist[0]
            item_queue = delete_queue[0]
            item_pppoe = delete_pppoe[0]
            id2rm_arp = item_arp['id']
            id2rm_addlist = item_addlist['id']
            id2rm_queue = item_queue['id']
            id2rm_pppoe = item_pppoe['id']
            arp.remove(id=id2rm_arp)
            add_list.remove(id=id2rm_addlist)
            cola.remove(id=id2rm_queue)
            ppp.remove(id=id2rm_pppoe)
            # Crear ppp secret
            ppp.add(caller_id=macaddress[i], comment=nombres[i], local_address=localip, name=user_pppoe, password=pwd_pppoe,
                    profile=perfil_pppoe, remote_address=ip, service="pppoe")
            # Marcar estatico en arp
            arp.add(address=ip, comment=nombres[i], interface=interfaz, mac_address=macaddress[i])
            # Agregar cliente a address list
            add_list.add(address=ip, comment=nombres[i], list="ips_autorizadas_mikrospider")
            # Se calcula parámetros de la cola simple
            bl = str(plan[i] + 5) + "M"
            bth = str(round(plan[i] / 2)) + "M"
            bti = "16s"
            lat = str(round(plan[i] / 2) - 1) + "M"
            mli = str(plan[i]) + "M"
            # Se crea la cola simple
            cola.add(burst_limit=bl + "/" + bl, burst_threshold=bth + "/" + bth, burst_time=bti + "/" + bti,
                     limit_at=lat + "/" + lat, max_limit=mli + "/" + mli, name=nombres[i], target=ip + "/32",
                     queue="default/default", total_queue="default")
            # Se obtiene la información (id) de los items creados en el mikrptik
            info_addlist = add_list.get(comment=nombres[i])
            info_queue = cola.get(name=nombres[i])
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
        status = "No se ha procesado la información debido a un error de conexión."
        return status