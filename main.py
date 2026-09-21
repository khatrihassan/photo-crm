from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_connection, init_db
import sqlite3

app = FastAPI()

init_db()


class NewClient(BaseModel):
    id: str
    name: str
    email: str

class NewShoot(BaseModel):
    id: str
    date: str
    shoot_type: str
    status: str


@app.get("/clients")
def get_clients():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

@app.get("/clients/{client_id}")
def get_client(client_id: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,) )
    row = cursor.fetchone()
    connection.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return dict(row)
   

@app.post("/clients", status_code=201)
def create_client(new_client: NewClient):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO clients (id, name, email) VALUES (?, ?, ?)",
                   (new_client.id, new_client.name, new_client.email)
                   )
    except sqlite3.IntegrityError:
        connection.close()
        raise HTTPException(status_code=409, detail="A client with that id already exists")
    connection.commit()
    connection.close()
    client_dict = new_client.model_dump()
    return client_dict

@app.delete("/clients/{client_id}")
def delete_client(client_id: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    rowcounter = cursor.rowcount
    connection.commit()
    connection.close()
    if rowcounter == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"deleted": client_id}

@app.put("/clients/{client_id}")
def update_client(client_id: str, updated: NewClient):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE clients SET name = ?, email = ? WHERE id = ?", (updated.name, updated.email, client_id))
    rowcounter = cursor.rowcount
    connection.commit()
    connection.close()
    if rowcounter == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"updated": client_id}

@app.post("/clients/{client_id}/shoots", status_code=201)
def create_shoot(client_id: str, new_shoot: NewShoot):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    if cursor.fetchone() is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Client not found")
    
    try:
        cursor.execute(
            "INSERT INTO shoots (id, client_id, date, shoot_type, status) VALUES (?, ?, ?, ?, ?)",
            (new_shoot.id, client_id, new_shoot.date, new_shoot.shoot_type, new_shoot.status)
        )
    except sqlite3.OperationalError:
        connection.close()
        raise HTTPException(status_code=409, detail="A shoot with that id already exists")
    
    connection.commit()
    connection.close()

    shoot_dict = new_shoot.model_dump()
    shoot_dict["client_id"] = client_id
    return shoot_dict