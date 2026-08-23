# photo-crm

A lightweight client management API for photographers and videographers, built with FastAPI and SQLite.

Freelance photographers typically track clients across a mix of Instagram DMs, WhatsApp threads, and spreadsheets. This project is a small, self-hosted backend that gives them a single source of truth for client records, with a clean REST interface that a web or mobile front end can sit on top of.

## Status

In active development. Core client CRUD is implemented and working against a persistent SQLite database. See [Roadmap](#roadmap) for what's next.

## Tech stack

| Layer | Choice |
|---|---|
| Language | Python 3 |
| Web framework | FastAPI |
| Validation | Pydantic |
| Database | SQLite (via the standard-library `sqlite3` module) |
| Server | Uvicorn |
| Docs | Auto-generated OpenAPI / Swagger UI |

No ORM. Queries are written directly against `sqlite3` with parameterised statements, which keeps the data layer transparent and dependency-light.

## Getting started

### Prerequisites

- Python 3.9 or newer
- `git`

### Setup

```
git clone git@github.com:khatrihassan/photo-crm.git
cd photo-crm

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Initialise the database

`db.py` creates the SQLite file and the `clients` table, and seeds a couple of sample records:

```
python db.py
```

This only needs to be run once. The database file is excluded from version control.

### Run the server

```
uvicorn main:app --reload
```

The API is then available at `http://127.0.0.1:8000`.

Interactive documentation is served at `http://127.0.0.1:8000/docs`, which is the easiest way to exercise the `POST`, `PUT`, and `DELETE` routes without writing a client.

## API

All endpoints operate on the `clients` resource.

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| `GET` | `/clients` | Return all clients | `200` | — |
| `POST` | `/clients` | Create a client | `200` | — |
| `PUT` | `/clients/{client_id}` | Update an existing client | `200` | `404` if no client with that ID |
| `DELETE` | `/clients/{client_id}` | Delete a client | `200` | `404` if no client with that ID |

Missing records raise `HTTPException`, so the response carries a genuine `404` status rather than a `200` with an error body in it.

### Example

```
curl -X POST http://127.0.0.1:8000/clients \
  -H "Content-Type: application/json" \
  -d '{"id": "c3", "name": "Amira Haddad", "email": "amira@example.com"}'
```

## Data model

The `clients` table:

| Column | Type | Constraints |
|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` |
| `name` | `TEXT` | `NOT NULL` |
| `email` | `TEXT` | `NOT NULL` |

Request and response bodies are validated by a Pydantic model, so malformed payloads are rejected at the boundary with a `422` before reaching the database.

## Project structure

```
photo-crm/
├── main.py            # FastAPI app and route handlers
├── db.py              # Schema creation and seed data
├── requirements.txt
├── .gitignore
└── README.md
```

Each request opens a connection through a `get_connection()` helper with `row_factory` set to `sqlite3.Row`, which allows rows to be converted straight to dictionaries for JSON serialisation.

## Roadmap

**Deployment.** Host the API on Render so it is publicly reachable rather than local-only.

**AI onboarding questionnaire.** A `POST /clients/{client_id}/onboarding` endpoint that accepts structured answers from a new client — shoot type, aesthetic preferences, budget, timeline — passes them to the Claude API, and stores a generated compatibility brief against the client record. The goal is to give a photographer a usable read on fit and creative direction before the first call, rather than after it.

**Business discovery.** A longer-term ambition: automatically surface local businesses that are likely to need photography or video work, and score them for fit. This is deliberately out of scope for the current build — it needs the core CRM to be solid first — but it is the direction the project is aimed.

## License

MIT
