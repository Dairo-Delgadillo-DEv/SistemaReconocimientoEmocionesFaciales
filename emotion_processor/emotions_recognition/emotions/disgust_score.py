# Importa la clase base para calculadores de puntuación con pesos
from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore


# Clase que calcula la puntuación de la emoción de disgusto
class DisgustScore(WeightedEmotionScore):
    # Constructor que define los pesos de cada característica para disgusto
    def __init__(self):
        # Disgusto: cejas 25%, ojos 25%, nariz 35% (la nariz es la característica más importante), boca 15%
        super().__init__(eyebrows_weight=0.25, eyes_weight=0.25, nose_weight=0.35, mouth_weight=0.15)

    # Calcula la puntuación de las cejas para disgusto
    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Si las cejas están juntas, suma 33.33 puntos
        if 'eyebrows together' in eyebrows_result:
            score += 33.33
        # Si la ceja derecha está bajada, suma 33.33 puntos
        if 'right eyebrow: lowered' in eyebrows_result:
            score += 33.33
        # Si la ceja izquierda está bajada, suma 33.33 puntos
        if 'left eyebrow: lowered' in eyebrows_result:
            score += 33.33
        return score

    # Calcula la puntuación de los ojos para disgusto
    def calculate_eyes_score(self, eyes_result: str) -> float:
        # Si los ojos están cerrados/entrecerrados, retorna 100 puntos
        if 'closed eyes' in eyes_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la nariz para disgusto
    def calculate_nose_score(self, nose_result: str) -> float:
        # Si la nariz está arrugada, retorna 100 puntos (característica clave de disgusto)
        if 'wrinkled nose' in nose_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la boca para disgusto
    def calculate_mouth_score(self, mouth_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Divide el resultado en partes individuales
        mouth_result = mouth_result.split(', ')
        # Si la boca está abierta, suma 50 puntos
        if 'open mouth' in mouth_result:
            score += 50.0
        # Si hay sonrisa derecha, suma 25 puntos
        if 'right smile' in mouth_result:
            score += 25.0
        # Si hay sonrisa izquierda, suma 25 puntos
        if 'left smile' in mouth_result:
            score += 25.0
        return score
