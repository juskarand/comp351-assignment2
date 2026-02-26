# Assignment 2 - LEGO Inventory Items API

## FastAPI + SQLAlchemy + SQLite)

## Requirements
- Python 3.9+
- pip
- class virtual environment

## Project Structure

- main.py
- database.py
- models.py
- schemas.py
- requirements.txt
- README.md
- .gitignore

.gitignore must include *.db

## Setup (Mac)
```bash
from the assignment2 folder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Running the API
uvicorn main:app --reload
Open http://127.0.0.1:8000/docs


Try out and execute the following Endpoints:

POST /items → 201 Created (Create an item)

GET /items → 200 OK (List items + filters)

GET /items/{item_id} → 200 OK / 404 Not Found (Get one item)

PATCH /items/{item_id} → 200 OK / 404 Not Found (Partial update)

DELETE /items/{item_id} → 204 No Content / 404 Not Found (Delete item)


Sample Request Body used for POST/items
{
  "sku": "LEGO-75331",
  "name": "UCS Razor Crest",
  "description": "Star Wars set",
  "quantity": 3,
  "unit_price": 699.99,
  "reorder_level": 2,
  "location": "Shelf A3",
  "is_active": true
}

## Testing Evidence based on Sample Request Body (Terminal Output)

Below is terminal output showing CRUD testing via Swagger UI (`/docs`) and the resulting HTTP status codes:

uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/juskarandhanjal/assignment2']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [906] using WatchFiles
INFO:     Started server process [908]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:61609 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:61609 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:61622 - "POST /items HTTP/1.1" 201 Created
INFO:     127.0.0.1:61629 - "GET /items?skip=0&limit=50 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61634 - "GET /items/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61635 - "PATCH /items/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61637 - "DELETE /items/1 HTTP/1.1" 204 No Content
INFO:     127.0.0.1:61637 - "DELETE /items/1 HTTP/1.1" 404 Not Found
