from sqlalchemy import Column, Integer, String

from app.db.base import Base


class ComponentCategory(Base):
    __tablename__ = "component_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
