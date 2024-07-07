from app.repository.postgres_repository import QueryManager

from app.core.models.model import User
from app.api.serializers.user_serializer import UserDeserializer

from datetime import datetime
import inject


class UserService:
    """."""

    def create(self, kwargs: dict):
        """Create User."""

        try:
            # create user
            _user = QueryManager(User).create(kwargs)
            return UserDeserializer.model_validate(_user).model_dump()

        except Exception as error:
            raise Exception(str(error))

    def get(self, kwargs: dict):
        """Get User"""
        try:
            _instance = QueryManager(User).filter(kwargs)

            if list(_instance):
                rest = [UserDeserializer.model_validate(data).model_dump(exclude_none=True) for data in _instance]

                return {"status": 200, "data": rest, "msg": "OK"}

            return {"status": 404, "data": "User", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": str(error), "msg": "ERROR"}

    def update(self, user_id, kwarg: dict):
        try:
            kwarg["updated_at"] = datetime.utcnow()
            query = {"id": user_id}
            _instance = QueryManager(User).update(query, kwarg)

            if _instance == 1:
                return {"status": 200, "data": "User update successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in update User not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": f"Error in update user {error}", "msg": "ERROR"}

    def delete(self, user_id: dict):
        try:
            data = {"active": False, "updated_at": datetime.utcnow()}
            query = {"id": user_id}
            _instance = QueryManager(User).delete(query, data)

            if _instance == 1:
                return {"status": 200, "data": "User deleted successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in deleting User not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": "Error in deleting User", "msg": "ERROR"}
