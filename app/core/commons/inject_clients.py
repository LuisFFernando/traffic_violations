import inject

from app.repository.postgres_repository import QueryManager


def instantiate_and_inject_clients() -> None:
    def configure_injection(binder: inject.Binder):
        binder.bind(QueryManager, QueryManager())

    inject.clear_and_configure(config=configure_injection)
