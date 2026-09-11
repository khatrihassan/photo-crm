from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


import sqlite3
def get_connection():
    connection = sqlite3.connect("photo_crm.db")
    connection.row_factory = sqlite3.Row
    return connection

app = FastAPI()


class NewClient(BaseModel):
    id: str
    name: str
    email: str


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
   

@app.post("/clients")
def create_client(new_client: NewClient):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO clients (id, name, email) VALUES (?, ?, ?)",
                   (new_client.id, new_client.name, new_client.email)
                   )
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
