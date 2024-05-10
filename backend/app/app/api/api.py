from fastapi import APIRouter
from .endpoints import job_endpoints

api_router = APIRouter()

api_router.include_router(job_endpoints.router, tags=["Jobs"])