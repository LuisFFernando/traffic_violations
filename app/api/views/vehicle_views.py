from app.api.handler import VehicleHandler
from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

# serializers
from app.api.serializers.vehicle_serializer import CreateVehicleSerializer
from app.api.serializers.vehicle_serializer import ParamVehicleGetSerializer
from app.api.serializers.vehicle_serializer import UpdateVehicleSerializer

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/api/templates")

# handlers

router = APIRouter()


@router.get("/create_vehicle/{user_id}")
def read_root(request: Request):
    return templates.TemplateResponse("register_vehicle.html", {"request": request})


@router.get("/list_vehicle/{user_id}")
def read_root(request: Request):
    return templates.TemplateResponse("list_vehicle.html", {"request": request})


@router.get("/edit_vehicle/{user_id}")
def read_root(request: Request):
    return templates.TemplateResponse("list_vehicle.html", {"request": request})


@router.get("/update_vehicle/{vehicle_id}/user/{user_id}")
def read_root(request: Request):
    return templates.TemplateResponse("update_vehicle.html", {"request": request})


@router.post("/vehicle/{user_id}", tags=["Vehicle"])
def create_vehicle(request: CreateVehicleSerializer, user_id: int):
    """Create Vehicle."""

    response = VehicleHandler.create(request.model_dump(exclude_none=True), user_id)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get("msg"), data=response.get("data")),
    )


@router.get("/vehicle/{user_id}", tags=["Vehicle"])
def get_vehicle(request: Request, user_id: int):
    """ """
    serializers = ParamVehicleGetSerializer(**request.query_params).model_dump(exclude_none=True)
    response = VehicleHandler.get(serializers, user_id)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get("msg"), data=response.get("data")),
    )


@router.put("/vehicle/{vehicle_id}/user/{user_id}", tags=["Vehicle"])
def update_vehicle(request: UpdateVehicleSerializer, vehicle_id: int, user_id: int):
    """ """
    response = VehicleHandler.update(request.model_dump(exclude_none=True), vehicle_id, user_id)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get("msg"), data=response.get("data")),
    )


@router.delete("/vehicle/{vehicle_id}/user/{user_id}", tags=["Vehicle"])
def delete_vehicle(vehicle_id: int, user_id: int):
    """Delete Vehicle"""

    response = VehicleHandler.delete(vehicle_id, user_id)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get("msg"), data=response.get("data")),
    )
