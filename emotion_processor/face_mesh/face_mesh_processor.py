# Importa numpy para operaciones con arrays numéricos
import numpy as np
# Importa OpenCV para procesamiento de imágenes y video
import cv2
# Importa MediaPipe para detección de malla facial
import mediapipe as mp
# Importa tipos para anotaciones de tipo en Python
from typing import Any, Tuple, List, Dict


# Clase para realizar la inferencia de malla facial usando MediaPipe
class FaceMeshInference:
    # Constructor que inicializa los parámetros de confianza mínima
    def __init__(self, min_detection_confidence=0.6, min_tracking_confidence=0.6):
        # Crea una instancia de FaceMesh de MediaPipe con configuraciones específicas
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,  # Modo video (False) en lugar de imagen estática
            max_num_faces=1,  # Detecta máximo 1 rostro por frame
            refine_landmarks=True,  # Refina los puntos de referencia para mayor precisión
            min_detection_confidence=min_detection_confidence,  # Confianza mínima para detectar un rostro
            min_tracking_confidence=min_tracking_confidence  # Confianza mínima para seguir un rostro detectado
        )

    # Procesa una imagen para detectar la malla facial
    def process(self, image: np.ndarray) -> Tuple[bool, Any]:
        # Convierte la imagen de BGR (formato OpenCV) a RGB (formato MediaPipe)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Procesa la imagen RGB para detectar puntos de la malla facial
        face_mesh = self.face_mesh.process(rgb_image)
        # Retorna si se detectó un rostro y el objeto con información de la malla
        return bool(face_mesh.multi_face_landmarks), face_mesh


        


# Clase para extraer puntos específicos de características faciales
class FaceMeshExtractor:
    # Constructor que inicializa la estructura de datos para almacenar puntos
    def __init__(self):
        # Diccionario que almacena puntos de diferentes características faciales
        self.points: dict = {
            'eyebrows': {'right arch': [], 'left arch': [], 'distances': []},  # Puntos de cejas
            'eyes': {'right arch': [], 'left arch': [], 'distances': []},  # Puntos de ojos
            'nose': {'distances': []},  # Puntos de nariz
            'mouth': {'upper arch': [], 'lower arch': [], 'distances': []}  # Puntos de boca
        }

    # Extrae todos los puntos de la malla facial y los convierte a coordenadas de píxeles
    def extract_points(self, face_image: np.ndarray, face_mesh_info: Any) -> List[List[int]]:
        # Obtiene las dimensiones de la imagen (altura, ancho, canales)
        h, w, _ = face_image.shape
        # Crea una lista de puntos con [índice, coordenada_x, coordenada_y]
        mesh_points = [
            [i, int(pt.x * w), int(pt.y * h)]  # Convierte coordenadas normalizadas (0-1) a píxeles
            for face in face_mesh_info.multi_face_landmarks  # Itera sobre cada rostro detectado
            for i, pt in enumerate(face.landmark)  # Itera sobre cada punto de referencia
        ]
        # Retorna la lista de puntos con sus coordenadas en píxeles
        return mesh_points

    # Extrae puntos específicos de características faciales según índices predefinidos
    def extract_feature_points(self, face_points: List[List[int]], feature_indices: dict):
        # Itera sobre cada característica facial (cejas, ojos, nariz, boca)
        for feature, indices in feature_indices.items():
            # Itera sobre cada sub-característica (arco derecho, izquierdo, distancias)
            for sub_feature, sub_indices in indices.items():
                # Extrae solo las coordenadas [x, y] (omite el índice) de los puntos especificados
                self.points[feature][sub_feature] = [face_points[i][1:] for i in sub_indices]

    # Obtiene los puntos específicos de las cejas
    def get_eyebrows_points(self, face_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        # Define los índices de los puntos de la malla facial que corresponden a las cejas
        feature_indices = {
            'eyebrows': {
                'right arch': [143, 156, 70, 63, 105, 66, 107],  # Índices del arco de la ceja derecha
                'left arch': [336, 296, 334, 293, 300, 383, 372],  # Índices del arco de la ceja izquierda
                'distances': [65, 468, 295, 473, 69, 66, 299, 296, 55, 8, 70, 21]  # Puntos para calcular distancias
            }
        }
        # Extrae los puntos usando los índices definidos
        self.extract_feature_points(face_points, feature_indices)
        # Retorna el diccionario con los puntos de las cejas
        return self.points['eyebrows']

    # Obtiene los puntos específicos de los ojos
    def get_eyes_points(self, face_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        # Define los índices de los puntos de la malla facial que corresponden a los ojos
        feature_indices = {
            'eyes': {
                'right arch': [33, 246, 161, 160, 159, 158, 157, 173, 133],  # Índices del contorno del ojo derecho
                'left arch': [263, 398, 384, 385, 386, 387, 388, 466, 263],  # Índices del contorno del ojo izquierdo
                'distances': [159, 145, 385, 374, 145, 230, 374, 450],  # Puntos para calcular distancias (apertura)
            }
        }
        # Extrae los puntos usando los índices definidos
        self.extract_feature_points(face_points, feature_indices)
        # Retorna el diccionario con los puntos de los ojos
        return self.points['eyes']

    # Obtiene los puntos específicos de la nariz
    def get_nose_points(self, face_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        # Define los índices de los puntos de la malla facial que corresponden a la nariz
        feature_indices = {
            'nose': {
                'distances': [0, 13, 2, 164],  # Puntos clave de la nariz para calcular distancias
            }
        }
        # Extrae los puntos usando los índices definidos
        self.extract_feature_points(face_points, feature_indices)
        # Retorna el diccionario con los puntos de la nariz
        return self.points['nose']

    # Obtiene los puntos específicos de la boca
    def get_mouth_points(self, face_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        # Define los índices de los puntos de la malla facial que corresponden a la boca
        feature_indices = {
            'mouth': {
                'upper arch': [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308],  # Índices del arco superior de la boca
                'lower arch': [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308],  # Índices del arco inferior de la boca
                'distances': [13, 14, 17, 200, 78, 186, 61, 95, 308, 410, 291, 324]  # Puntos para calcular distancias (apertura)
            }
        }
        # Extrae los puntos usando los índices definidos
        self.extract_feature_points(face_points, feature_indices)
        # Retorna el diccionario con los puntos de la boca
        return self.points['mouth']


# Clase para dibujar la malla facial sobre la imagen
class FaceMeshDrawer:
    # Constructor que inicializa el color y estilo de dibujo
    def __init__(self, color: Tuple[int, int, int] = (255, 255, 0)):
        # Obtiene las utilidades de dibujo de MediaPipe
        self.mp_draw = mp.solutions.drawing_utils
        # Configura el estilo de dibujo: color cian (255, 255, 0), grosor 1, radio de círculo 1
        self.config_draw = self.mp_draw.DrawingSpec(color=color, thickness=1, circle_radius=1)

    # Dibuja la malla facial sobre la imagen
    def draw(self, face_image: np.ndarray, face_mesh_info: Any):
        # Itera sobre cada rostro detectado en la imagen
        for face_mesh in face_mesh_info.multi_face_landmarks:
            # Dibuja los puntos y conexiones de la malla facial usando la teselación de MediaPipe
            self.mp_draw.draw_landmarks(face_image, face_mesh, mp.solutions.face_mesh.FACEMESH_TESSELATION,
                                        self.config_draw, self.config_draw)  # Aplica la configuración de estilo


# Clase principal que coordina todo el procesamiento de malla facial
class FaceMeshProcessor:
    # Constructor que inicializa los componentes de inferencia, extracción y dibujo
    def __init__(self):
        # Crea una instancia para realizar la inferencia de malla facial
        self.inference = FaceMeshInference()
        # Crea una instancia para extraer puntos específicos de características
        self.extractor = FaceMeshExtractor()
        # Crea una instancia para dibujar la malla facial
        self.drawer = FaceMeshDrawer()

    # Método principal que procesa una imagen facial completa
    def process(self, face_image: np.ndarray, draw: bool = True) -> Tuple[dict, bool, np.ndarray]:
        # Guarda una copia de la imagen original para retornar si no se dibuja
        original_image = face_image.copy()
        # Realiza la inferencia para detectar la malla facial
        success, face_mesh_info = self.inference.process(face_image)
        # Si no se detectó ningún rostro, retorna diccionario vacío y la imagen original
        if not success:
            return {}, False, original_image

        # Extrae todos los puntos de la malla facial
        face_points = self.extractor.extract_points(face_image, face_mesh_info)
        # Organiza los puntos por características faciales (cejas, ojos, nariz, boca)
        points = {
            'eyebrows': self.extractor.get_eyebrows_points(face_points),  # Extrae puntos de cejas
            'eyes': self.extractor.get_eyes_points(face_points),  # Extrae puntos de ojos
            'nose': self.extractor.get_nose_points(face_points),  # Extrae puntos de nariz
            'mouth': self.extractor.get_mouth_points(face_points)  # Extrae puntos de boca
        }

        # Si se solicita dibujar la malla
        if draw:
            # Dibuja la malla facial sobre la imagen
            self.drawer.draw(face_image, face_mesh_info)
            # Retorna los puntos, éxito y la imagen con la malla dibujada
            return points, True, face_image

        # Si no se dibuja, retorna los puntos, éxito y la imagen original sin modificar
        return points, True, original_image
