# Importa la clase base abstracta para procesadores de características
from emotion_processor.data_processing.feature_processor import FeatureProcessor
# Importa el procesador específico para cejas
from emotion_processor.data_processing.eyebrows.eyebrows_processor import EyeBrowsProcessor
# Importa el procesador específico para ojos
from emotion_processor.data_processing.eyes.eyes_processor import EyesProcessor
# Importa el procesador específico para nariz
from emotion_processor.data_processing.nose.nose_processor import NoseProcessor
# Importa el procesador específico para boca
from emotion_processor.data_processing.mouth.mouth_processor import MouthProcessor


# Clase principal que coordina el procesamiento de todos los puntos faciales
class PointsProcessing:
    # Constructor que inicializa todos los procesadores de características faciales
    def __init__(self):
        # Diccionario que mapea cada característica facial a su procesador específico
        self.processors: dict[str, FeatureProcessor] = {
            'eyebrows': EyeBrowsProcessor(),  # Procesador de cejas
            'eyes': EyesProcessor(),  # Procesador de ojos
            'nose': NoseProcessor(),  # Procesador de nariz
            'mouth': MouthProcessor()  # Procesador de boca
        }
        # Diccionario para almacenar los puntos procesados de todas las características
        self.processed_points: dict = {}

    # Método principal que procesa todos los puntos faciales
    def main(self, points: dict):
        # Reinicia el diccionario de puntos procesados
        self.processed_points = {}
        # Itera sobre cada característica facial y su procesador
        for feature, processor in self.processors.items():
            # Obtiene los puntos de la característica actual (o diccionario vacío si no existe)
            feature_points = points.get(feature, {})
            # Procesa los puntos de la característica y almacena el resultado
            self.processed_points[feature] = processor.process(feature_points)
        # Retorna el diccionario con todas las características procesadas
        return self.processed_points

