# Importa la clase base para calculadores de puntuación con pesos
from emotion_processor.emotions_recognition.features.weights_emotion_score import WeightedEmotionScore


# Clase que calcula la puntuación de la emoción de enojo
class AngryScore(WeightedEmotionScore):
    # Constructor que define los pesos de cada característica para enojo
    def __init__(self):
        # Enojo: cejas 40%, ojos 25%, nariz 10%, boca 25%
        super().__init__(eyebrows_weight=0.40, eyes_weight=0.25, nose_weight=0.1, mouth_weight=0.25)

    # Calcula la puntuación de las cejas para enojo
    def calculate_eyebrows_score(self, eyebrows_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Si las cejas están juntas, suma 50 puntos (característica clave de enojo)
        if 'eyebrows together' in eyebrows_result:
            score += 50.0
        # Si la ceja derecha está bajada, suma 25 puntos
        if 'right eyebrow: lowered' in eyebrows_result:
            score += 25.0
        # Si la ceja izquierda está bajada, suma 25 puntos
        if 'left eyebrow: lowered' in eyebrows_result:
            score += 25.0
        return score

    # Calcula la puntuación de los ojos para enojo
    def calculate_eyes_score(self, eyes_result: str) -> float:
        # Si los ojos están cerrados/entrecerrados, retorna 100 puntos
        if 'closed eyes' in eyes_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la nariz para enojo
    def calculate_nose_score(self, nose_result: str) -> float:
        # Si la nariz está arrugada, retorna 100 puntos
        if 'wrinkled nose' in nose_result:
            return 100.0
        return 0.0

    # Calcula la puntuación de la boca para enojo
    def calculate_mouth_score(self, mouth_result: str) -> float:
        # Inicializa la puntuación en 0
        score = 0.0
        # Divide el resultado en partes individuales
        mouth_result = mouth_result.split(', ')
        # Si la boca está cerrada, suma 20 puntos
        if 'closed mouth' in mouth_result:
            score += 20.0
        # Si no hay sonrisa derecha, suma 40 puntos (característica de enojo)
        if 'no right smile' in mouth_result:
            score += 40.0
        # Si no hay sonrisa izquierda, suma 40 puntos (característica de enojo)
        if 'no left smile' in mouth_result:
            score += 40.0
        return score
