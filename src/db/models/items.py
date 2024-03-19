#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 21/06/2022
    About: 

"""

from sqlalchemy import Column, ForeignKey, Integer, String, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList


from src.db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_status = Column(Integer, index=True)
    start_time = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    path = Column(String, index=True)
    arguments = Column(MutableList.as_mutable(PickleType), default=[], index=True)
    time_to_start = Column(String, index=True)
    process_id = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    reports = relationship("Report", back_populates="item_owner")
