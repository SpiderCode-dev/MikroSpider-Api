import routeros_api

##FUNCION QUE CREA REGLAS DE FIREWALL PARA CORTE DE SERVICIO  CLIENTES
# PARAMETROS
# ip_host: Es la ip pública del router mikrotik
# user: nombre de usuario previamente creado en el router con los permisos requeridos
# pwd: contraseña del usuario
# port: puerto API, este valor por lo general es 8728, el mismo que es habilitado previamente
def crear_reglas(ip_host, user, pwd, port):
    try:
        connection = routeros_api.RouterOsApiPool(ip_host, username=user, password=pwd, port=port, plaintext_login=True)
        api = connection.get_api()
        # CREACION DE ADDRESSLIST PARA CLIENTES CON SERVICIO ACTIVO Y CORTADO
        addresslist = api.get_resource("/ip/firewall/address-list")
        addresslist.add(address="1.1.1.1", comment="IP NO VALIDA", list="ips_autorizadas_mikrospider")
        addresslist.add(address="1.1.1.1", comment="IP NO VALIDA", list="ips_sin_servicio")
        # CREACION DE REGLA FIREWALL PARA PERMITIR TRAFICO DE CLIENTES ACTIVOS
        filter_rules = api.get_resource("/ip/firewall/filter")
        filter_rules.add(chain="FORWARD", action="accept", src_address_list="ips_autorizadas_mikrospider",
                         comment="Permitir trafico IPs Autorizadas")
        # CREACION DE UNA LISTA DE INTERFACE CON LA SALIDA A WAN
        interfaces = api.get_resource("/interface/list/member")
        interfaces.add(list="Lista_WAN", interface="ether1")
        # CREACION REGLAS DE NATEO PARA CORTES
        nat = api.get_resource("/ip/firewall/nat")
        nat.add(chain="dstnat", protocol="tcp", dst_port="!8291", in_interface_list="!Lista_WAN",
                src_address_list="ips_sin_servicio", action="redirect", to_ports="999", comment="Mikrospider - Suspension de clientes (TCP)")
        nat.add(chain="dstnat", protocol="udp", dst_port="!8291,53", in_interface_list="!Lista_WAN",
                src_address_list="ips_sin_servicio", action="redirect", to_ports="999", comment="Mikrospider - Suspension de clientes (UDP)")
        status = "Reglas para la suspensión del servicio creadas exitosamente."
    except routeros_api.exceptions.RouterOsApiConnectionError:
        status = "No se ha podido realizar los cambios debido a un error de conexión."
    return status
