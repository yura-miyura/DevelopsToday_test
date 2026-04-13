# Travel Project Management API

A robust FastAPI-based CRUD application designed for travelers to plan their trips and collect desired places to visit using the Art Institute of Chicago API.

---

## Features

- **Travel Projects**: Full CRUD lifecycle for travel plans.
- **Third-Party Integration**: Real-time validation of places against the Art Institute of Chicago API.
- **Advanced Validations**: 
  - Enforced limit of 10 places per project.
  - Prevention of duplicate places within a single project.
  - Deletion protection for projects with visited locations.
- **Smart Logic**: Automatic calculation of project completion status based on visited places.
- **Fully Typed**: Comprehensive Python type hints for better stability and IDE support.
- **Automated Testing**: Complete test suite with API mocking for reliable verification.

---

## Tech Stack

- **Framework**: FastAPI (Python 3.14+)
- **Database**: SQLite with SQLAlchemy 2.0 (Asynchronous ready)
- **HTTP Client**: HTTPX (for external API validation)
- **Environment**: uv (Next-generation Python manager)
- **Testing**: pytest & pytest-asyncio

---

## Project Structure

```text
├── main.py          # API Endpoints & Core Logic
├── models.py        # SQLAlchemy Database Models
├── schemas.py       # Pydantic Request/Response Models
├── services.py      # Third-party API Integration (Art Institute)
├── database.py      # Database Configuration & Session Management
├── test_main.py     # Automated Test Suite (pytest)
├── pyproject.toml   # Project Metadata & Dependencies
└── README.md        # Documentation
```

---

## Setup & Installation

### 1. Install uv
If you don't have uv installed, run:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Run the Application
```bash
uv run uvicorn main:app --reload
```
The API will be live at: http://127.0.0.1:8000

---

## API Documentation

Access the interactive documentation to explore and test the endpoints directly:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## Testing

Run the automated test suite to verify all business rules:
```bash
uv run pytest
```
*Tests utilize an in-memory database and mocked external API responses for speed and isolation.*

---

## Business Rules & Constraints

| Rule | Description |
| :--- | :--- |
| **Place Limit** | Maximum of 10 places per travel project. |
| **Validation** | Every external_id must exist in the Art Institute of Chicago API. |
| **Uniqueness** | Cannot add the same external_id to the same project twice. |
| **Deletion** | Projects with any visited places are locked and cannot be deleted. |
| **Completion** | A project is is_completed: true only when all associated places are visited. |

---

## Example cURL Commands

### Create a Project
```bash
curl -X 'POST' 'http://127.0.0.1:8000/projects/' \
-H 'Content-Type: application/json' \
-d '{"name": "Summer in Chicago", "places": [{"external_id": 22}]}'
```

### Mark a Place as Visited
```bash
curl -X 'PATCH' 'http://127.0.0.1:8000/projects/1/places/1?visited=true'
```

---

## Database
The application uses SQLite (travel_plans.db). No setup is required; the schema is automatically initialized on the first run.
