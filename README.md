# Student Management System — REST API (Flask + SQLite)

## Tech Stack
Python, Flask, SQL (SQLite), JSON, Postman

## Endpoints
- `GET /students` — list all
- `GET /students/<id>` — get by id
- `POST /students` — create (JSON: {"name":"Sanjay","age":20,"grade":"A"})
- `PUT /students/<id>` — update (same JSON shape)
- `DELETE /students/<id>` — delete by id

## Run locally
```bash
pip install -r requirements.txt
python app.py
