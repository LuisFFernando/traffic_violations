import inject
from datetime import datetime
from app.repository.postgres_repository import QueryManager
from app.core.models.model import User
from app.api.serializers.user_serializer import UserDeserializer


class UserService:
    """."""

    def __init__(self, kwargs: dict = None, user_id: int = None) -> None:
        self.kwargs = kwargs
        self.user_id = user_id

    @inject.params(query_manager=QueryManager)
    def create(self, query_manager: QueryManager):
        """Create User."""

        try:
            query_manager.entity = User
            user_instance = query_manager.create(self.kwargs)

            return UserDeserializer.model_validate(user_instance).model_dump()

        except Exception as error:
            raise Exception(str(error))

    @inject.params(query_manager=QueryManager)
    def get(self, query_manager: QueryManager):
        """Get User"""
        try:
            query_manager.entity = User
            user_instance = query_manager.filter(self.kwargs)

            if list(user_instance):
                rest = [UserDeserializer.model_validate(data).model_dump(exclude_none=True) for data in user_instance]

                return {"status": 200, "data": rest, "msg": "OK"}

            return {"status": 404, "data": "User", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": str(error), "msg": "ERROR"}

    @inject.params(query_manager=QueryManager)
    def update(self, query_manager: QueryManager):
        try:
            self.kwargs.update({"updated_at": datetime.now()})
            query = {"id": self.user_id}

            query_manager.entity = User
            user_instance = query_manager.update(query, self.kwargs)

            if user_instance == 1:
                return {"status": 200, "data": "User update successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in update User not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": f"Error in update user {error}", "msg": "ERROR"}

    @inject.params(query_manager=QueryManager)
    def delete(self, query_manager: QueryManager):
        try:
            data = {"active": False, "updated_at": datetime.now()}
            query = {"id": self.user_id}

            query_manager.entity = User
            user_instance = query_manager.delete(query, data)

            if user_instance == 1:
                return {"status": 200, "data": "User deleted successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in deleting User not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": "Error in deleting User", "msg": "ERROR"}
