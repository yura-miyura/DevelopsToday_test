from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
import models
import schemas
import services
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/projects/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # 1. Enforce max 10 places limit
    if len(project_in.places) > 10:
        raise HTTPException(status_code=400, detail="A project can have a maximum of 10 places.")

    # 2. Check for duplicate external_ids in the request itself
    external_ids = [p.external_id for p in project_in.places]
    if len(external_ids) != len(set(external_ids)):
        raise HTTPException(status_code=400, detail="Duplicate external IDs are not allowed in a project.")

    # 3. Create Project
    new_project = models.Project(
        name=project_in.name,
        description=project_in.description,
        start_date=project_in.start_date
    )
    db.add(new_project)
    db.flush()

    # 4. Validate and Add Places
    for p in project_in.places:
        await services.validate_artwork_id(p.external_id)
        db_place = models.Place(**p.model_dump(), project_id=new_project.id)
        db.add(db_place)

    db.commit()
    db.refresh(new_project)
    return new_project

@app.get("/projects/", response_model=List[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    result = db.execute(select(models.Project)).scalars().all()
    return result

@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=schemas.ProjectResponse)
def update_project(project_id: int, project_update: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project_update.name is not None:
        project.name = project_update.name
    if project_update.description is not None:
        project.description = project_update.description
    if project_update.start_date is not None:
        project.start_date = project_update.start_date

    db.commit()
    db.refresh(project)
    return project

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if any(place.is_visited for place in project.places):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete project because some places have already been visited."
        )

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

@app.post("/projects/{project_id}/places/", response_model=schemas.PlaceResponse, status_code=status.HTTP_201_CREATED)
async def add_place_to_project(project_id: int, place_in: schemas.PlaceCreate, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if len(project.places) >= 10:
        raise HTTPException(status_code=400, detail="A project can have a maximum of 10 places.")

    # Business Rule: Prevent adding same external place twice
    if any(p.external_id == place_in.external_id for p in project.places):
        raise HTTPException(status_code=400, detail="Place already exists in this project.")

    await services.validate_artwork_id(place_in.external_id)
    db_place = models.Place(**place_in.model_dump(), project_id=project_id)
    db.add(db_place)

    # If a new place is added, the project might no longer be completed
    project.is_completed = False

    db.commit()
    db.refresh(db_place)
    return db_place

@app.get("/projects/{project_id}/places/", response_model=List[schemas.PlaceResponse])
def list_project_places(project_id: int, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.places

@app.get("/projects/{project_id}/places/{place_id}", response_model=schemas.PlaceResponse)
def get_place(project_id: int, place_id: int, db: Session = Depends(get_db)):
    stmt = select(models.Place).where(models.Place.id == place_id, models.Place.project_id == project_id)
    place = db.execute(stmt).scalar_one_or_none()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found in this project")
    return place

@app.patch("/projects/{project_id}/places/{place_id}")
def update_place_status(project_id: int, place_id: int, note_update: str = None, visited: bool = None, db: Session = Depends(get_db)):
    stmt = select(models.Place).where(models.Place.id == place_id, models.Place.project_id == project_id)
    place = db.execute(stmt).scalar_one_or_none()

    if not place:
        raise HTTPException(status_code=404, detail="Place not found in this project")

    if note_update is not None:
        place.notes = note_update
    if visited is not None:
        place.is_visited = visited

    db.commit()

    # Business Rule: Project completed if all places visited, else not completed
    project = db.get(models.Project, project_id)
    project.is_completed = all(p.is_visited for p in project.places)
    db.commit()

    return {"message": "Place updated"}
