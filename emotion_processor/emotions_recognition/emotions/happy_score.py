# Importa la clase base para calculadores de puntuación con pesos
from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore


# Clase que calcula la puntuación de la emoción de felicidad
class HappyScore(WeightedEmotionScore):
    # Constructor que define los pesos de cada característica para felicidad
    def __init__(self):
        # Felicidad: cejas 10%, ojos 20%, nariz 10%, boca 60% (la boca es la característica más importante)
        super().__init__(eyebrows_weight=0.1, eyes_weight=0.20, nose_weight=0.1, mouth_weight=0.6)

    # Calcula la puntuación de las cejas para felicidad
    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Si las cejas están separadas, suma 50 puntos
        if 'eyebrows separated' in eyebrows_result:
            score += 50.0
        # Si la ceja derecha está bajada, suma 25 puntos
        if 'right eyebrow: lowered' in eyebrows_result:
            score += 25.0
        # Si la ceja izquierda está bajada, suma 25 puntos
        if 'left eyebrow: lowered' in eyebrows_result:
            score += 25.0
        return score

    # Calcula la puntuación de los ojos para felicidad
    def calculate_eyes_score(self, eyes_result: str) -> float:
        # Si los ojos están abiertos, retorna 100 puntos
        if 'open eyes' in eyes_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la nariz para felicidad
    def calculate_nose_score(self, nose_result: str) -> float:
        # Si la nariz está neutral, retorna 100 puntos
        if 'neutral nose' in nose_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la boca para felicidad
    def calculate_mouth_score(self, mouth_result: str) -> float:
        # Divide el resultado en partes individuales
        mouth_result = mouth_result.split(', ')
        # Inicializa la puntuación en 0
        score = 0.0
        # Si la boca está abierta, suma 16 puntos
        if 'open mouth' in mouth_result:
            score += 16.0
        # Si hay sonrisa derecha, suma 42 puntos (característica clave de felicidad)
        if 'right smile' in mouth_result:
            score += 42.0
        # Si hay sonrisa izquierda, suma 42 puntos (característica clave de felicidad)
        if 'left smile' in mouth_result:
            score += 42.0
        return score
