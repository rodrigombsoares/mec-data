from abc import ABC, abstractmethod


class DataLakeBase(ABC):
    @abstractmethod
    def store():
        pass
