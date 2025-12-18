# Importa la clase base para calculadores de puntuación con pesos
from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore


# Clase que calcula la puntuación de la emoción de sorpresa
class SurpriseScore(WeightedEmotionScore):
    # Constructor que define los pesos de cada característica para sorpresa
    def __init__(self):
        # Sorpresa: cejas 40%, ojos 25%, nariz 10%, boca 25%
        super().__init__(eyebrows_weight=0.40, eyes_weight=0.25, nose_weight=0.1, mouth_weight=0.25)

    # Calcula la puntuación de las cejas para sorpresa
    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Si las cejas están separadas, suma 10 puntos
        if 'eyebrows separated' in eyebrows_result:
            score += 10.0
        # Si la ceja derecha está levantada, suma 45 puntos
        if 'right eyebrow: raised' in eyebrows_result:
            score += 45.0
        # Si la ceja izquierda está levantada, suma 45 puntos
        if 'left eyebrow: raised' in eyebrows_result:
            score += 45.0
        return score

    # Calcula la puntuación de los ojos para sorpresa
    def calculate_eyes_score(self, eyes_result: str) -> float:
        # Si los ojos están abiertos, retorna 100 puntos (característica clave de sorpresa)
        if 'open eyes' in eyes_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la nariz para sorpresa
    def calculate_nose_score(self, nose_result: str) -> float:
        # Si la nariz está neutral, retorna 100 puntos
        if 'neutral nose' in nose_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la boca para sorpresa
    def calculate_mouth_score(self, mouth_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Si la boca está abierta, suma 80 puntos (característica clave de sorpresa)
        if 'open mouth' in mouth_result:
            score += 80.0
        # Si no hay sonrisa derecha, suma 10 puntos
        if 'no right smile' in mouth_result:
            score += 10.0
        # Si no hay sonrisa izquierda, suma 10 puntos
        if 'no left smile' in mouth_result:
            score += 10.0
        return score
