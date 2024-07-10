from app.repository.postgres_repository import QueryManager

from app.core.models.model import Vehicle
from app.api.serializers.vehicle_serializer import VehicleDeserializer
from datetime import datetime
import inject


class VehicleService:
    """."""

    def __init__(self, kwargs: dict = None, user_id: int = 0, vehicle_id: int = 0) -> None:
        self.kwargs = kwargs
        self.user_id = user_id
        self.vehicle_id = vehicle_id

    @inject.params(query_manager=QueryManager)
    def create(self, query_manager: QueryManager):
        """Create User."""

        try:
            self.kwargs.update({"user_id": self.user_id})

            query_manager.entity = Vehicle
            vehicle_instance = query_manager.create(self.kwargs)

            result = VehicleDeserializer.model_validate(vehicle_instance).model_dump(exclude_none=True)

            return {"status": 201, "data": result, "msg": "OK"}
        except Exception as error:
            return {"status": 500, "data": f"Vehicle already exist {error}", "msg": "ERROR"}

    @inject.params(query_manager=QueryManager)
    def get(self, query_manager: QueryManager):
        """Get User"""
        try:
            self.kwargs.update({"user_id": self.user_id})

            query_manager.entity = Vehicle
            vehicle_instance = query_manager.filter(self.kwargs)

            if list(vehicle_instance):
                rest = [
                    VehicleDeserializer.model_validate(data).model_dump(exclude_none=True) for data in vehicle_instance
                ]

                return {"status": 200, "data": rest, "msg": "OK"}

            return {"status": 404, "data": "Vehicle not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": str(error), "msg": "ERROR"}

    @inject.params(query_manager=QueryManager)
    def update(self, query_manager: QueryManager):
        try:
            self.kwargs.update({"updated_at": datetime.now()})

            query = {"id": self.vehicle_id, "user_id": self.user_id}

            query_manager.entity = Vehicle
            vehicle_instance = query_manager.update(query, self.kwargs)

            if vehicle_instance == 1:
                return {"status": 200, "data": "Vehicle update successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in update Vehicle not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": f"Error in update Vehicle {error}", "msg": "ERROR"}

    @inject.params(query_manager=QueryManager)
    def delete(self, query_manager: QueryManager):
        try:
            data = {"active": False, "updated_at": datetime.now()}
            query = {"id": self.vehicle_id, "user_id": self.user_id}

            query_manager.entity = Vehicle
            vehicle_instance = query_manager.delete(query, data)

            if vehicle_instance == 1:
                return {"status": 200, "data": "Vehicle deleted successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in deleting Vehicle not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": "Error in deleting Vehicle", "msg": "ERROR"}
