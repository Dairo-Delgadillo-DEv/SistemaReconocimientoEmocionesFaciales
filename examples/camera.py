# Importa OpenCV para captura de video desde cámara
import cv2


# Clase para manejar la captura de video desde una cámara
class Camera:
    # Constructor que inicializa la cámara con índice y resolución específicos
    def __init__(self, index: int, width: int, height: int):
        # Crea un objeto de captura de video usando el índice de la cámara
        self.cap = cv2.VideoCapture(index)
        # Establece el ancho del frame (propiedad 3 de OpenCV)
        self.cap.set(3, width)
        # Establece la altura del frame (propiedad 4 de OpenCV)
        self.cap.set(4, height)

    # Lee un frame de la cámara
    def read(self):
        # Captura un frame y retorna el estado de éxito y el frame
        ret, frame = self.cap.read()
        return ret, frame

    # Libera los recursos de la cámara
    def release(self):
        # Libera el objeto de captura de video
        self.cap.release()
