#!/usr/bin/env python3

"""
    ideal_lab_back

    Author: bricetoffolon
    Created on: 19/03/2024
    About: What will be stored in the database

"""

from sqlalchemy import Column, ForeignKey, Integer, String, PickleType, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList

from src.db.database import Base

from datetime import datetime


class Project(Base):
    __tablename__ = "projects"

    unique_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, index=True)
    repository = Column(String, index=True)
    executable = Column(String, index=True)
    arguments = Column(MutableList.as_mutable(PickleType), default=[])
    start_time = Column(String, index=True, default=datetime.now().strftime('%H:%M'))
    auto_launch = Column(Boolean, index=True, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")