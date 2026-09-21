import sqlite3

def get_connection():
    connection = sqlite3.connect("photo_crm.db")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def init_db():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS shoots (
                    id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,
                    date TEXT NOT NULL,
                    shoot_type TEXT NOT NULL,
                    status TEXT NOT NULL
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

    cursor.execute(
        "INSERT OR IGNORE INTO shoots (id, client_id, date, shoot_type, status) VALUES (?, ?, ?, ?, ?)",
        ("s01", "01", "2026-09-25", "reel batch", "booked")
    )

    connection.commit()

    connection.close()