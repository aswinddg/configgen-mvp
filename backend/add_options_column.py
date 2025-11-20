import asyncio
import sqlite3

async def add_options_column():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('configgen.db')
    cursor = conn.cursor()
    
    try:
        # Verificar si la columna options ya existe
        cursor.execute("PRAGMA table_info(params)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'options' not in columns:
            # Agregar la columna options
            cursor.execute("ALTER TABLE params ADD COLUMN options TEXT")
            print("✅ Columna 'options' agregada exitosamente")
        else:
            print("✅ Columna 'options' ya existe")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(add_options_column())