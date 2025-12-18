# Importa numpy para operaciones con arrays numéricos
import numpy as np
# Importa el procesador de malla facial
from emotion_processor.face_mesh.face_mesh_processor import FaceMeshProcessor
# Importa el procesador de puntos faciales
from emotion_processor.data_processing.main import PointsProcessing
# Importa el sistema de reconocimiento de emociones
from emotion_processor.emotions_recognition.main import EmotionRecognition
# Importa el sistema de visualización de emociones
from emotion_processor.emotions_visualizations.main import EmotionsVisualization


# Clase principal que coordina todo el sistema de reconocimiento de emociones
class EmotionRecognitionSystem:
    # Constructor que inicializa todos los componentes del sistema
    def __init__(self):
        # Inicializa el procesador de malla facial para detectar puntos del rostro
        self.face_mesh = FaceMeshProcessor()
        # Inicializa el procesador de datos para calcular métricas de características faciales
        self.data_processing = PointsProcessing()
        # Inicializa el sistema de reconocimiento de emociones
        self.emotions_recognition = EmotionRecognition()
        # Inicializa el sistema de visualización de emociones
        self.emotions_visualization = EmotionsVisualization()

    # Procesa un frame de imagen para detectar y visualizar emociones
    def frame_processing(self, face_image: np.ndarray):
        # Procesa la imagen para extraer puntos faciales y dibuja la malla
        face_points, control_process, original_image = self.face_mesh.process(face_image, draw=True)
        # Si se detectó un rostro exitosamente
        if control_process:
            # Procesa los puntos faciales para calcular características
            processed_features = self.data_processing.main(face_points)
            # Reconoce las emociones basándose en las características procesadas
            emotions = self.emotions_recognition.recognize_emotion(processed_features)
            # Dibuja las emociones detectadas sobre la imagen
            draw_emotions = self.emotions_visualization.main(emotions, original_image)
            # Retorna la imagen con las emociones visualizadas
            return draw_emotions
        else:
            # Si no se detectó rostro, lanza una excepción (nota: no se captura)
            Exception(f"No face mesh")
            # Retorna la imagen original sin modificar
            return face_image

