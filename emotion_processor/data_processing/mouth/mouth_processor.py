# Importa la clase base abstracta para procesadores de características
from emotion_processor.data_processing.feature_processor import FeatureProcessor
# Importa las clases necesarias para procesar puntos de boca
from emotion_processor.data_processing.mouth.mouth_processing import (MouthPointsProcessing,
                                                                      PolynomialMouthArchCalculator,
                                                                      EuclideanDistanceCalculator)


# Clase procesadora de boca que implementa la interfaz FeatureProcessor
class MouthProcessor(FeatureProcessor):
    # Constructor que inicializa los calculadores y el procesador de boca
    def __init__(self):
        # Crea un calculador de arco de boca usando ajuste polinomial
        arch_calculator = PolynomialMouthArchCalculator()
        # Crea un calculador de distancias euclidiano
        distance_calculator = EuclideanDistanceCalculator()
        # Inicializa el procesador de puntos de boca con los calculadores
        self.processor = MouthPointsProcessing(arch_calculator, distance_calculator)

    # Procesa los puntos de la boca y retorna las métricas calculadas
    def process(self, points: dict):
        # Delega el procesamiento al procesador de puntos de boca
        return self.processor.main(points)
