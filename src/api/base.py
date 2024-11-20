#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 21/06/2022
    About: 

"""

from fastapi import APIRouter

from src.api.api_v1 import route_items
from src.api.api_v1 import route_auth
from src.api.api_v1 import route_users
from src.api.api_v1 import route_repositories
from src.api.api_v1 import route_admin
from src.api.api_v1 import route_projects

api_router = APIRouter()
api_router.include_router(route_auth.router_auth, prefix="/auth", tags=["auth"])
api_router.include_router(route_users.router_user, prefix="/user", tags=["user"])
api_router.include_router(route_items.router_items, prefix="/items", tags=["items"])
api_router.include_router(route_repositories.router_repositories, prefix="/repositories", tags=["repositories"])
api_router.include_router(route_admin.router_admin, prefix="/admin", tags=["admin"])
api_router.include_router(route_projects.router_project, prefix='/projects', tags=["projects"])