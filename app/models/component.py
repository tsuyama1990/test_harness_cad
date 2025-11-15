from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    manufacturer_part_number = Column(String, nullable=True)
    symbol_reference = Column(String, nullable=False)
    footprint_reference = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("component_categories.id"), nullable=False)

    category = relationship("ComponentCategory")
