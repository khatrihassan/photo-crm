from fastapi import FastAPI, HTTPException
# Pulls the FastAPI class out of the installed fastapi package 
#   and makes it usable in this file

from pydantic import BaseModel
# pulls the BaseModel class out of the pydantic package
# pydantic'sjob is decribing the shape data is supposed to have, and enforcing it 

import sqlite3
def get_connection():
    connection = sqlite3.connect("photo_crm.db")
    connection.row_factory = sqlite3.Row
    return connection

app = FastAPI()
#creats one instance of that class and names it app

class NewClient(BaseModel):
    id: str
    name: str
    email: str

# #TODO: a list of 3 client dict, each with id, name, email
# clients = [{"id":"01", "name":"TwinsBarberShop", "email":"sb@twinsbbs.com"},
#             {"id":"02", "name":"TwinsCoffeeShop", "email":"eshan@twins.com"},
#             {"id":"03", "name":"CommonwealthCafe","email":"cmw@commonwealthcafe.com"}]

@app.get("/clients")    # A decorator, registers the function below it in FastAPI's routing table
def get_clients():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

@app.get("/clients/{client_id}") # client_id is a placeholder
def get_client(client_id: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,) )
    row = cursor.fetchone()
    connection.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Client not found")
    else:
        return dict(row)
   
    # # TODO: loop through clients
    # for client in clients:
    # # TODO: if this client's id matches client_id, return it
    #     if client["id"] == client_id:
    #         return client
    # # TODO: if the loop finishes without finding one, return {"error": "not found"}
    # raise HTTPException(status_code=404, detail="Client not found") #raises an exception error when client is not found

@app.post("/clients")   #registers the function for POST requests to /clients
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

    # # TODO: turn new_client into a plain dict
    # client_dict = new_client.model_dump()   #model_dump because the list holds plain dicts, not pydantic objects

    # # TODO: add that dict to the clients list
    # clients.append(client_dict)

    # # TODO: return the dict you just added
    # return client_dict  # returns the created record, not the whole client list


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
    else:
        return {"deleted": client_id}

    # # TODO loop through clients
    # for client in clients:

    # # TODO if this client's id matches client_id, remove it and return a conformation
    #     if client["id"] == client_id:
    #         clients.remove(client)
    #         return {"deleted": client_id}
        
    # # TODO if the lopp finishes without finding one, return {"error": "not found"}
    # raise HTTPException(status_code=404, detail="Client not found")