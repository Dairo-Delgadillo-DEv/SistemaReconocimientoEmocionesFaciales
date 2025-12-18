# Importa Dict para anotaciones de tipo
from typing import Dict
# Importa la clase base abstracta para calculadores de puntuación de emociones
from emotion_processor.emotions_recognition.features.emotion_score import EmotionScore
# Importa el calculador de puntuación para la emoción de sorpresa
from .emotions.suprise_score import SurpriseScore
# Importa el calculador de puntuación para la emoción de enojo
from .emotions.angry_score import AngryScore
# Importa el calculador de puntuación para la emoción de disgusto
from .emotions.disgust_score import DisgustScore
# Importa el calculador de puntuación para la emoción de tristeza
from .emotions.sad_score import SadScore
# Importa el calculador de puntuación para la emoción de felicidad
from .emotions.happy_score import HappyScore
# Importa el calculador de puntuación para la emoción de miedo
from .emotions.fear_score import FearScore


# Clase principal para reconocer emociones basándose en características faciales procesadas
class EmotionRecognition:
    # Constructor que inicializa todos los calculadores de emociones
    def __init__(self):
        # Diccionario que mapea cada emoción a su calculador de puntuación específico
        self.emotions: Dict[str, EmotionScore] = {
            'surprise': SurpriseScore(),  # Calculador de sorpresa
            'angry': AngryScore(),  # Calculador de enojo
            'disgust': DisgustScore(),  # Calculador de disgusto
            'sad': SadScore(),  # Calculador de tristeza
            'happy': HappyScore(),  # Calculador de felicidad
            'fear': FearScore(),  # Calculador de miedo
        }

    # Reconoce emociones calculando puntuaciones para cada una basándose en características procesadas
    def recognize_emotion(self, processed_features: dict) -> dict:
        # Diccionario para almacenar las puntuaciones de todas las emociones
        scores = {}
        # Itera sobre cada emoción y su calculador de puntuación
        for emotion_name, emotion_score_obj in self.emotions.items():
            # Calcula la puntuación de la emoción y actualiza el diccionario de puntuaciones
            scores.update(emotion_score_obj.calculate_score(processed_features))
        # Retorna el diccionario con las puntuaciones de todas las emociones
        return scores
