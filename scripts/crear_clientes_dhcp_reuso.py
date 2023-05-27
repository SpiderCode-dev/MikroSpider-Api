import random

import routeros_api

##FUNCION PARA CREAR CLIENTES CON AMARRE DE IP MAC, DHCP Y PLAN DE REUSO
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# nombres = Lista del o los clientes a añadir
# ips = lista de ips de cada cliente (la información debe ser simétrica en cuanto al orden de en los que se ubican los nombreS)
# macaddress = lista de direccion o direcciones mac del equipo cliente
# interfaz = lista de la interfaz lan en la que se encuenta el cliente o clientes
# dhcp_server = lista del nombre derl server DHCP en el que se encuentra la ip del o los clientes.
# plan = lista de velocidades del plan del cliente (Por ejemplo: 45, 65 etc...) en formato entero
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero y de los planes
# La función devolvera una lista con el id del item creado en el address-list y el id del item creado en la cola
def crearclientes_dhcp_reuso(ip_host, user, pwd, port, nombres, ips, macaddress, interfaz, dhcp_server, plan):
    try: # Estructura try para controlar el error si no se establece la conexión
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        address_list = api.get_resource("/ip/firewall/address-list")
        cola = api.get_resource("/queue/simple")
        arp = api.get_resource("/ip/arp")
        dhcp = api.get_resource("/ip/dhcp-server/lease")
        i = 0
        lista_ids = []
        for ip in ips:
            num_cola = cola.get()
            if len(num_cola) == 0:
                lat = str(plan[i]) + "M"
                mli = str(plan[i]) + "M"
                id_cola_padre = str(random.randint(1, 999999))
                cola.add(comment="Plan: PLUS_REHUSO_1 - Router: PRUEBA", limit_at=lat + "/" + lat,
                         max_limit=mli + "/" + mli,
                         name="Plan_" + id_cola_padre + "_Mikrospider", queue="pcq-upload-default/pcq-download-default",
                         target=ip+ "/32")  # Cola padre
                cola.add(limit_at=lat + "/" + lat, max_limit=mli + "/" + mli, name=nombres[i], target=ip + "/32",
                         queue="pcq-upload-default/pcq-download-default",
                         parent="Plan_" + id_cola_padre + "_Mikrospider")
            else:
                for j in range(len(num_cola)):
                    info_cola = cola.get(comment="Plan: PLUS_REHUSO_" + str(j + 1) + " - Router: PRUEBA")
                    if len(info_cola) != 0:
                        item = info_cola[0]
                        id_parent = item['id']
                        nombre_padre = item['name']
                        target = item['target']
                        if len(target.split(sep=",")) < 3:
                            plan_parent = nombre_padre
                            ips_n = target + "," + ip + "/32"
                            lat = str(plan[i]) + "M"
                            mli = str(plan[i]) + "M"
                            cola.set(id=id_parent, target=ips_n)  # Edit cola padre
                            cola.add(limit_at=lat + "/" + lat, max_limit=mli + "/" + mli, name=nombres[i],
                                     target=ip[i] + "/32",
                                     queue="pcq-upload-default/pcq-download-default", parent=plan_parent)
                            break
                    else:
                        lat = str(plan[i]) + "M"
                        mli = str(plan[i]) + "M"
                        id_cola_padre = str(random.randint(1, 999999))
                        cola.add(comment="Plan: PLUS_REHUSO_" + str(j + 1) + " - Router: PRUEBA",
                                 limit_at=lat + "/" + lat,
                                 max_limit=mli + "/" + mli,
                                 name="Plan_" + id_cola_padre + "_Mikrospider",
                                 queue="pcq-upload-default/pcq-download-default",
                                 target=ip + "/32")  # Cola padre
                        cola.add(limit_at=lat + "/" + lat, max_limit=mli + "/" + mli, name=nombres[i], target=ip + "/32",
                                 queue="pcq-upload-default/pcq-download-default",
                                 parent="Plan_" + id_cola_padre + "_Mikrospider")
                        break
            address_list.add(address=ip, comment=nombres[i], list="ips_autorizadas_mikrospider")  # Agrega el cliente en el address_list
            infoarp = arp.get(mac_address=macaddress[i])
            lista_infoarp = infoarp[0]
            macfr = lista_infoarp['mac_address'] # Obtiene la mac desde el router
            ipfr = lista_infoarp['address'] # Obtiene la ip desde el router
            if ip == ipfr and macaddress[i] == macfr: # Controla que la información ingresada coincida con la del router
                arp.add(address=ip, comment=nombres[i], interface=interfaz[i], mac_address=macaddress[i])  # Agrega el cliente en el arp
                dhcp.add(address=ip, client_id=macaddress[i], comment=nombres[i], mac_address=macaddress[i],
                         server=dhcp_server)  # Agrega el cliente en el dhcp lease
                mensaje = "Información IP/MAC ingresada correctamente"
            else:
                mensaje = "La dirección IP o MAC no coinciden con lo existente en el router"
            # Se obtiene la información (id) de los items creados en el mikrptik
            info_addlist = address_list.get(comment=nombres[i])
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
            return mensaje, status, lista_ids
        else:
            status = "Clientes activados exitosamente"
            return mensaje, status, lista_ids
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha procesado la información debido a un error de conexión."
        return status

