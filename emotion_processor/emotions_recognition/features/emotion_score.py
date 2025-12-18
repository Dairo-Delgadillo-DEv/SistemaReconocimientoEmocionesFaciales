# Importa ABC (Abstract Base Class) y abstractmethod para crear clases abstractas
from abc import ABC, abstractmethod


# Clase abstracta base que define la interfaz para calculadores de puntuación de emociones
class EmotionScore(ABC):
    # Método abstracto que debe ser implementado por todas las subclases
    @abstractmethod
    def calculate_score(self, features: dict) -> dict:
        # Calcula la puntuación de una emoción basándose en características faciales
        pass
    