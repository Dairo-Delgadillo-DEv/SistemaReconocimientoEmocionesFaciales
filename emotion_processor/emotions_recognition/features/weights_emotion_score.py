# Importa ABC (Abstract Base Class) y abstractmethod para crear clases abstractas
from abc import ABC, abstractmethod
# Importa la clase base para calculadores de puntuación de emociones
from emotion_processor.emotions_recognition.features.emotion_score import EmotionScore
# Importa las implementaciones básicas de verificación de características faciales
from emotion_processor.emotions_recognition.features.feature_implementation import (BasicEyebrowsCheck, BasicEyesCheck,
                                                                                    BasicNoseCheck, BasicMouthCheck)


# Clase abstracta que calcula puntuaciones de emociones usando pesos para cada característica facial
class WeightedEmotionScore(EmotionScore, ABC):
    # Constructor que inicializa los pesos para cada característica facial
    def __init__(self, eyebrows_weight, eyes_weight, nose_weight, mouth_weight):
        # Peso de importancia de las cejas para esta emoción
        self.eyebrows_weight = eyebrows_weight
        # Peso de importancia de los ojos para esta emoción
        self.eyes_weight = eyes_weight
        # Peso de importancia de la nariz para esta emoción
        self.nose_weight = nose_weight
        # Peso de importancia de la boca para esta emoción
        self.mouth_weight = mouth_weight
        # Inicializa el verificador de cejas
        self.eyebrows_check = BasicEyebrowsCheck()
        # Inicializa el verificador de ojos
        self.eyes_check = BasicEyesCheck()
        # Inicializa el verificador de nariz
        self.nose_check = BasicNoseCheck()
        # Inicializa el verificador de boca
        self.mouth_check = BasicMouthCheck()

    # Calcula la puntuación total de la emoción basándose en todas las características faciales
    def calculate_score(self, features: dict) -> dict:
        # Verifica el estado de las cejas y obtiene una descripción textual
        eyebrows_result = self.eyebrows_check.check_eyebrows(features['eyebrows'])
        # Verifica el estado de los ojos y obtiene una descripción textual
        eyes_result = self.eyes_check.check_eyes(features['eyes'])
        # Verifica el estado de la nariz y obtiene una descripción textual
        nose_result = self.nose_check.check_nose(features['nose'])
        # Verifica el estado de la boca y obtiene una descripción textual
        mouth_result = self.mouth_check.check_mouth(features['mouth'])

        # Calcula la puntuación específica de las cejas para esta emoción
        eyebrows_score = self.calculate_eyebrows_score(eyebrows_result)
        # Calcula la puntuación específica de los ojos para esta emoción
        eyes_score = self.calculate_eyes_score(eyes_result)
        # Calcula la puntuación específica de la nariz para esta emoción
        nose_score = self.calculate_nose_score(nose_result)
        # Calcula la puntuación específica de la boca para esta emoción
        mouth_score = self.calculate_mouth_score(mouth_result)

        # Calcula la puntuación total ponderada sumando cada puntuación multiplicada por su peso
        total_score = (eyebrows_score * self.eyebrows_weight +
                       eyes_score * self.eyes_weight +
                       nose_score * self.nose_weight +
                       mouth_score * self.mouth_weight)
        # Retorna un diccionario con el nombre de la emoción y su puntuación
        return {self.__class__.__name__.replace("Score", "").lower(): total_score}

    # Método abstracto para calcular la puntuación de las cejas (debe implementarse en subclases)
    @abstractmethod
    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        pass

    # Método abstracto para calcular la puntuación de los ojos (debe implementarse en subclases)
    @abstractmethod
    def calculate_eyes_score(self, eyes_result: str) -> float:
        pass

    # Método abstracto para calcular la puntuación de la nariz (debe implementarse en subclases)
    @abstractmethod
    def calculate_nose_score(self, nose_result: str) -> float:
        pass

    # Método abstracto para calcular la puntuación de la boca (debe implementarse en subclases)
    @abstractmethod
    def calculate_mouth_score(self, mouth_result: str) -> float:
        pass
