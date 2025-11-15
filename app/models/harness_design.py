from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class HarnessDesign(Base):
    __tablename__ = "harness_designs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    version = Column(Integer, nullable=False, default=1)
    design_data = Column(JSON, nullable=False)

    project = relationship("Project", back_populates="harness_designs")
