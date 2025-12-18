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


# Clase principal para procesar los puntos de la nariz y calcular métricas
class NosePointsProcessing:
    # Constructor que recibe el calculador de distancias mediante inyección de dependencias
    def __init__(self, distance_calculator: DistanceCalculator):
        # Almacena el calculador de distancias
        self.distance_calculator = distance_calculator
        # Diccionario para almacenar todas las métricas calculadas de la nariz
        self.nose: dict = {}

    # Calcula las distancias relevantes de la nariz
    def calculate_distances(self, eyebrows_points: dict):
        # Calcula la distancia entre la nariz y la parte superior de la boca
        upper_mouth = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][0], eyebrows_points['distances'][1])
        # Calcula la distancia de la parte inferior de la nariz
        lower_nose = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][2], eyebrows_points['distances'][3])

        # Retorna ambas distancias como una tupla
        return upper_mouth, lower_nose

    # Método principal que procesa todos los puntos de la nariz y calcula todas las métricas
    def main(self, mouth_points: dict):
        # Calcula las distancias entre la nariz y la boca
        mouth_upper_distance, nose_lower_distance = self.calculate_distances(mouth_points)
        # Almacena la distancia entre la nariz y la parte superior de la boca
        self.nose['mouth_upper_distance'] = mouth_upper_distance
        # Almacena la distancia de la parte inferior de la nariz
        self.nose['nose_lower_distance'] = nose_lower_distance
        # Línea comentada que imprimiría todas las métricas redondeadas a 4 decimales
        #print(f'Nose: { {k: (round(float(v), 4)) for k, v in self.nose.items()} }')
        # Retorna el diccionario con todas las métricas calculadas de la nariz
        return self.nose
