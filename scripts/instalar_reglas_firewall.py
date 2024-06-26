import routeros_api

##FUNCION QUE CREA REGLAS DE FIREWALL PARA CORTE DE SERVICIO  CLIENTES
# PARAMETROS
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
# interfaz: interfaz del mikrotik por el que tiene salida a internet o WAN (puede ser una interfaz o varias interfaces a modo de lista)
# El formato de los datos a ingresar son tipo String, a excepción del puerto API que puede ser ingresado como número entero
def crear_reglas(ip_host, user, pwd, port, interfaz):
    try:
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        nat = api.get_resource("/ip/firewall/nat")
        # HABILITAR NAT PARA CREAR LAS REGLAS DE BLOQUEO
        nat.add(action="accept", chain="srcnat", comment="NAT ALL")
        # CREACION DE NOMBRE DE LA LISTA DE INTERFACE CON SALIDA A WAN
        interface_name = api.get_resource("/interface/list")
        interface_name.add(name="Lista_WAN")
        # CREACION DE REGLA FIREWALL PARA PERMITIR TRAFICO DE CLIENTES ACTIVOS Y BLOQUEAR PUERTO 999
        filter_rules = api.get_resource("/ip/firewall/filter")
        filter_rules.add(chain="FORWARD", action="accept", src_address_list="ips_autorizadas_mikrospider",
                         comment="Permitir trafico IPs Autorizadas")
        filter_rules.add(chain="INPUT", action="drop", comment="Bloquear puerto WebProxy desde WANs", dst_port="999", in_interface_list="Lista_WAN",
                         protocol="tcp")
        # CREACION DE UN MIEMBRO/MIEMBROS EN LA LISTA DE INTERFACE CON LA SALIDA A WAN
        interface_list = api.get_resource("/interface/list/member")
        for i in interfaz:
            interface_list.add(list="Lista_WAN", interface=i)
        # CREACION REGLAS DE NATEO PARA CORTES
        nat.add(chain="dstnat", protocol="tcp", dst_port="!8291", in_interface_list="!Lista_WAN",
                src_address_list="ips_sin_servicio", action="redirect", to_ports="999", comment="Mikrospider - Suspension de clientes (TCP)")
        nat.add(chain="dstnat", protocol="udp", dst_port="!8291,53", in_interface_list="!Lista_WAN",
                src_address_list="ips_sin_servicio", action="redirect", to_ports="999", comment="Mikrospider - Suspension de clientes (UDP)")
        nat.add(action="accept", chain="dstnat", comment="Mikrospider - Permitir pagina web morosos",
                dst_address_list="servers_mikrospider", src_address_list="ips_sin_servicio")
        nat.add(action="accept", chain="dstnat", comment="Mikrospider - Permitir pagina web avisos",
                dst_address_list="servers_mikrospider", src_address_list="Aviso")
        nat.add(chain="dstnat", protocol="tcp", dst_port="!8291", in_interface_list="!Lista_WAN",
                src_address_list="Aviso", action="redirect", to_ports="999",
                comment="Mikrospider - Aviso de Pago en Pantalla de clientes(TCP)")
        nat.add(chain="dstnat", protocol="udp", dst_port="!8291,53", in_interface_list="!Lista_WAN",
                src_address_list="Aviso", action="redirect", to_ports="999",
                comment="Mikrospider - Aviso de Pago en Pantalla de clientes(UDP)")
        # HABILITAR EL WEB PROXY
        proxy = api.get_resource("/ip/proxy")
        proxy.set(enabled="yes", max_fresh_time="10s", port="999")
        status = "Reglas para la suspensión del servicio creadas exitosamente."
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha podido realizar los cambios debido a un error de conexión."
    return status
