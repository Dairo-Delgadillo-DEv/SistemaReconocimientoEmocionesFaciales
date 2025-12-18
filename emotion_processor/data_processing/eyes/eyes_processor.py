# Importa la clase base abstracta para procesadores de características
from emotion_processor.data_processing.feature_processor import FeatureProcessor
# Importa las clases necesarias para procesar puntos de ojos
from emotion_processor.data_processing.eyes.eyes_processing import (EyesPointsProcessing,
                                                                    PolynomialEyesArchCalculator,
                                                                    EuclideanDistanceCalculator)


# Clase procesadora de ojos que implementa la interfaz FeatureProcessor
class EyesProcessor(FeatureProcessor):
    # Constructor que inicializa los calculadores y el procesador de ojos
    def __init__(self):
        # Crea un calculador de arco de ojos usando ajuste polinomial
        arch_calculator = PolynomialEyesArchCalculator()
        # Crea un calculador de distancias euclidiano
        distance_calculator = EuclideanDistanceCalculator()
        # Inicializa el procesador de puntos de ojos con los calculadores
        self.processor = EyesPointsProcessing(arch_calculator, distance_calculator)

    # Procesa los puntos de los ojos y retorna las métricas calculadas
    def process(self, points: dict):
        # Delega el procesamiento al procesador de puntos de ojos
        return self.processor.main(points)
