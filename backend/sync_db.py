import sqlite3

conn = sqlite3.connect('configgen.db')
cur = conn.cursor()

# Clear existing data
cur.execute('DELETE FROM params')
cur.execute('DELETE FROM scenarios')
cur.execute('DELETE FROM vendors')

# Insert vendors
vendors = [
    (1, 'Mikrotik'),
    (2, 'Cisco'),
    (3, 'Juniper'),
]
cur.executemany('INSERT INTO vendors (id, name) VALUES (?, ?)', vendors)

# Insert scenarios
scenarios = [
    (1, 1, 'WAN IP Estática', 'Configuración Modular'),
    (2, 2, 'WAN IP Estática', 'Configuración Modular'),
    (3, 3, 'WAN IP Estática', 'Configuración Modular'),
]
cur.executemany('INSERT INTO scenarios (id, vendor_id, name, description) VALUES (?, ?, ?, ?)', scenarios)

# Insert params
params = [[1, 1, "system_identity", "Nombre del Router", "text", 1, "", ""], [2, 1, "wan_enabled", "¿Configurar WAN?", "select", 1, "", "Yes,No"], [3, 1, "wan_interface", "Interfaz WAN", "select", 1, "", "ether1,ether2,ether3,ether4,ether5,ether6,ether7,ether8,ether9,ether10,sfp1,sfp2"], [4, 1, "wan_type", "Tipo de WAN", "select", 1, "", "DHCP,Static"], [5, 1, "wan_ip", "IP WAN (Solo Static)", "text", 0, "", ""], [6, 1, "wan_mask", "Máscara WAN (CIDR)", "text", 0, "", ""], [7, 1, "gateway", "Gateway (Solo Static)", "text", 0, "", ""], [8, 1, "enable_nat", "¿Habilitar NAT?", "select", 1, "Yes", "Yes,No"], [9, 1, "nat_inside", "¿NAT Inside?", "text", 0, "ether2", ""], [10, 1, "nat_outside", "¿NAT Outside?", "text", 0, "ether1", ""], [11, 1, "nat_inside_source_static", "NAT Inside Source Static", "text", 0, "", ""], [12, 1, "nat_pool", "NAT Pool", "text", 0, "", ""], [13, 1, "nat_inside_source_list", "NAT Inside Source List", "text", 0, "", ""], [14, 1, "lan_enabled", "¿Configurar LAN?", "select", 1, "", "Yes,No"], [15, 1, "lan_type", "Tipo de LAN", "select", 1, "", "Bridge,Interface"], [16, 1, "lan_interface_name", "Nombre (Bridge o Interfaz)", "text", 1, "", ""], [17, 1, "bridge_ports", "Puertos Bridge (Sep. por coma)", "text", 0, "", ""], [18, 1, "lan_ip", "IP LAN (Gateway)", "text", 1, "", ""], [19, 1, "lan_mask", "Máscara LAN (CIDR)", "text", 1, "", ""], [20, 1, "lan_network", "Red LAN", "text", 1, "", ""], [21, 1, "dhcp_server_enabled", "¿Habilitar DHCP Server?", "select", 1, "", "Yes,No"], [22, 1, "dhcp_pool_start", "Inicio Pool DHCP", "text", 0, "", ""], [23, 1, "dhcp_pool_end", "Fin Pool DHCP", "text", 0, "", ""], [24, 1, "dhcp_lease_time", "Tiempo de Concesión", "text", 0, "", ""], [25, 1, "dns_servers", "DNS Servers", "text", 0, "", ""], [26, 1, "dns1", "DNS Primario", "text", 1, "", ""], [27, 1, "lan_interface", "Interfaz LAN", "select", 0, "", "GigabitEthernet0/0,GigabitEthernet0/1,GigabitEthernet0/2,GigabitEthernet0/3"], [1001, 2, "wan_enabled", "¿Configurar WAN?", "select", 1, "", "Yes,No"], [1002, 2, "wan_interface", "Interfaz WAN", "select", 1, "", "GigabitEthernet0/0,GigabitEthernet0/1,GigabitEthernet0/2,GigabitEthernet0/3"], [1003, 2, "wan_type", "Tipo de WAN", "select", 1, "", "DHCP,Static"], [1004, 2, "wan_ip", "IP WAN", "text", 0, "", ""], [1005, 2, "wan_mask", "Máscara WAN", "text", 0, "", ""], [1006, 2, "gateway", "Gateway", "text", 0, "", ""], [1007, 2, "dns1", "DNS Primario", "text", 1, "", ""], [1008, 2, "enable_nat", "¿Habilitar NAT?", "select", 1, "Yes", "Yes,No"], [1009, 2, "nat_inside", "¿NAT Inside?", "text", 0, "ether2", ""], [1010, 2, "nat_outside", "¿NAT Outside?", "text", 0, "ether1", ""], [1011, 2, "nat_inside_source_static", "NAT Inside Source Static", "text", 0, "", ""], [1012, 2, "nat_pool", "NAT Pool", "text", 0, "", ""], [1013, 2, "nat_inside_source_list", "NAT Inside Source List", "text", 0, "", ""], [1014, 2, "lan_enabled", "¿Configurar LAN?", "select", 1, "", "Yes,No"], [1015, 2, "lan_type", "Tipo de LAN", "select", 1, "", "VLAN,Interface"], [1016, 2, "lan_interface", "Interfaz LAN", "select", 0, "", "GigabitEthernet0/0,GigabitEthernet0/1,GigabitEthernet0/2,GigabitEthernet0/3"], [1017, 2, "lan_ip", "IP LAN", "text", 1, "", ""], [1018, 2, "lan_mask", "Máscara LAN", "text", 1, "", ""], [1019, 2, "system_identity", "Nombre del Router", "text", 1, "", ""], [1020, 2, "lan_interface_name", "Nombre (Bridge o Interfaz)", "text", 1, "", ""], [1021, 2, "bridge_ports", "Puertos Bridge (Sep. por coma)", "text", 0, "", ""], [1022, 2, "lan_network", "Red LAN", "text", 1, "", ""], [1023, 2, "dhcp_server_enabled", "¿Habilitar DHCP Server?", "select", 1, "", "Yes,No"], [1024, 2, "dhcp_pool_start", "Inicio Pool DHCP", "text", 0, "", ""], [1025, 2, "dhcp_pool_end", "Fin Pool DHCP", "text", 0, "", ""], [1026, 2, "dhcp_lease_time", "Tiempo de Concesión", "text", 0, "", ""], [1027, 2, "dns_servers", "DNS Servers", "text", 0, "", ""], [2001, 3, "wan_enabled", "¿Configurar WAN?", "select", 1, "", "Yes,No"], [2002, 3, "wan_interface", "Interfaz WAN", "select", 1, "", "ge-0/0/0,ge-0/0/1,ge-0/0/2,ge-0/0/3,ge-0/0/4,ge-0/0/5,ge-0/0/6,ge-0/0/7,ge-0/0/8,ge-0/0/9,ge-0/0/10"], [2003, 3, "wan_type", "Tipo de WAN", "select", 1, "", "DHCP,Static"], [2004, 3, "wan_ip", "IP WAN", "text", 0, "", ""], [2005, 3, "wan_mask", "Máscara WAN (CIDR)", "text", 0, "", ""], [2006, 3, "gateway", "Gateway", "text", 0, "", ""], [2007, 3, "dns1", "DNS Primario", "text", 1, "", ""], [2008, 3, "enable_nat", "¿Habilitar NAT?", "select", 1, "Yes", "Yes,No"], [2009, 3, "nat_inside", "¿NAT Inside?", "text", 0, "ether2", ""], [2010, 3, "nat_outside", "¿NAT Outside?", "text", 0, "ether1", ""], [2011, 3, "nat_inside_source_static", "NAT Inside Source Static", "text", 0, "", ""], [2012, 3, "nat_pool", "NAT Pool", "text", 0, "", ""], [2013, 3, "nat_inside_source_list", "NAT Inside Source List", "text", 0, "", ""], [2014, 3, "lan_enabled", "¿Configurar LAN?", "select", 1, "", "Yes,No"], [2015, 3, "lan_type", "Tipo de LAN", "select", 1, "", "VLAN,Interface"], [2016, 3, "lan_interface", "Interfaz LAN", "select", 0, "", "ge-0/0/0,ge-0/0/1,ge-0/0/2,ge-0/0/3,ge-0/0/4,ge-0/0/5,ge-0/0/6,ge-0/0/7,ge-0/0/8,ge-0/0/9,ge-0/0/10"], [2017, 3, "lan_ip", "IP LAN", "text", 1, "", ""], [2018, 3, "lan_mask", "Máscara LAN (CIDR)", "text", 1, "", ""], [2019, 3, "system_identity", "Nombre del Router", "text", 1, "", ""], [2020, 3, "lan_interface_name", "Nombre (Bridge o Interfaz)", "text", 1, "", ""], [2021, 3, "bridge_ports", "Puertos Bridge (Sep. por coma)", "text", 0, "", ""], [2022, 3, "lan_network", "Red LAN", "text", 1, "", ""], [2023, 3, "dhcp_server_enabled", "¿Habilitar DHCP Server?", "select", 1, "", "Yes,No"], [2024, 3, "dhcp_pool_start", "Inicio Pool DHCP", "text", 0, "", ""], [2025, 3, "dhcp_pool_end", "Fin Pool DHCP", "text", 0, "", ""], [2026, 3, "dhcp_lease_time", "Tiempo de Concesión", "text", 0, "", ""], [2027, 3, "dns_servers", "DNS Servers", "text", 0, "", ""]]

cur.executemany('INSERT INTO params (id, scenario_id, key, label, type, required, default_value, options) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', params)

conn.commit()
print('Database synced!')
print(f'Vendors: {cur.execute("SELECT COUNT(*) FROM vendors").fetchone()[0]}')
print(f'Scenarios: {cur.execute("SELECT COUNT(*) FROM scenarios").fetchone()[0]}')  
print(f'Params: {cur.execute("SELECT COUNT(*) FROM params").fetchone()[0]}')
