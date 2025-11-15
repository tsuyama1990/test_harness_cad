from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class HarnessDesign(Base):
    __tablename__ = "harness_designs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    design_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="harness_designs")
