from abc import ABC
from abc import abstractmethod


class InterfaceCrud(ABC):
    """Docstring"""

    @abstractmethod
    def get(self):
        return

    @abstractmethod
    def filter(self):
        return

    @abstractmethod
    def create(self):
        return

    @abstractmethod
    def delete(self):
        return

    @abstractmethod
    def update(self):
        return
