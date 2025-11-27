import asyncio
import sqlite3

async def simple_setup():
    conn = sqlite3.connect('configgen.db')
    cursor = conn.cursor()
    
    try:
        # Agregar parámetro de interfaz para Mikrotik (scenario_id = 1)
        cursor.execute("""
            INSERT OR REPLACE INTO params (scenario_id, key, label, type, required, default_value, options)
            VALUES (1, 'wan_interface', 'Interfaz WAN', 'select', 1, 'ether1', 'ether1,ether2,ether3,ether4,ether5,ether6,ether7,ether8,ether9,ether10,ether11,sfp1,sfp2')
        """)

        # Nuevos parámetros para Mikrotik (scenario_id = 1)
        mikrotik_params = [
            (1, 'bridge_name', 'Nombre del Bridge', 'text', 1, '', ''),
            (1, 'lan_ip', 'IP LAN', 'text', 1, '', ''),
            (1, 'lan_mask', 'Máscara LAN (CIDR)', 'text', 1, '', ''),
            (1, 'lan_network', 'Red LAN', 'text', 1, '', ''),
            (1, 'dhcp_pool_start', 'Inicio Pool DHCP', 'text', 1, '', ''),
            (1, 'dhcp_pool_end', 'Fin Pool DHCP', 'text', 1, '', ''),
            (1, 'dhcp_lease_time', 'Tiempo de Concesión', 'text', 1, '', ''),
            (1, 'dns_servers', 'Servidores DNS', 'text', 1, '', ''),
            (1, 'system_identity', 'Nombre del Router', 'text', 1, '', '')
        ]

        for param in mikrotik_params:
            cursor.execute("""
                INSERT OR REPLACE INTO params (scenario_id, key, label, type, required, default_value, options)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, param)
        
        # Crear scenario para Cisco si no existe
        cursor.execute("SELECT id FROM vendors WHERE name = 'Cisco'")
        cisco_vendor = cursor.fetchone()
        if cisco_vendor:
            cisco_vendor_id = cisco_vendor[0]
            
            # Crear scenario para Cisco
            cursor.execute("""
                INSERT OR IGNORE INTO scenarios (vendor_id, name, description)
                VALUES (?, 'WAN IP Estática', 'Configuración WAN con IP estática para Cisco')
            """, (cisco_vendor_id,))
            
            # Obtener el scenario_id de Cisco
            cursor.execute("SELECT id FROM scenarios WHERE vendor_id = ? AND name = 'WAN IP Estática'", (cisco_vendor_id,))
            cisco_scenario = cursor.fetchone()
            if cisco_scenario:
                cisco_scenario_id = cisco_scenario[0]
                
                # Crear interfaces para Cisco
                cisco_interfaces = [f"GigabitEthernet0/{i}" for i in range(49)]
                
                # Parámetros para Cisco
                params = [
                    (cisco_scenario_id, 'wan_interface', 'Interfaz WAN', 'select', 1, 'GigabitEthernet0/0', ','.join(cisco_interfaces)),
                    (cisco_scenario_id, 'wan_ip', 'IP WAN', 'text', 1, '192.168.1.1', ''),
                    (cisco_scenario_id, 'wan_mask', 'Máscara WAN', 'text', 1, '255.255.255.0', ''),
                    (cisco_scenario_id, 'gateway', 'Gateway', 'text', 1, '192.168.1.1', ''),
                    (cisco_scenario_id, 'dns1', 'DNS Primario', 'text', 1, '8.8.8.8', '')
                ]
                
                for param in params:
                    cursor.execute("""
                        INSERT OR REPLACE INTO params (scenario_id, key, label, type, required, default_value, options)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, param)
        
        # Crear scenario para Juniper si no existe
        cursor.execute("SELECT id FROM vendors WHERE name = 'Juniper'")
        juniper_vendor = cursor.fetchone()
        if juniper_vendor:
            juniper_vendor_id = juniper_vendor[0]
            
            # Crear scenario para Juniper
            cursor.execute("""
                INSERT OR IGNORE INTO scenarios (vendor_id, name, description)
                VALUES (?, 'WAN IP Estática', 'Configuración WAN con IP estática para Juniper')
            """, (juniper_vendor_id,))
            
            # Obtener el scenario_id de Juniper
            cursor.execute("SELECT id FROM scenarios WHERE vendor_id = ? AND name = 'WAN IP Estática'", (juniper_vendor_id,))
            juniper_scenario = cursor.fetchone()
            if juniper_scenario:
                juniper_scenario_id = juniper_scenario[0]
                
                # Crear interfaces para Juniper
                juniper_interfaces = [f"ge-0/0/{i}" for i in range(11)]
                
                # Parámetros para Juniper
                params = [
                    (juniper_scenario_id, 'wan_interface', 'Interfaz WAN', 'select', 1, 'ge-0/0/0', ','.join(juniper_interfaces)),
                    (juniper_scenario_id, 'wan_ip', 'IP WAN', 'text', 1, '192.168.1.1', ''),
                    (juniper_scenario_id, 'wan_mask', 'Máscara WAN', 'text', 1, '24', ''),
                    (juniper_scenario_id, 'gateway', 'Gateway', 'text', 1, '192.168.1.1', ''),
                    (juniper_scenario_id, 'dns1', 'DNS Primario', 'text', 1, '8.8.8.8', '')
                ]
                
                for param in params:
                    cursor.execute("""
                        INSERT OR REPLACE INTO params (scenario_id, key, label, type, required, default_value, options)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, param)
        
        conn.commit()
        print("✅ Setup completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(simple_setup())