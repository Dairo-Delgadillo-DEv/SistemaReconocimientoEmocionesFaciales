# Importa la clase base para calculadores de puntuación con pesos
from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore


# Clase que calcula la puntuación de la emoción de tristeza
class SadScore(WeightedEmotionScore):
    # Constructor que define los pesos de cada característica para tristeza
    def __init__(self):
        # Tristeza: cejas 30%, ojos 30%, nariz 10%, boca 30%
        super().__init__(eyebrows_weight=0.30, eyes_weight=0.30, nose_weight=0.1, mouth_weight=0.3)

    # Calcula la puntuación de las cejas para tristeza
    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Si las cejas están juntas, suma 60 puntos (característica de tristeza)
        if 'eyebrows together' in eyebrows_result:
            score += 60.0
        # Si la ceja derecha está bajada, suma 20 puntos
        if 'right eyebrow: lowered' in eyebrows_result:
            score += 20.0
        # Si la ceja izquierda está bajada, suma 20 puntos
        if 'left eyebrow: lowered' in eyebrows_result:
            score += 20.0
        return score

    # Calcula la puntuación de los ojos para tristeza
    def calculate_eyes_score(self, eyes_result: str) -> float:
        # Si los ojos están cerrados/entrecerrados, retorna 100 puntos
        if 'closed eyes' in eyes_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la nariz para tristeza
    def calculate_nose_score(self, nose_result: str) -> float:
        # Si la nariz está neutral, retorna 100 puntos
        if 'neutral nose' in nose_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la boca para tristeza
    def calculate_mouth_score(self, mouth_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Si la boca está cerrada, suma 30 puntos
        if 'closed mouth' in mouth_result:
            score += 30.0
        # Si no hay sonrisa derecha, suma 35 puntos (característica de tristeza)
        if 'no right smile' in mouth_result:
            score += 35.0
        # Si no hay sonrisa izquierda, suma 35 puntos (característica de tristeza)
        if 'no left smile' in mouth_result:
            score += 35.0
        return score
