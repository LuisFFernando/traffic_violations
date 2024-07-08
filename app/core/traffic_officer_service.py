from app.repository.postgres_repository import QueryManager

from app.core.models.model import TrafficOfficer
from app.core.models.model import Violations
from app.core.models.model import Vehicle
from app.core.models.model import User
from app.api.serializers.traffic_officer_serializer import TrafficOfficerDeserializer
from app.api.serializers.traffic_officer_serializer import ViolationsDeserializer
from app.api.serializers.traffic_officer_serializer import VehicleViolationsDeserializer

from datetime import datetime
from app.core.utils import hashed_password


class TrafficOfficerService:
    """."""

    def create(self, kwargs: dict):
        """Create User."""

        try:
            kwarg = self.hash_password(kwarg)

            _officer = QueryManager(TrafficOfficer).create(kwargs)
            result = TrafficOfficerDeserializer.model_validate(_officer).model_dump(exclude_none=True)

            return {"status": 201, "data": result, "msg": "OK"}
        except Exception as error:
            return {"status": 500, "data": f"Error in create traffic officer {error}", "msg": "ERROR"}

    def get(self, kwargs: dict):
        """Get Traffic Officer"""
        try:
            _instance = QueryManager(TrafficOfficer).filter(kwargs)

            if list(_instance):
                rest = [
                    TrafficOfficerDeserializer.model_validate(data).model_dump(exclude_none=True) for data in _instance
                ]

                return {"status": 200, "data": rest, "msg": "OK"}

            return {"status": 404, "data": "Traffic Officer not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": str(error), "msg": "ERROR"}

    def update(self, vehicle_id, kwarg: dict):
        try:
            kwarg.update({"updated_at": datetime.now()})
            
            kwarg = self.hash_password(kwarg)
            
            query = {"id": vehicle_id}
            _instance = QueryManager(TrafficOfficer).update(query, kwarg)

            if _instance == 1:
                return {"status": 200, "data": "Traffic Officer update successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in update traffic officer not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": "Error in update traffic officer", "msg": "ERROR"}
        
    def hash_password(self, kwargs:dict):
        
        if kwargs.get("password"):
            kwargs.update({"password": hashed_password(kwargs.get("password"))})
            
        return kwargs

    def delete(self, nid: dict):
        try:
            data = {"active": False, "updated_at": datetime.utcnow()}
            query = {"id": nid}
            _instance = QueryManager(TrafficOfficer).delete(query, data)

            if _instance == 1:
                return {"status": 200, "data": "Traffic Officer deleted successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in deleting traffic officer not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": "Error in deleting traffic officer", "msg": "ERROR"}


class ViolationsService:
    def create(self, kwargs: dict, officer_id):
        """Create User."""

        try:
            kwargs["vehicle_id"] = self.exist_vehicle(kwargs.get("placa_patente"))
            kwargs["traffic_officer_id"] = officer_id
            _traffic_violations = QueryManager(Violations).create(kwargs)
            result = ViolationsDeserializer.model_validate(_traffic_violations).model_dump(exclude_none=True)

            return {"status": 200, "data": result, "msg": "OK"}

        except Exception as error:
            return {"status": 404, "data": str(error), "msg": "ERROR"}

    def exist_vehicle(self, placa_patente):
        try:
            _vehicle = QueryManager(Vehicle).get({"placa_patente": placa_patente})
            return _vehicle.id
        except Exception:
            raise Exception("Number Plate not found.")

    def violations_reports(self, email: str):
        try:
            _traffic_violations = QueryManager(Violations).custom_query(email, Vehicle, User)

            result = [
                VehicleViolationsDeserializer.model_validate(data).model_dump(exclude_none=True)
                for data in _traffic_violations
            ]

            return {"status": 200, "data": result, "msg": "OK"}
        except Exception as error:
            return {"status": 500, "data": str(error), "msg": "ERROR"}
