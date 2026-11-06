from abc import ABC, abstractmethod


class Vendible(ABC):

    @abstractmethod
    def calcular_precio_final(self):
        pass
