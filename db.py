import sqlite3

def get_connection():
    connection = sqlite3.connect("photo_crm.db")
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_connection()

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



    connection.commit()

    connection.close()