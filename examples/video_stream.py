# Importa módulo os para operaciones del sistema operativo
import os
# Importa módulo sys para manipular el path de Python
import sys
# Importa OpenCV para mostrar video
import cv2
# Agrega el directorio padre al path para poder importar emotion_processor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Importa el sistema de reconocimiento de emociones
from emotion_processor.main import EmotionRecognitionSystem
# Importa la clase Camera para captura de video
from camera import Camera


# Clase para manejar el stream de video con reconocimiento de emociones en tiempo real
class VideoStream:
    # Constructor que inicializa la cámara y el sistema de reconocimiento
    def __init__(self, cam: Camera, emotion_recognition_system: EmotionRecognitionSystem):
        # Almacena la instancia de la cámara
        self.camera = cam
        # Almacena la instancia del sistema de reconocimiento de emociones
        self.emotion_recognition_system = emotion_recognition_system

    # Método principal que ejecuta el loop de procesamiento de video
    def run(self):
        # Loop infinito para procesar frames continuamente
        while True:
            # Lee un frame de la cámara
            ret, frame = self.camera.read()
            # Si se capturó un frame exitosamente
            if ret:
                # Procesa el frame para detectar y visualizar emociones
                frame = self.emotion_recognition_system.frame_processing(frame)
                # Muestra el frame procesado en una ventana
                cv2.imshow('Emotion Recognition', frame)
                # Espera 5ms por una tecla presionada
                t = cv2.waitKey(5)
                # Si se presiona ESC (código 27), sale del loop
                if t == 27:
                    break

            else:
                # Si no se pudo capturar el frame, lanza una excepción (nota: no se captura)
                Exception(f"No cam connected")
        # Libera los recursos de la cámara
        self.camera.release()
        # Cierra todas las ventanas de OpenCV
        cv2.destroyAllWindows()


# Punto de entrada del programa
if __name__ == "__main__":
    # Crea una instancia de cámara (índice 0, resolución 1280x720)
    camera = Camera(0, 1280, 720)
    # Crea una instancia del sistema de reconocimiento de emociones
    emotion_recognition_system = EmotionRecognitionSystem()
    # Crea una instancia del stream de video
    video_stream = VideoStream(camera, emotion_recognition_system)
    # Ejecuta el stream de video
    video_stream.run()


