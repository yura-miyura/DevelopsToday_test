from typing import List, Optional
from datetime import date
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    start_date: Mapped[Optional[date]] = mapped_column()
    is_completed: Mapped[bool] = mapped_column(default=False)

    # Relationship using Mapped for type safety
    places: Mapped[List["Place"]] = relationship(
        back_populates="project", cascade="all, delete-orphan", lazy="selectin"
    )


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_id: Mapped[int] = mapped_column(index=True)
    notes: Mapped[Optional[str]] = mapped_column(String(1000))
    is_visited: Mapped[bool] = mapped_column(default=False)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="places")
