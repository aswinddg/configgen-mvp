import sqlite3

conn = sqlite3.connect('configgen.db')
cursor = conn.cursor()
cursor.execute('SELECT scenario_id, key, label, type, options FROM params WHERE key = "wan_interface"')
results = cursor.fetchall()
print("Parámetros de wan_interface:")
for r in results:
    print(f'Scenario: {r[0]}, Key: {r[1]}, Label: {r[2]}, Type: {r[3]}, Options: {r[4]}')
conn.close()