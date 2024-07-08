from app.repository.postgres_repository import QueryManager

from app.core.models.model import Vehicle
from app.api.serializers.vehicle_serializer import VehicleDeserializer
from datetime import datetime


class VehicleService:
    """."""

    def create(self, kwargs: dict, user_id):
        """Create User."""

        try:
            kwargs.update({"user_id": user_id})
            _vehicle = QueryManager(Vehicle).create(kwargs)
            result = VehicleDeserializer.model_validate(_vehicle).model_dump(exclude_none=True)

            return {"status": 201, "data": result, "msg": "OK"}
        except Exception as error:
            return {"status": 500, "data": f"Vehicle already exist {error}", "msg": "ERROR"}

    def get(self, kwargs: dict, user_id: int):
        """Get User"""
        try:
            kwargs.update({"user_id": user_id})
            _instance = QueryManager(Vehicle).filter(kwargs)

            if list(_instance):
                rest = [VehicleDeserializer.model_validate(data).model_dump(exclude_none=True) for data in _instance]

                return {"status": 200, "data": rest, "msg": "OK"}

            return {"status": 404, "data": "Vehicle not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": str(error), "msg": "ERROR"}

    def update(self, vehicle_id, user_id, kwarg: dict):
        try:
            kwarg.update({"updated_at": datetime.now()})
            query = {"id": vehicle_id, "user_id": user_id}
            _instance = QueryManager(Vehicle).update(query, kwarg)

            if _instance == 1:
                return {"status": 200, "data": "Vehicle update successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in update Vehicle not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": f"Error in update Vehicle {error}", "msg": "ERROR"}

    def delete(self, vehicle_id: int, user_id: int):
        try:
            data = {"active": False, "updated_at": datetime.utcnow()}
            query = {"id": vehicle_id, "user_id": user_id}
            _instance = QueryManager(Vehicle).delete(query, data)

            if _instance == 1:
                return {"status": 200, "data": "Vehicle deleted successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in deleting Vehicle not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": "Error in deleting Vehicle", "msg": "ERROR"}
