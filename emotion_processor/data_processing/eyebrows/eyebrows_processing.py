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


# Clase abstracta base para calcular el arco de las cejas
class EyebrowArchCalculator(ABC):
    # Método abstracto que debe ser implementado por las subclases
    @abstractmethod
    def calculate_eyebrow_arch(self, eyebrow_points):
        pass


# Implementación concreta que calcula el arco de la ceja usando ajuste polinomial
class PolynomialEyebrowArchCalculator(EyebrowArchCalculator):
    # Calcula la curvatura de la ceja ajustando un polinomio de grado 2
    def calculate_eyebrow_arch(self, eyebrow_points):
        # Extrae las coordenadas x de todos los puntos de la ceja
        x = [point[0] for point in eyebrow_points]
        # Extrae las coordenadas y de todos los puntos de la ceja
        y = [point[1] for point in eyebrow_points]
        # Ajusta un polinomio de grado 2 (parábola) a los puntos
        z = np.polyfit(x, y, 2)
        # Retorna el coeficiente cuadrático (indica la curvatura de la ceja)
        return z[0]


# Clase principal para procesar los puntos de las cejas y calcular métricas
class EyeBrowsPointsProcessing:
    # Constructor que recibe los calculadores de arco y distancia mediante inyección de dependencias
    def __init__(self, arch_calculator: EyebrowArchCalculator, distance_calculator: DistanceCalculator):
        # Almacena el calculador de arco de cejas
        self.arch_calculator = arch_calculator
        # Almacena el calculador de distancias
        self.distance_calculator = distance_calculator
        # Diccionario para almacenar todas las métricas calculadas de las cejas
        self.eyebrows: dict = {}

    # Calcula todas las distancias relevantes entre puntos de las cejas
    def calculate_distances(self, eyebrows_points: dict):
        # Calcula la distancia entre la ceja derecha y el ojo derecho (puntos 0 y 1)
        right_eyebrow_to_eye_distance = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][0], eyebrows_points['distances'][1])
        # Calcula la distancia entre la ceja izquierda y el ojo izquierdo (puntos 2 y 3)
        left_eyebrow_to_eye_distance = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][2], eyebrows_points['distances'][3])
        # Calcula la distancia entre la ceja derecha y la frente (puntos 4 y 5)
        right_eyebrow_to_forehead_distance = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][4], eyebrows_points['distances'][5])
        # Calcula la distancia entre la ceja izquierda y la frente (puntos 6 y 7)
        left_eyebrow_to_forehead_distance = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][6], eyebrows_points['distances'][7])
        # Calcula la distancia entre ambas cejas (puntos 8 y 9)
        distance_between_eyebrows = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][8], eyebrows_points['distances'][9])
        # Calcula la distancia entre el punto medio de las cejas y la frente (puntos 10 y 11)
        distance_between_eyebrow_forehead = self.distance_calculator.calculate_distance(
            eyebrows_points['distances'][10], eyebrows_points['distances'][11])

        # Retorna todas las distancias calculadas como una tupla
        return (right_eyebrow_to_eye_distance, left_eyebrow_to_eye_distance, right_eyebrow_to_forehead_distance,
                left_eyebrow_to_forehead_distance, distance_between_eyebrows, distance_between_eyebrow_forehead)

    # Método principal que procesa todos los puntos de las cejas y calcula todas las métricas
    def main(self, eyebrows_points: dict):
        # Calcula el arco (curvatura) de la ceja derecha usando los puntos del arco derecho
        right_eyebrow_arch = self.arch_calculator.calculate_eyebrow_arch(eyebrows_points['right arch'])
        # Calcula el arco (curvatura) de la ceja izquierda usando los puntos del arco izquierdo
        left_eyebrow_arch = self.arch_calculator.calculate_eyebrow_arch(eyebrows_points['left arch'])
        # Almacena el valor del arco de la ceja derecha en el diccionario
        self.eyebrows['arch_right'] = right_eyebrow_arch
        # Almacena el valor del arco de la ceja izquierda en el diccionario
        self.eyebrows['arch_left'] = left_eyebrow_arch

        # Calcula todas las distancias y las desempaqueta en variables individuales
        (right_eye_distance, left_eye_distance, right_forehead_distance, left_forehead_distance, eyebrows_distance,
         eyebrow_distance_forehead) = (self.calculate_distances(eyebrows_points))
        # Almacena la distancia entre la ceja derecha y el ojo derecho
        self.eyebrows['eye_right_distance'] = right_eye_distance
        # Almacena la distancia entre la ceja izquierda y el ojo izquierdo
        self.eyebrows['eye_left_distance'] = left_eye_distance
        # Almacena la distancia entre la ceja derecha y la frente
        self.eyebrows['forehead_right_distance'] = right_forehead_distance
        # Almacena la distancia entre la ceja izquierda y la frente
        self.eyebrows['forehead_left_distance'] = left_forehead_distance
        # Almacena la distancia entre ambas cejas
        self.eyebrows['eyebrows_distance'] = eyebrows_distance
        # Almacena la distancia entre el punto medio de las cejas y la frente
        self.eyebrows['eyebrow_distance_forehead'] = eyebrow_distance_forehead
        # Línea comentada que imprimiría todas las métricas redondeadas a 4 decimales
        #print(f'Eyebrows: { {k: (round(float(v),4)) for k,v in self.eyebrows.items()}}')
        # Retorna el diccionario con todas las métricas calculadas de las cejas
        return self.eyebrows
