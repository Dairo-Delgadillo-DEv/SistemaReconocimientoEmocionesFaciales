# Importa numpy para operaciones matemáticas y de arrays
import numpy as np
# Importa ABC (Abstract Base Class) y abstractmethod para crear clases abstractas
from abc import ABC, abstractmethod


# Clase abstracta base para calcular distancias entre puntos
class DistanceCalculator(ABC):
    # Método abstracto que debe ser implementado por las subclases
    @abstractmethod
    def calculate_distance(self, point1, point2):
        pass


# Implementación concreta del calculador de distancias usando distancia euclidiana
class EuclideanDistanceCalculator(DistanceCalculator):
    # Calcula la distancia euclidiana entre dos puntos
    def calculate_distance(self, point1, point2):
        # Convierte los puntos a arrays de numpy, calcula la diferencia y obtiene la norma (distancia)
        return np.linalg.norm(np.array(point1) - np.array(point2))


# Clase abstracta base para calcular el arco de los labios
class MouthArchCalculator(ABC):
    # Método abstracto que debe ser implementado por las subclases
    @abstractmethod
    def calculate_lips_arch(self, eyebrow_points):
        pass


# Implementación concreta que calcula el arco de los labios usando ajuste polinomial
class PolynomialMouthArchCalculator(MouthArchCalculator):
    # Calcula la curvatura de los labios ajustando un polinomio de grado 2
    def calculate_lips_arch(self, eyebrow_points):
        # Extrae las coordenadas x de todos los puntos de los labios
        x = [point[0] for point in eyebrow_points]
        # Extrae las coordenadas y de todos los puntos de los labios
        y = [point[1] for point in eyebrow_points]
        # Ajusta un polinomio de grado 2 (parábola) a los puntos
        z = np.polyfit(x, y, 2)
        # Retorna el coeficiente cuadrático (indica la curvatura de los labios)
        return z[0]


# Clase principal para procesar los puntos de la boca y calcular métricas
class MouthPointsProcessing:
    # Constructor que recibe los calculadores de arco y distancia mediante inyección de dependencias
    def __init__(self, arch_calculator: MouthArchCalculator, distance_calculator: DistanceCalculator):
        # Almacena el calculador de arco de boca
        self.arch_calculator = arch_calculator
        # Almacena el calculador de distancias
        self.distance_calculator = distance_calculator
        # Diccionario para almacenar todas las métricas calculadas de la boca
        self.mouth: dict = {}

    # Calcula todas las distancias relevantes de la boca y labios
    def calculate_distances(self, eyebrows_points: dict):
        # Calcula la distancia de apertura del labio superior
        upper_mouth = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][0], eyebrows_points['distances'][1])
        # Calcula la distancia de apertura del labio inferior
        lower_mouth = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][2], eyebrows_points['distances'][3])
        # Calcula la distancia de la sonrisa derecha (comisura derecha)
        right_smile = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][4], eyebrows_points['distances'][5])
        # Calcula la distancia del labio derecho
        right_lip = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][6], eyebrows_points['distances'][7])
        # Calcula la distancia de la sonrisa izquierda (comisura izquierda)
        left_smile = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][8], eyebrows_points['distances'][9])
        # Calcula la distancia del labio izquierdo
        left_lip = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][10], eyebrows_points['distances'][11])

        # Retorna todas las distancias calculadas como una tupla
        return upper_mouth, lower_mouth, right_smile, right_lip, left_smile, left_lip

    # Método principal que procesa todos los puntos de la boca y calcula todas las métricas
    def main(self, mouth_points: dict):
        # Calcula el arco (curvatura) del labio superior usando los puntos del arco superior
        upper_arch = self.arch_calculator.calculate_lips_arch(mouth_points['upper arch'])
        # Calcula el arco (curvatura) del labio inferior usando los puntos del arco inferior
        lower_arch = self.arch_calculator.calculate_lips_arch(mouth_points['lower arch'])
        # Almacena el valor del arco del labio superior en el diccionario
        self.mouth['upper_arch'] = upper_arch
        # Almacena el valor del arco del labio inferior en el diccionario
        self.mouth['lower_arch'] = lower_arch

        # Calcula todas las distancias de los labios y las desempaqueta en variables individuales
        (mouth_upper_distance, mouth_lower_distance, right_smile_distance, right_lip_distance, left_smile_distance,
         left_lip_distance) = self.calculate_distances(mouth_points)
        # Almacena la distancia de apertura del labio superior
        self.mouth['mouth_upper_distance'] = mouth_upper_distance
        # Almacena la distancia de apertura del labio inferior
        self.mouth['mouth_lower_distance'] = mouth_lower_distance
        # Almacena la distancia de la sonrisa derecha
        self.mouth['right_smile_distance'] = right_smile_distance
        # Almacena la distancia del labio derecho
        self.mouth['right_lip_distance'] = right_lip_distance
        # Almacena la distancia de la sonrisa izquierda
        self.mouth['left_smile_distance'] = left_smile_distance
        # Almacena la distancia del labio izquierdo
        self.mouth['left_lip_distance'] = left_lip_distance
        # Línea comentada que imprimiría todas las métricas redondeadas a 4 decimales
        #print(f'Mouth: { {k: (round(float(v), 4)) for k, v in self.mouth.items()} }')
        # Retorna el diccionario con todas las métricas calculadas de la boca
        return self.mouth
