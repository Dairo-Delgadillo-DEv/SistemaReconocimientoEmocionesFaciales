# Importa OpenCV para dibujar sobre imágenes
import cv2
# Importa numpy para operaciones con arrays numéricos
import numpy as np


# Clase para visualizar las emociones detectadas sobre la imagen
class EmotionsVisualization:
    # Constructor que define los colores para cada emoción en formato BGR
    def __init__(self):
        # Diccionario que mapea cada emoción a su color específico (BGR)
        self.emotion_colors = {
            'surprise': (184, 183, 83),  # Color para sorpresa (cian)
            'angry': (35, 50, 220),  # Color para enojo (rojo)
            'disgust': (79, 164, 36),  # Color para disgusto (verde)
            'sad': (186, 119, 4),  # Color para tristeza (azul oscuro)
            'happy': (27, 151, 239),  # Color para felicidad (naranja)
            'fear': (128, 37, 146)  # Color para miedo (morado)
        }

    # Método principal que dibuja las emociones y sus puntuaciones sobre la imagen
    def main(self, emotions: dict, original_image: np.ndarray):
        # Itera sobre cada emoción y su puntuación con un índice
        for i, (emotion, score) in enumerate(emotions.items()):
            # Dibuja el nombre de la emoción en la imagen
            cv2.putText(original_image, emotion, (10, 30 + i * 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.emotion_colors[emotion], 1,
                        cv2.LINE_AA)
            # Dibuja una barra de progreso rellena proporcional a la puntuación de la emoción
            cv2.rectangle(original_image, (150, 15 + i * 40), (150 + int(score * 2.5), 35 + i * 40), self.emotion_colors[emotion],
                          -1)
            # Dibuja el contorno de la barra de progreso completa
            cv2.rectangle(original_image, (150, 15 + i * 40), (400, 35 + i * 40), (255, 255, 255), 1)

        # Retorna la imagen con las emociones visualizadas
        return original_image
