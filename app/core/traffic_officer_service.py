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
import inject


class TrafficOfficerService:
    """."""

    def __init__(self, kwargs: dict = None, officer_id: int = 0) -> None:
        self.kwargs = kwargs
        self.officer_id = officer_id

    @inject.params(query_manager=QueryManager)
    def create(self, query_manager: QueryManager):
        """Create User."""

        try:
            kwargs = self.hash_password(self.kwargs)

            query_manager.entity = TrafficOfficer
            officer = query_manager.create(kwargs)

            result = TrafficOfficerDeserializer.model_validate(officer).model_dump(exclude_none=True)

            return {"status": 201, "data": result, "msg": "OK"}

        except Exception as error:
            return {"status": 500, "data": f"Error in create traffic officer {error}", "msg": "ERROR"}

    @inject.params(query_manager=QueryManager)
    def get(self, query_manager: QueryManager):
        """Get Traffic Officer"""
        try:
            query_manager.entity = TrafficOfficer
            instance_officer = query_manager.filter(self.kwargs)

            if list(instance_officer):
                rest = [
                    TrafficOfficerDeserializer.model_validate(data).model_dump(exclude_none=True)
                    for data in instance_officer
                ]

                return {"status": 200, "data": rest, "msg": "OK"}

            return {"status": 404, "data": "Traffic Officer not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": str(error), "msg": "ERROR"}

    @inject.params(query_manager=QueryManager)
    def update(self, query_manager: QueryManager):
        try:
            self.kwargs.update(
                {
                    "updated_at": datetime.now(),
                }
            )

            self.kwargs = self.hash_password(self.kwargs)

            query = {"id": self.officer_id}

            query_manager.entity = TrafficOfficer
            instance_officer = query_manager.update(query, self.kwargs)

            if instance_officer == 1:
                return {"status": 200, "data": "Traffic Officer update successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in update traffic officer not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": "Error in update traffic officer", "msg": "ERROR"}

    def hash_password(self, kwargs: dict):
        if kwargs.get("password"):
            kwargs.update({"password": hashed_password(kwargs.get("password"))})

        return kwargs

    @inject.params(query_manager=QueryManager)
    def delete(self, query_manager: QueryManager):
        try:
            data = {"active": False, "updated_at": datetime.now()}
            query = {"id": self.officer_id}

            query_manager.entity = TrafficOfficer
            instance_officer = query_manager.delete(query, data)

            if instance_officer == 1:
                return {"status": 200, "data": "Traffic Officer deleted successfully", "msg": "OK"}

            return {"status": 404, "data": "Error in deleting traffic officer not found", "msg": "ERROR"}

        except Exception as error:
            return {"status": 500, "data": "Error in deleting traffic officer", "msg": "ERROR"}


class ViolationsService:
    def __init__(self, kwargs: dict = {}, params: str = None):
        self.kwargs = kwargs
        self.params = params

    @inject.params(query_manager=QueryManager)
    def create(self, query_manager: QueryManager):
        """Create User."""

        try:
            self.kwargs.update(
                {"vehicle_id": self.exist_vehicle(self.kwargs.get("placa_patente")), "traffic_officer_id": self.params}
            )

            query_manager.entity = Violations
            instance_officer = query_manager.create(self.kwargs)

            result = ViolationsDeserializer.model_validate(instance_officer).model_dump(exclude_none=True)

            return {"status": 200, "data": result, "msg": "OK"}

        except Exception as error:
            return {"status": 404, "data": str(error), "msg": "ERROR"}

    def exist_vehicle(self, placa_patente):
        """Valida que exista el vehiculo si la respuesta es True retorna el vehicle_id,
        si es false retorna una exceptions
        """
        try:
            _vehicle = QueryManager(Vehicle).get({"placa_patente": placa_patente})
            return _vehicle.id
        except Exception:
            raise Exception("Number Plate not found.")

    @inject.params(query_manager=QueryManager)
    def violations_reports(self, query_manager=QueryManager):
        try:
            query_manager.entity = Violations
            instance_officer = query_manager.custom_query(self.params, Vehicle, User)

            result = [
                VehicleViolationsDeserializer.model_validate(data).model_dump(exclude_none=True)
                for data in instance_officer
            ]

            return {"status": 200, "data": result, "msg": "OK"}
        except Exception as error:
            return {"status": 500, "data": str(error), "msg": "ERROR"}
