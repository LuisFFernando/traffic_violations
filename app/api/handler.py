from app.core.user_service import UserService
from app.core.traffic_officer_service import TrafficOfficerService
from app.core.traffic_officer_service import ViolationsService
from app.core.vehicle_service import VehicleService


class UserHandler:
    @classmethod
    def create(cls, kwargs: dict):
        return UserService(kwargs).create()

    @classmethod
    def get(cls, kwargs: dict):
        return UserService(kwargs).get()

    @classmethod
    def update(cls, kwargs: dict, user_id: int):
        return UserService(kwargs, user_id).update()

    @classmethod
    def delete(cls, user_id: int):
        return UserService(user_id=user_id).delete()


class TrafficOfficerHandler:
    @classmethod
    def create(cls, kwargs: dict):
        return TrafficOfficerService(kwargs).create()

    @classmethod
    def get(cls, kwargs: dict):
        return TrafficOfficerService(kwargs).get()

    @classmethod
    def update(cls, kwargs: dict, officer_id: int):
        return TrafficOfficerService(kwargs, officer_id).update()

    @classmethod
    def delete(cls, nid: int):
        return TrafficOfficerService(officer_id=nid).delete()


class TrafficViolationsHandler:
    @classmethod
    def create(cls, kwargs: dict, payload_token):
        return ViolationsService(kwargs, payload_token.get("officer_id")).create()

    @classmethod
    def report(cls, params: dict):
        return ViolationsService(params=params.get("email")).violations_reports()


class VehicleHandler:
    @classmethod
    def create(cls, kwargs: dict, user_id):
        return VehicleService(kwargs, user_id).create()

    @classmethod
    def get(cls, kwargs: dict, user_id: int):
        return VehicleService(kwargs=kwargs, user_id=user_id).get()

    @classmethod
    def update(cls, kwargs: dict, vehicle_id: int, user_id: int):
        return VehicleService(kwargs, user_id, vehicle_id).update()

    @classmethod
    def delete(cls, vehicle_id: int, user_id: int):
        return VehicleService(user_id=user_id, vehicle_id=vehicle_id).delete()
