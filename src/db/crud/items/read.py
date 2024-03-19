#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 11/07/2022
    About: 

"""

from sqlalchemy.orm import Session

from src.db.models import Item


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def get_items_by_title(db: Session, title: str, owner_id: int) -> Item:
    return db.query(Item).filter(Item.title == title, Item.owner_id == owner_id).first()


def get_items_by_id(db: Session, id: str, owner_id: int) -> Item:
    return db.query(Item).filter(Item.id == id, Item.owner_id == owner_id).first()