from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from db_setup import Base

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, unique=True, nullable=False)
    data = Column(JSONB)
    data_sources = relationship('DataSource', back_populates='project', cascade='all, delete-orphan')

class DataSource(Base):
    __tablename__ = 'data_sources'

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    tags = Column(JSONB)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='data_sources')

Project.data_sources = relationship('DataSource', order_by=DataSource.id, back_populates='project')

