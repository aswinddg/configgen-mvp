import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.models import Vendor, Scenario, Param

async def setup_vendor_interfaces():
    engine = create_async_engine("sqlite+aiosqlite:///./configgen.db")
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        # Obtener vendors
        vendors = await session.execute(text("SELECT * FROM vendors"))
        vendors_data = vendors.fetchall()
        
        # Obtener scenarios
        scenarios = await session.execute(text("SELECT * FROM scenarios"))
        scenarios_data = scenarios.fetchall()
        
        print("Vendors existentes:", vendors_data)
        print("Scenarios existentes:", scenarios_data)
        
        # Agregar vendors faltantes si no existen
        vendor_names = [v[1] for v in vendors_data]  # v[1] es el name
        
        if "Cisco IOS" not in vendor_names:
            cisco_vendor = Vendor(name="Cisco IOS")
            session.add(cisco_vendor)
            await session.flush()
            
            # Agregar scenario para Cisco
            cisco_scenario = Scenario(
                vendor_id=cisco_vendor.id,
                name="WAN IP Estática",
                description="Configuración de IP estática en interfaz WAN para Cisco IOS"
            )
            session.add(cisco_scenario)
            await session.flush()
            
            # Parámetros para Cisco
            cisco_params = [
                Param(scenario_id=cisco_scenario.id, key="wan_interface", label="Interfaz WAN", 
                      type="select", required=True, default_value="GigabitEthernet0/0",
                      options=",".join([f"GigabitEthernet0/{i}" for i in range(49)])),
                Param(scenario_id=cisco_scenario.id, key="wan_ip", label="IP WAN", 
                      type="text", required=True, default_value="192.168.1.1"),
                Param(scenario_id=cisco_scenario.id, key="wan_mask", label="Máscara WAN", 
                      type="text", required=True, default_value="255.255.255.0"),
                Param(scenario_id=cisco_scenario.id, key="gateway", label="Gateway", 
                      type="text", required=True, default_value="192.168.1.1"),
                Param(scenario_id=cisco_scenario.id, key="dns1", label="DNS Primario", 
                      type="text", required=True, default_value="8.8.8.8")
            ]
            for param in cisco_params:
                session.add(param)
        
        if "Juniper" not in vendor_names:
            juniper_vendor = Vendor(name="Juniper")
            session.add(juniper_vendor)
            await session.flush()
            
            # Agregar scenario para Juniper
            juniper_scenario = Scenario(
                vendor_id=juniper_vendor.id,
                name="WAN IP Estática",
                description="Configuración de IP estática en interfaz WAN para Juniper"
            )
            session.add(juniper_scenario)
            await session.flush()
            
            # Parámetros para Juniper
            juniper_params = [
                Param(scenario_id=juniper_scenario.id, key="wan_interface", label="Interfaz WAN", 
                      type="select", required=True, default_value="ge-0/0/0",
                      options=",".join([f"ge-0/0/{i}" for i in range(11)])),
                Param(scenario_id=juniper_scenario.id, key="wan_ip", label="IP WAN", 
                      type="text", required=True, default_value="192.168.1.1"),
                Param(scenario_id=juniper_scenario.id, key="wan_mask", label="Máscara WAN", 
                      type="text", required=True, default_value="24"),
                Param(scenario_id=juniper_scenario.id, key="gateway", label="Gateway", 
                      type="text", required=True, default_value="192.168.1.1"),
                Param(scenario_id=juniper_scenario.id, key="dns1", label="DNS Primario", 
                      type="text", required=True, default_value="8.8.8.8")
            ]
            for param in juniper_params:
                session.add(param)
        
        # Actualizar Mikrotik con nuevas interfaces
        mikrotik_scenario_id = None
        for scenario in scenarios_data:
            if scenario[1] == 1:  # vendor_id = 1 (Mikrotik)
                mikrotik_scenario_id = scenario[0]
                break
        
        if mikrotik_scenario_id:
            # Eliminar parámetro de interfaz existente si existe
            await session.execute(
                text("DELETE FROM params WHERE scenario_id = :scenario_id AND key = 'wan_interface'")
                .bindparams(scenario_id=mikrotik_scenario_id)
            )
            
            # Agregar nuevo parámetro de interfaz para Mikrotik
            mikrotik_interfaces = []
            # GigabitEthernet 0-10
            mikrotik_interfaces.extend([f"ether{i+1}" for i in range(11)])
            # SFP 1 y 2
            mikrotik_interfaces.extend(["sfp1", "sfp2"])
            
            mikrotik_interface_param = Param(
                scenario_id=mikrotik_scenario_id,
                key="wan_interface",
                label="Interfaz WAN",
                type="select",
                required=True,
                default_value="ether1",
                options=",".join(mikrotik_interfaces)
            )
            session.add(mikrotik_interface_param)
        
        await session.commit()
        print("✅ Interfaces por vendor configuradas exitosamente")

if __name__ == "__main__":
    asyncio.run(setup_vendor_interfaces())