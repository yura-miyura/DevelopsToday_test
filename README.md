# Travel Project Management API

A FastAPI-based CRUD application designed for travelers to plan their trips and collect desired places to visit using the **Art Institute of Chicago API**.

## Features

- **Travel Projects**: Create, list, update, and delete travel plans.
- **Place Collection**: Add up to 10 places per project, validated against the Art Institute of Chicago's official database.
- **Progress Tracking**: Add notes to places and mark them as visited.
- **Smart Completion**: Projects are automatically marked as "Completed" when all their places are visited.
- **Data Integrity**: Prevents duplicate places in the same project and protects projects from deletion if they contain visited locations.

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (SQLAlchemy 2.0 ORM)
- **HTTP Client**: HTTPX (for async third-party API validation)
- **Environment Management**: [uv](https://github.com/astral-sh/uv)

---

## Setup & Installation

### 1. Prerequisite: Install `uv`

If you don't have `uv` installed, follow the [official guide](https://github.com/astral-sh/uv#installation).

### 2. Setup Environment

Clone the repository and run the following command to create a virtual environment and install all dependencies:
```bash
uv sync
```

### 3. Run the Application

Start the development server:
```bash
uv run uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

---

## API Documentation

FastAPI provides interactive documentation out of the box:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Best for interactive testing)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI JSON**: `http://127.0.0.1:8000/openapi.json` (Import this into **Postman**)

---

## Example Requests (cURL)

### 1. Create a New Project

```bash
curl -X 'POST' 'http://127.0.0.1:8000/projects/' \
-H 'Content-Type: application/json' \
-d '{
  "name": "Trip to Chicago Museums",
  "description": "A weekend exploring the Art Institute",
  "start_date": "2026-05-15",
  "places": [
    { "external_id": 22, "notes": "Check out the Villa Pamphili views" }
  ]
}'
```

### 2. Add a Place to an Existing Project

```bash
curl -X 'POST' 'http://127.0.0.1:8000/projects/1/places/' \
-H 'Content-Type: application/json' \
-d '{
  "external_id": 16568,
  "notes": "Must see this ancient artifact"
}'
```

### 3. Mark a Place as Visited

```bash
curl -X 'PATCH' 'http://127.0.0.1:8000/projects/1/places/1?visited=true'
```

### 4. Update Project Info

```bash
curl -X 'PUT' 'http://127.0.0.1:8000/projects/1' \
-H 'Content-Type: application/json' \
-d '{"name": "Updated Trip Name"}'
```

---

## Business Rules & Constraints

1. **API Validation**: Every `external_id` is validated against the [Art Institute of Chicago API](https://api.artic.edu/docs/). Invalid IDs will return a `400 Bad Request`.
2. **Project Capacity**: A maximum of **10 places** can be added to any single project.
3. **Uniqueness**: The same external place cannot be added to the same project more than once.
4. **Deletion Protection**: A project **cannot be deleted** if any of its places are already marked as "visited".
5. **Project Completion**: A project is automatically marked as `is_completed: true` only when **all** associated places have been marked as visited. Adding a new place or unmarking a place as visited will revert this status.

---

## Database

The application uses **SQLite** by default (`travel_plans.db`). No additional database setup is required. The tables are automatically created when the application starts for the first time.
