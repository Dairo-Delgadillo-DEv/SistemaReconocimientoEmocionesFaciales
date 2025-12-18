# Importa la clase base para calculadores de puntuación con pesos
from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore


# Clase que calcula la puntuación de la emoción de miedo
class FearScore(WeightedEmotionScore):
    # Constructor que define los pesos de cada característica para miedo
    def __init__(self):
        # Miedo: cejas 25%, ojos 25%, nariz 10%, boca 40%
        super().__init__(eyebrows_weight=0.25, eyes_weight=0.25, nose_weight=0.1, mouth_weight=0.4)

    # Calcula la puntuación de las cejas para miedo
    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Si las cejas están juntas, suma 20 puntos
        if 'eyebrows together' in eyebrows_result:
            score += 20.0
        # Si la ceja derecha está levantada, suma 40 puntos (característica de miedo)
        if 'right eyebrow: raised' in eyebrows_result:
            score += 40.0
        # Si la ceja izquierda está levantada, suma 40 puntos (característica de miedo)
        if 'left eyebrow: raised' in eyebrows_result:
            score += 40.0
        return score

    # Calcula la puntuación de los ojos para miedo
    def calculate_eyes_score(self, eyes_result: str) -> float:
        # Si los ojos están cerrados/entrecerrados, retorna 100 puntos
        if 'closed eyes' in eyes_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la nariz para miedo
    def calculate_nose_score(self, nose_result: str) -> float:
        # Si la nariz está neutral, retorna 100 puntos
        if 'neutral nose' in nose_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la boca para miedo
    def calculate_mouth_score(self, mouth_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Divide el resultado en partes individuales
        mouth_result = mouth_result.split(', ')
        # Si la boca está abierta, suma 75 puntos (característica clave de miedo)
        if 'open mouth' in mouth_result:
            score += 75.0
        # Si no hay sonrisa derecha, suma 12.5 puntos
        if 'no right smile' in mouth_result:
            score += 12.5
        # Si no hay sonrisa izquierda, suma 12.5 puntos
        if 'no left smile' in mouth_result:
            score += 12.5
        return score
