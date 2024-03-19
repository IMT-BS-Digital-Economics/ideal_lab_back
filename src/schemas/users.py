#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 21/06/2022
    About: 

"""

from typing import Union

from pydantic import BaseModel

from src.schemas.items import Item


class UserBase(BaseModel):
    email: Union[str, None] = None
    username: Union[str, None] = None


class UserCreate(UserBase):
    password: str
    validation_token: Union[str, None] = None


class UserResetPass(BaseModel):
    password: Union[str, None] = None
    confirm_password: Union[str, None] = None


class UserMail(BaseModel):
    email: str


class UpdateUserRole(BaseModel):
    username: Union[str, None] = None
    role: Union[str, None] = None


class SessionData(BaseModel):
    username: str


class User(UserBase):
    id: Union[int, None] = None
    is_verified: Union[bool, None] = None
    username: Union[str, None] = None
    items: list[Item] = []
    role: Union[str, None] = None

    class Config:
        orm_mode = True


class UserList(User):
    users: Union[list, None]