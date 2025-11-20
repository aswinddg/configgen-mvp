import asyncio
from .core.database import engine, Base, AsyncSessionLocal
from .core.models import Vendor, Scenario, Param

async def init_database():
    # Crear todas las tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Insertar datos
    async with AsyncSessionLocal() as session:
        # Crear vendors
        mikrotik = Vendor(name="Mikrotik")
        cisco = Vendor(name="Cisco")
        juniper = Vendor(name="Juniper")
        
        session.add_all([mikrotik, cisco, juniper])
        await session.flush()  # Para obtener los IDs sin hacer commit
        
        # Crear scenarios para Mikrotik
        wan_static = Scenario(
            vendor_id=mikrotik.id,
            name="WAN IP Estática",
            description="Configuración WAN con IP estática"
        )
        
        wan_pppoe = Scenario(
            vendor_id=mikrotik.id,
            name="WAN PPPoE", 
            description="Configuración WAN con PPPoE"
        )
        
        session.add_all([wan_static, wan_pppoe])
        await session.flush()
        
        # Crear parámetros para WAN IP Estática
        params = [
            Param(scenario_id=wan_static.id, key="wan_ip", label="IP WAN", type="ip", required=True),
            Param(scenario_id=wan_static.id, key="wan_mask", label="Máscara WAN", type="string", required=True, default_value="24"),
            Param(scenario_id=wan_static.id, key="gateway", label="Gateway", type="ip", required=True),
            Param(scenario_id=wan_static.id, key="dns1", label="DNS Primario", type="ip", required=True, default_value="8.8.8.8"),
        ]
        
        session.add_all(params)
        await session.commit()
        
        print("✅ Base de datos inicializada correctamente!")

if __name__ == "__main__":
    asyncio.run(init_database())