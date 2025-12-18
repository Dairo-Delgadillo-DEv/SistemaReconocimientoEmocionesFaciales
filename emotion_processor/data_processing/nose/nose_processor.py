# Importa la clase base abstracta para procesadores de características
from emotion_processor.data_processing.feature_processor import FeatureProcessor
# Importa las clases necesarias para procesar puntos de nariz
from emotion_processor.data_processing.nose.nose_processing import (NosePointsProcessing,
                                                                    EuclideanDistanceCalculator)


# Clase procesadora de nariz que implementa la interfaz FeatureProcessor
class NoseProcessor(FeatureProcessor):
    # Constructor que inicializa el calculador de distancias y el procesador de nariz
    def __init__(self):
        # Crea un calculador de distancias euclidiano
        distance_calculator = EuclideanDistanceCalculator()
        # Inicializa el procesador de puntos de nariz con el calculador
        self.processor = NosePointsProcessing(distance_calculator)

    # Procesa los puntos de la nariz y retorna las métricas calculadas
    def process(self, points: dict):
        # Delega el procesamiento al procesador de puntos de nariz
        return self.processor.main(points)
