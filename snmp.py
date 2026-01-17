from pysnmp.hlapi import *
    
class Device:
    def __init__(self, ip_device_):
        self.ip_device = ip_device_
        self.port_device = 161
        self.community = 'private'

    def set_speed(self, oid):
        next(setCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(),
            *oid)
        )
    
    def set_flow_control(self, oid):
        next(setCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(),
            *oid)
        )

    def set_address_learning(self, oid):
        next(setCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(),
            *oid)
        )

    def set_mdix(self, oid):
        next(setCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(),
            *oid)
        )

    def change_type_list_oids(self, oids):
        new_oids = oids
        for i in range(len(new_oids)):
            new_oids[i][1] = Integer(new_oids[i][1])
        return new_oids
    
    def is_combo_port(self, oid, port):
        list_index_ports = self.get_index_ports(oid)
        if (list_index_ports.count(int(port)) > 1):
            return True
        else:
            return False

    def set_state_port(self, oid):
        next(setCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(),
            *oid)
        )

    def get_list_ports(self, oid_index, oid_medium_types):
        list_index_ports = self.get_index_ports(oid_index)
        list_medium_types_ports =   self.get_medium_types_ports(oid_medium_types)
        list_ports = []
        for i in list_index_ports:
            list_ports.append(i)
        
        for i in range(len(list_ports)):
            list_ports[i] = str(list_index_ports[i]) + '.' + list_medium_types_ports[i]
                   
        return list_ports

    def get_index_ports(self, oid):
        list_index_ports = []

        iterator = bulkCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(), 0, 50, 
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False)

        MAX_REPS = 500
        count = 0

        while(count < MAX_REPS):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
                list_index_ports.append(varBinds[0].prettyPrint())
            except StopIteration:
                break
            count += 1
            
        for i in range(len(list_index_ports)):
            list_index_ports[i] = int(list_index_ports[i].partition('= ')[2])
      
        return list_index_ports  

    def get_medium_types_ports(self , oid):
        list_medium_types_ports = []

        iterator = bulkCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(), 0, 50, 
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False)
            
        MAX_REPS = 500
        count = 0

        while(count < MAX_REPS):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
                list_medium_types_ports.append(varBinds[0].prettyPrint())
            except StopIteration:
                break
            count += 1

        for i in range(len(list_medium_types_ports)):
            list_medium_types_ports[i] = list_medium_types_ports[i].partition('= ')[2]
            
        return list_medium_types_ports

    def get_states_ports(self, oid):
        list_states_ports = []
        iterator = bulkCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(), 0, 50, 
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False)
        
        MAX_REPS = 500
        count = 0
        while(count < MAX_REPS):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

                list_states_ports.append(varBinds[0].prettyPrint())
            except StopIteration:
                break
            count += 1
        
        for i in range(len(list_states_ports)):
            list_states_ports[i] = int(
                list_states_ports[i].partition('= ')[2])
        return list_states_ports

    def get_count_ports(self, oid):
        errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)))
        )
        for name, val in varBinds:
            return int(val.prettyPrint())

    def get_speeds_ports(self, oid):
        list_speeds_ports = []
        iterator = bulkCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(), 0, 50, 
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False)

        MAX_REPS = 500
        count = 0
        while(count < MAX_REPS):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
                list_speeds_ports.append(varBinds[0].prettyPrint())
            except StopIteration:
                break
            count += 1
        for i in range(len(list_speeds_ports)):
            list_speeds_ports[i] = int(list_speeds_ports[i].partition('= ')[2])

        return list_speeds_ports

    def get_flow_control_ports(self, oid):
        list_flow_control_ports = []
        iterator = bulkCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(), 0, 50, 
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False)

        MAX_REPS = 500
        count = 0
        while(count < MAX_REPS):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
                list_flow_control_ports.append(varBinds[0].prettyPrint())
            except StopIteration:
                break
            count += 1
            
        for i in range(len(list_flow_control_ports)):
            list_flow_control_ports[i] = int(list_flow_control_ports[i].partition('= ')[2])
        return list_flow_control_ports

    def get_address_learning_ports(self, oid):
        list_address_learning_ports = []
        iterator = bulkCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(), 0, 50, 
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False)

        MAX_REPS = 500
        count = 0
        while(count < MAX_REPS):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
                list_address_learning_ports.append(varBinds[0].prettyPrint())
            except StopIteration:
                break
            count += 1
            
        for i in range(len(list_address_learning_ports)):
            list_address_learning_ports[i] = int(list_address_learning_ports[i].partition('= ')[2])
        return list_address_learning_ports

    def get_link_status_ports(self, oid):
        list_link_status_ports = []
        iterator = bulkCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(), 0, 50, 
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False)

        MAX_REPS = 500
        count = 0
        while(count < MAX_REPS):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
                list_link_status_ports.append(varBinds[0].prettyPrint())
            except StopIteration:
                break
            count += 1
            
        for i in range(len(list_link_status_ports)):
            list_link_status_ports[i] = int(list_link_status_ports[i].partition('= ')[2])

        return list_link_status_ports

    def get_mdix_ports(self, oid):
        list_mdix_ports = []
        iterator = bulkCmd(SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.ip_device, self.port_device)),
            ContextData(), 0, 50, 
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False)

        MAX_REPS = 500
        count = 0
        while(count < MAX_REPS):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
                list_mdix_ports.append(varBinds[0].prettyPrint())
            except StopIteration:
                break
            count += 1
            
        for i in range(len(list_mdix_ports)):
            list_mdix_ports[i] = int(list_mdix_ports[i].partition('= ')[2])

        return list_mdix_ports

