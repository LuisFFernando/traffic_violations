from fastapi import APIRouter, Request, Depends

from sentry_sdk import capture_exception
from starlette import status
from starlette.responses import JSONResponse

# serializers
from app.api.serializers.user_serializer import CreateUserSerializer
from app.api.serializers.user_serializer import ParamUserGetSerializer
from app.api.serializers.user_serializer import UpdateUserSerializer

# handlers
from app.api.handler import UserHandler

# utils
from app.core.utils import oauth2_scheme
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/api/templates")

router = APIRouter()


@router.get("/admin")
def admin(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/create_user")
def create_user(request: Request):
    return templates.TemplateResponse("register_user.html", {"request": request})


@router.get("/list_user")
def list_user(request: Request):
    return templates.TemplateResponse("list_user.html", {"request": request})


@router.get("/update_user/{user_id}")
def update_user(request: Request):
    return templates.TemplateResponse("update_user.html", {"request": request})


@router.post("/user", tags=["User"])
def create_user(request: CreateUserSerializer):
    """Create User."""

    try:
        handler_create = UserHandler.create(request.model_dump(exclude_none=True))
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(success=True, code=0, message="OK", data=handler_create),
        )
    except Exception as e:
        return JSONResponse(dict(error=True, message=str(e)), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.get("/user", tags=["User"])
def get_user(request: Request):
    """Get User by params
    :: Params
        - id
        - nid
        - email
        - phone
        - name
    """

    serializers = ParamUserGetSerializer(**request.query_params).model_dump(exclude_none=True)
    response = UserHandler.get(serializers)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get("msg"), data=response.get("data")),
    )


@router.put("/user/{user_id}", tags=["User"])
def update_user(request: UpdateUserSerializer, user_id: int):
    """ """

    response = UserHandler.update(request.model_dump(exclude_none=True), user_id)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get("msg"), data=response.get("data")),
    )


@router.delete("/user/{user_id}", tags=["User"])
def delete_user(user_id: int):
    """Get User by params
    :: Params
        - nid
    """

    response = UserHandler.delete(user_id)
    return JSONResponse(
        status_code=response.get("status"),
        content=dict(success=True, message=response.get("msg"), data=response.get("data")),
    )
