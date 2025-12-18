# Importa ABC (Abstract Base Class) y abstractmethod para crear clases abstractas
from abc import ABC, abstractmethod


# Clase abstracta base para verificar el estado de las cejas
class EyebrowsCheck(ABC):
    # Método abstracto que analiza las cejas y retorna una descripción de su estado
    @abstractmethod
    def check_eyebrows(self, eyebrows: dict) -> str:
        pass


# Clase abstracta base para verificar el estado de los ojos
class EyesCheck(ABC):
    # Método abstracto que analiza los ojos y retorna una descripción de su estado
    @abstractmethod
    def check_eyes(self, eyes: dict) -> str:
        pass


# Clase abstracta base para verificar el estado de la nariz
class NoseCheck(ABC):
    # Método abstracto que analiza la nariz y retorna una descripción de su estado
    @abstractmethod
    def check_nose(self, nose: dict) -> str:
        pass


# Clase abstracta base para verificar el estado de la boca
class MouthCheck(ABC):
    # Método abstracto que analiza la boca y retorna una descripción de su estado
    @abstractmethod
    def check_mouth(self, mouth: dict) -> str:
        pass
