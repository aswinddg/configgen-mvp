import sqlite3
import json

conn = sqlite3.connect('configgen.db')
cur = conn.cursor()

# Get all params
cur.execute('SELECT id, scenario_id, key, label, type, required, default_value, options FROM params ORDER BY scenario_id, id')
params = cur.fetchall()

# Create sync script
script = '''import sqlite3

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
params = ''' + json.dumps(params, ensure_ascii=False) + '''

cur.executemany('INSERT INTO params (id, scenario_id, key, label, type, required, default_value, options) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', params)

conn.commit()
print('Database synced!')
print(f'Vendors: {cur.execute("SELECT COUNT(*) FROM vendors").fetchone()[0]}')
print(f'Scenarios: {cur.execute("SELECT COUNT(*) FROM scenarios").fetchone()[0]}')  
print(f'Params: {cur.execute("SELECT COUNT(*) FROM params").fetchone()[0]}')
'''

with open('sync_db.py', 'w', encoding='utf-8') as f:
    f.write(script)
print('Created sync_db.py')
