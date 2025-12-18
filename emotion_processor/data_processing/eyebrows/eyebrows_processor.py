# Importa la clase base abstracta para procesadores de características
from emotion_processor.data_processing.feature_processor import FeatureProcessor
# Importa las clases necesarias para procesar puntos de cejas
from emotion_processor.data_processing.eyebrows.eyebrows_processing import (EyeBrowsPointsProcessing,
                                                                            PolynomialEyebrowArchCalculator,
                                                                            EuclideanDistanceCalculator)


# Clase procesadora de cejas que implementa la interfaz FeatureProcessor
class EyeBrowsProcessor(FeatureProcessor):
    # Constructor que inicializa los calculadores y el procesador de cejas
    def __init__(self):
        # Crea un calculador de arco de cejas usando ajuste polinomial
        arch_calculator = PolynomialEyebrowArchCalculator()
        # Crea un calculador de distancias euclidiano
        distance_calculator = EuclideanDistanceCalculator()
        # Inicializa el procesador de puntos de cejas con los calculadores
        self.processor = EyeBrowsPointsProcessing(arch_calculator, distance_calculator)

    # Procesa los puntos de las cejas y retorna las métricas calculadas
    def process(self, points: dict):
        # Delega el procesamiento al procesador de puntos de cejas
        return self.processor.main(points)
