from fastapi import APIRouter, Request, Depends

from starlette import status
from starlette.responses import JSONResponse
from typing import Dict

# serializers
from app.api.serializers.traffic_officer_serializer import CreateTrafficOfficerSerializer
from app.api.serializers.traffic_officer_serializer import CreateTrafficViolationsSerializer
from app.api.serializers.traffic_officer_serializer import ParamGetSerializer
from app.api.serializers.traffic_officer_serializer import ParamGetViolationsSerializer
from app.api.serializers.traffic_officer_serializer import LoginSerializer
from app.api.serializers.traffic_officer_serializer import UpdatedTrafficOfficerSerializer

# handlers
from app.api.handler import TrafficOfficerHandler
from app.api.handler import TrafficViolationsHandler

# utils
from app.core.utils import authenticate_user
from app.core.utils import verify_jwt_token
from app.core.utils import oauth2_scheme

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/api/templates")

router = APIRouter()


###############################################################
# Admin views
###############################################################

@router.get("/create_officer")
def read_root_view(request: Request):
    return templates.TemplateResponse("register_traffic_officer.html", {"request": request})


@router.get("/list_officer")
def list_officer_view(request: Request):
    return templates.TemplateResponse("list_traffic_officer.html", {"request": request})


@router.get("/update_officer/{officer_id}")
def updated_officer_view(request: Request):
    return templates.TemplateResponse("update_traffic_officer.html", {"request": request})


###############################################################
#
###############################################################


@router.post("/login", tags=["Traffic Officer"])
def login(request: LoginSerializer):
    """Login."""

    response = authenticate_user(request.model_dump(exclude_none=True))
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get(
            "msg"), data=response.get("data")),
    )


@router.post("/officer", tags=["Traffic Officer"])
def create_officer(request: CreateTrafficOfficerSerializer):
    """Create officer."""
    response = TrafficOfficerHandler.create(
        request.model_dump(exclude_none=True))
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get(
            "msg"), data=response.get("data")),
    )


@router.get("/officer", tags=["Traffic Officer"])
def get_officer(request: Request):
    """Get officer by params
    :: Params
        - id
        - nid
        - email
        - phone
        - name
    """

    serializers = ParamGetSerializer(**request.query_params).model_dump(exclude_none=True)
    response = TrafficOfficerHandler.get(serializers)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get(
            "msg"), data=response.get("data")),
    )


@router.put("/officer/{officer_id}", tags=["Traffic Officer"])
def update_officer(request: UpdatedTrafficOfficerSerializer, officer_id: int):
    """Update officer """

    response = TrafficOfficerHandler.update(request.model_dump(exclude_none=True), officer_id)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get(
            "msg"), data=response.get("data")),
    )


@router.delete("/officer/{officer_id}", tags=["Traffic Officer"])
def delete_officer(officer_id: int):
    """Delete officer by url params officer_id
    """

    response = TrafficOfficerHandler.delete(officer_id)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get(
            "msg"), data=response.get("data")),
    )


###############################################################
# Traffic Violations
###############################################################


@router.post("/cargar_infraccion", tags=["Traffic Violations"])
def create_traffic_violations(request: CreateTrafficViolationsSerializer, token: str = Depends(oauth2_scheme)):
    """Create_traffic_violations."""

    payload_token = verify_jwt_token(token)
    response = TrafficViolationsHandler.create(
        request.model_dump(exclude_none=True), payload_token)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get(
            "msg"), data=response.get("data")),
    )


@router.get("/generar_informe", tags=["Traffic Violations"])
def violations_report(request: Request):
    """violations report."""
    try:
        serializers = ParamGetViolationsSerializer(
            **request.query_params).model_dump(exclude_none=True)
        response = TrafficViolationsHandler.report(serializers)
        return JSONResponse(
            status_code=response.get("status"),
            content=dict(success=True, message=response.get(
                "msg"), data=response.get("data")),
        )
    except Exception as error:
        return JSONResponse(dict(error=True, message=str(error)), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
