import sqlite3

connection = sqlite3.connect("photo_crm.db")

cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)""")

cursor.execute(
    "INSERT OR IGNORE INTO clients (id, name, email) VALUES (?, ?, ?)",
    ("01", "TwinsBarberShop", "sb@twinsbbs.com")
)

cursor.execute(
    "INSERT OR IGNORE INTO clients (id, name, email) VALUES (?, ?, ?)",
    ("02", "TwinsCoffeeShop", "eshan@twins.com")
)

cursor.execute(
    "INSERT OR IGNORE INTO clients (id, name, email) VALUES (?, ?, ?)",
    ("03", "CommonwealthCoffee", "cmw@commonwealthcafe.com")
)

cursor.execute("SELECT * FROM clients")
print(cursor.fetchall())

connection.commit()

connection.close()