from sqlalchemy.exc import NoResultFound, IntegrityError
from app.repository.crud_interface import InterfaceCrud
from config.postgres_conection import session
from typing import Optional, TypeVar

T = TypeVar("T", bound=object)


class QueryManager(InterfaceCrud):
    """ """

    def __init__(self, entity: Optional[T] = None) -> None:
        self.entity = entity

    def get(self, kwargs):
        """Return one Object."""
        try:
            _instance = session.query(self.entity).filter_by(**kwargs).one()
            return _instance

        except NoResultFound:
            session.rollback()
            raise Exception("NoResultFound")

        except Exception as error:
            session.rollback()
            raise Exception(error)

    def filter(self, kwargs):
        try:
            _instance = session.query(self.entity).filter_by(**kwargs)
            return _instance

        except Exception as error:
            session.rollback()
            raise Exception(error)

    def delete(self, query: dict, data: dict):
        try:
            _instance = session.query(self.entity).filter_by(**query).update(data)
            session.commit()
            return _instance
        except Exception as error:
            session.rollback()
            raise Exception(error)

    def create(self, kwargs):
        try:
            _instance = self.entity(**kwargs)
            session.add(_instance)
            session.commit()

            return _instance

        except IntegrityError as error:
            session.rollback()
            raise Exception(str(error))

        except Exception as e:
            session.rollback()
            raise Exception(f"Error DB {str(e)}")

    def update(self, query, data):
        """."""
        try:
            _instance = session.query(self.entity).filter_by(**query).update(data)
            session.commit()
            return _instance
        except Exception as error:
            message = error.args
            session.rollback()
            raise Exception(message)

    def custom_query(self, email, first_params, seconds_params):
        """."""
        try:
            _instance = (
                session.query(first_params)
                .join(seconds_params)
                .filter(seconds_params.email == email, first_params.violations)
                .all()
            )
            return _instance
        except Exception as error:
            session.rollback()
            raise Exception(error)
