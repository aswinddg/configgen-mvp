import sqlite3

def remove_duplicates():
    conn = sqlite3.connect('configgen.db')
    cursor = conn.cursor()
    
    try:
        # Find duplicates
        cursor.execute("""
            SELECT scenario_id, key, COUNT(*) 
            FROM params 
            GROUP BY scenario_id, key 
            HAVING COUNT(*) > 1
        """)
        duplicates = cursor.fetchall()
        
        if not duplicates:
            print("No duplicates found.")
            return

        print(f"Found {len(duplicates)} duplicate keys. Cleaning up...")
        
        for scenario_id, key, count in duplicates:
            print(f"Removing duplicates for {key} (Scenario {scenario_id})...")
            # Keep the one with the highest ID (latest)
            cursor.execute("""
                DELETE FROM params 
                WHERE scenario_id = ? AND key = ? 
                AND id NOT IN (
                    SELECT MAX(id) 
                    FROM params 
                    WHERE scenario_id = ? AND key = ?
                )
            """, (scenario_id, key, scenario_id, key))
            
        conn.commit()
        print("✅ Duplicates removed.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    remove_duplicates()
