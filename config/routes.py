from fastapi import APIRouter
from app.api.views import user_views
from app.api.views import traffic_officer_views
from app.api.views import vehicle_views


urls = APIRouter()

urls.include_router(user_views.router, prefix="/api/v1")
urls.include_router(traffic_officer_views.router, prefix="/api/v1")
urls.include_router(vehicle_views.router, prefix="/api/v1")
