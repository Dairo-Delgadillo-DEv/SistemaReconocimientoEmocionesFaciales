# Importa ABC (Abstract Base Class) y abstractmethod para crear clases abstractas
from abc import ABC, abstractmethod


# Clase abstracta base que define la interfaz para procesadores de características faciales
class FeatureProcessor(ABC):
    # Método abstracto que debe ser implementado por todas las subclases
    @abstractmethod
    def process(self, points: dict):
        # Lanza un error si no se implementa en la subclase
        raise NotImplementedError
