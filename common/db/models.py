from xmlrpc.client import DateTime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from DT.common.db.db_setup import Base
from datetime import datetime


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    data = Column(JSONB)
    data_sources = relationship('DataSource', back_populates='project', cascade='all, delete-orphan')
    tags = relationship('Tag', back_populates='project', cascade='all, delete-orphan')

class DataSource(Base):
    __tablename__ = 'data_sources'

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    tags = Column(JSONB)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='data_sources')


Project.data_sources = relationship('DataSource', order_by=DataSource.id, back_populates='project')


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    tag_name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='tags')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


Project.tags = relationship('Tag', back_populates='project')
