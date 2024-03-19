#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(String, index=True)
    traceback = Column(String, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))

    item_owner = relationship("Item", back_populates="reports")
