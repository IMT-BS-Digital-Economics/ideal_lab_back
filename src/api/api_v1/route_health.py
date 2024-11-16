#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 16/11/2024
    About: 

"""

from fastapi import APIRouter, HTTPException, status, Depends, Response

router_health = APIRouter()

@router_health.get('/')
async def health_status():
    return {"detail": "Ok"}