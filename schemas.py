from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

class PlaceBase(BaseModel):
    external_id: int
    notes: Optional[str] = None
    is_visited: bool = False

class PlaceCreate(PlaceBase):
    pass

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    places: List[PlaceCreate] = []

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None

class PlaceResponse(PlaceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    is_completed: bool
    places: List[PlaceBase]
