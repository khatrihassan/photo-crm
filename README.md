photo-crm

A lightweight client management API for photographers and videographers, built with FastAPI and SQLite.

Freelance photographers typically track clients across a mix of Instagram DMs, WhatsApp threads, and spreadsheets. This project is a small, self-hosted backend that gives them a single source of truth for client records, with a clean REST interface that a web or mobile front end can sit on top of.

Live: https://photo-crm-hozv.onrender.com/docs

Status

Core client CRUD is complete, tested, and deployed. The API runs against a persistent SQLite database with full create, read, update, and delete support and meaningful HTTP status codes on every failure path. See Roadmap for what's next.

Tech stack
Layer	Choice
Language	Python 3
Web framework	FastAPI
Validation	Pydantic
Database	SQLite (via the standard-library sqlite3 module)
Server	Uvicorn
Hosting	Render
Docs	Auto-generated OpenAPI / Swagger UI

No ORM. Queries are written directly against sqlite3 with parameterised statements, which keeps the data layer transparent and dependency-light.

Getting started
Prerequisites
Python 3.9 or newer
git
Setup
git clone git@github.com:khatrihassan/photo-crm.git
cd photo-crm

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
Run the server
uvicorn main:app --reload

The API is then available at http://127.0.0.1:8000.

There is no separate database setup step. init_db() runs on startup and creates the SQLite file, the clients table, and a small set of seed records if they do not already exist. It is safe to run on every boot — CREATE TABLE IF NOT EXISTS and INSERT OR IGNORE make it a no-op once the data is in place. This is what allows a fresh clone, or a fresh deployment, to work with no manual intervention.

Interactive documentation is served at http://127.0.0.1:8000/docs, which is the easiest way to exercise the POST, PUT, and DELETE routes without writing a client.

API

All endpoints operate on the clients resource.

Method	Path	Description	Success	Errors
GET	/clients	Return all clients	200	—
GET	/clients/{client_id}	Return a single client	200	404 if no client with that ID
POST	/clients	Create a client	200	409 if that ID already exists, 422 if the body is malformed
PUT	/clients/{client_id}	Update an existing client	200	404 if no client with that ID, 422 if the body is malformed
DELETE	/clients/{client_id}	Delete a client	200	404 if no client with that ID

Failure cases raise HTTPException, so responses carry a genuine status code rather than a 200 with an error buried in the body. Duplicate primary keys are caught as sqlite3.IntegrityError and translated into a 409 Conflict rather than surfacing as an unhandled 500.

PUT treats the path as authoritative for identity: the id in the request body is ignored, since the URL is what identifies the resource being updated.

Example
curl -X POST http://127.0.0.1:8000/clients \
  -H "Content-Type: application/json" \
  -d '{"id": "c3", "name": "Amira Haddad", "email": "amira@example.com"}'
Known limitations

The deployed instance runs on Render's free tier, which has two consequences worth stating plainly:

Cold starts. The service spins down after a period of inactivity. The first request after that takes roughly 30–60 seconds while it restarts. Subsequent requests are fast.

Ephemeral storage. The free tier's filesystem does not persist across restarts, so the SQLite file is recreated each time the service comes back up. Records added through the live API are lost; the seed data returns. This is a property of the hosting tier rather than the application — moving the data layer to Postgres, which Render offers as a managed service, would resolve it.

Data model

The clients table:

Column	Type	Constraints
id	TEXT	PRIMARY KEY
name	TEXT	NOT NULL
email	TEXT	NOT NULL

Request and response bodies are validated by a Pydantic model, so malformed payloads are rejected at the boundary with a 422 before reaching the database.

Project structure
photo-crm/
├── main.py            # FastAPI app and route handlers
├── db.py              # Connection helper, schema creation, seed data
├── requirements.txt
├── .gitignore
└── README.md

db.py defines get_connection() and init_db() and executes nothing at import time. Each request opens a connection through get_connection(), which sets row_factory to sqlite3.Row so rows convert straight to dictionaries for JSON serialisation.

Roadmap

Shoots. A second table with a client_id foreign key, so each client carries a history of bookings. This is the change that makes the project a CRM rather than a contact list.

AI onboarding questionnaire. A POST /clients/{client_id}/onboarding endpoint that accepts structured answers from a new client — shoot type, aesthetic preferences, budget, timeline — passes them to the Claude API, and stores a generated compatibility brief against the client record. The goal is to give a photographer a usable read on fit and creative direction before the first call, rather than after it.

Business discovery. A longer-term ambition: automatically surface local businesses that are likely to need photography or video work, and score them for fit. This is deliberately out of scope for the current build — it needs the core CRM to be solid first — but it is the direction the project is aimed.

License

MIT