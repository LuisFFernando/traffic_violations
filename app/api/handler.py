from app.core.user_service import UserService
from app.core.traffic_officer_service import TrafficOfficerService
from app.core.traffic_officer_service import ViolationsService
from app.core.vehicle_service import VehicleService


class UserHandler:
    @classmethod
    def create(cls, kwargs: dict):
        return UserService().create(kwargs)

    @classmethod
    def get(cls, kwargs: dict):
        return UserService().get(kwargs)

    @classmethod
    def update(cls, kwargs: dict, user_id: int):
        return UserService().update(user_id, kwargs)

    @classmethod
    def delete(cls, user_id: int):
        return UserService().delete(user_id)


class TrafficOfficerHandler:
    @classmethod
    def create(cls, kwargs: dict):
        return TrafficOfficerService().create(kwargs)

    @classmethod
    def get(cls, kwargs: dict):
        return TrafficOfficerService().get(kwargs)

    @classmethod
    def update(cls, kwargs: dict, officer_id: int):
        return TrafficOfficerService().update(officer_id, kwargs)

    @classmethod
    def delete(cls, nid: int):
        return TrafficOfficerService().delete(nid)


class TrafficViolationsHandler:
    @classmethod
    def create(cls, kwargs: dict, payload_token):
        return ViolationsService().create(kwargs, payload_token.get("officer_id"))

    @classmethod
    def report(cls, params: dict):
        return ViolationsService().violations_reports(params.get("email"))


class VehicleHandler:
    @classmethod
    def create(cls, kwargs: dict, user_id):
        return VehicleService().create(kwargs, user_id)

    @classmethod
    def get(cls, kwargs: dict, user_id: int):
        return VehicleService().get(kwargs, user_id)

    @classmethod
    def update(cls, kwargs: dict, vehicle_id: int, user_id: int):
        return VehicleService().update(vehicle_id, user_id, kwargs)

    @classmethod
    def delete(cls, vehicle_id: int, user_id: int):
        return VehicleService().delete(vehicle_id, user_id)
