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


# Clase abstracta base para calcular el arco de los ojos
class EyesArchCalculator(ABC):
    # Método abstracto que debe ser implementado por las subclases
    @abstractmethod
    def calculate_eyes_arch(self, eyebrow_points):
        pass


# Implementación concreta que calcula el arco del ojo usando ajuste polinomial
class PolynomialEyesArchCalculator(EyesArchCalculator):
    # Calcula la curvatura del ojo ajustando un polinomio de grado 2
    def calculate_eyes_arch(self, eyebrow_points):
        # Extrae las coordenadas x de todos los puntos del ojo
        x = [point[0] for point in eyebrow_points]
        # Extrae las coordenadas y de todos los puntos del ojo
        y = [point[1] for point in eyebrow_points]
        # Ajusta un polinomio de grado 2 (parábola) a los puntos
        z = np.polyfit(x, y, 2)
        # Retorna el coeficiente cuadrático (indica la curvatura del ojo)
        return z[0]


# Clase principal para procesar los puntos de los ojos y calcular métricas
class EyesPointsProcessing:
    # Constructor que recibe los calculadores de arco y distancia mediante inyección de dependencias
    def __init__(self, arch_calculator: EyesArchCalculator, distance_calculator: DistanceCalculator):
        # Almacena el calculador de arco de ojos
        self.arch_calculator = arch_calculator
        # Almacena el calculador de distancias
        self.distance_calculator = distance_calculator
        # Diccionario para almacenar todas las métricas calculadas de los ojos
        self.eyes: dict = {}

    # Calcula todas las distancias relevantes de los párpados
    def calculate_distances(self, eyebrows_points: dict):
        # Calcula la distancia del párpado superior derecho
        right_upper_eyelid = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][0], eyebrows_points['distances'][1])
        # Calcula la distancia del párpado superior izquierdo
        left_upper_eyelid = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][2], eyebrows_points['distances'][3])
        # Calcula la distancia del párpado inferior derecho
        right_lower_eyelid = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][4], eyebrows_points['distances'][5])
        # Calcula la distancia del párpado inferior izquierdo
        left_lower_eyelid = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][6], eyebrows_points['distances'][7])

        # Retorna todas las distancias calculadas como una tupla
        return right_upper_eyelid, left_upper_eyelid, right_lower_eyelid, left_lower_eyelid

    # Método principal que procesa todos los puntos de los ojos y calcula todas las métricas
    def main(self, eyes_points: dict):
        # Calcula el arco (curvatura) del ojo derecho usando los puntos del arco derecho
        right_eyes_arch = self.arch_calculator.calculate_eyes_arch(eyes_points['right arch'])
        # Calcula el arco (curvatura) del ojo izquierdo usando los puntos del arco izquierdo
        left_eyes_arch = self.arch_calculator.calculate_eyes_arch(eyes_points['left arch'])
        # Almacena el valor del arco del ojo derecho en el diccionario
        self.eyes['arch_right'] = right_eyes_arch
        # Almacena el valor del arco del ojo izquierdo en el diccionario
        self.eyes['arch_left'] = left_eyes_arch

        # Calcula todas las distancias de los párpados y las desempaqueta en variables individuales
        (right_upper_eyelid_distance, left_upper_eyelid_distance, right_lower_eyelid_distance,
         left_lower_eyelid_distance) = (self.calculate_distances(eyes_points))
        # Almacena la distancia del párpado superior derecho
        self.eyes['right_upper_eyelid_distance'] = right_upper_eyelid_distance
        # Almacena la distancia del párpado superior izquierdo
        self.eyes['left_upper_eyelid_distance'] = left_upper_eyelid_distance
        # Almacena la distancia del párpado inferior derecho
        self.eyes['right_lower_eyelid_distance'] = right_lower_eyelid_distance
        # Almacena la distancia del párpado inferior izquierdo
        self.eyes['left_lower_eyelid_distance'] = left_lower_eyelid_distance
        # Línea comentada que imprimiría todas las métricas redondeadas a 4 decimales
        #print(f'Eyes: { {k: (round(float(v),4)) for k,v in self.eyes.items()}}')
        # Retorna el diccionario con todas las métricas calculadas de los ojos
        return self.eyes
