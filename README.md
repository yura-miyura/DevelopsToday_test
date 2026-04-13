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

## API Endpoints Reference

| Category | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Project** | `POST` | `/projects/` | Create a new travel project. |
| **Project** | `GET` | `/projects/` | List all travel projects. |
| **Project** | `GET` | `/projects/{id}` | Get a single travel project. |
| **Project** | `PUT` | `/projects/{id}` | Update project info (Name, Description, Date). |
| **Project** | `DELETE` | `/projects/{id}` | Remove a project (forbidden if any place is visited). |
| **Place** | `POST` | `/projects/{id}/places/` | Add a new place to an existing project. |
| **Place** | `GET` | `/projects/{id}/places/` | List all places within a specific project. |
| **Place** | `GET` | `/projects/{id}/places/{place_id}` | Get details of a single place in a project. |
| **Place** | `PATCH` | `/projects/{id}/places/{place_id}` | Update place notes or mark as visited. |

---

## Usage Examples

### 1. Create a New Project

**Request:** `POST /projects/`

```json
{
  "name": "Trip to Chicago Art Museums",
  "description": "A weekend exploring world-class art",
  "start_date": "2026-05-15",
  "places": [
    { "external_id": 22, "notes": "Villa Pamphili view" }
  ]
}
```

### 2. Add a Place to a Project

**Request:** `POST /projects/1/places/`

```json
{
  "external_id": 16568,
  "notes": "Ancient artifact collection"
}
```

### 3. Mark a Place as Visited

**Request:** `PATCH /projects/1/places/1?visited=true`
*Optional: `note_update` can also be passed as a query parameter.*

### 4. Update Project Info

**Request:** `PUT /projects/1`

```json
{
  "name": "Updated Trip Name",
  "start_date": "2026-06-01"
}
```

---

## Setup & Installation

### 1. Prerequisite: Install `uv`

If you don't have `uv` installed, follow the [official guide](https://github.com/astral-sh/uv#installation).

### 2. Setup Environment

```bash
uv sync
```

### 3. Run the Application

```bash
uv run uvicorn main:app --reload
```
Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Business Rules

1. **API Validation**: Every `external_id` is verified against the [Art Institute of Chicago API](https://api.artic.edu/docs/).
2. **Project Capacity**: A maximum of **10 places** per project.
3. **Uniqueness**: Duplicate `external_id` within the same project is forbidden.
4. **Deletion Rule**: A project with **any** visited place cannot be deleted.
5. **Auto-Completion**: Project status becomes `is_completed: true` only when **all** its places are visited.

---

## Database
Uses **SQLite** (`travel_plans.db`). Tables are auto-created on the first run.
