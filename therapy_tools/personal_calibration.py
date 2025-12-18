# Sistema de calibración personal para ajustar el reconocimiento emocional
# a las características expresivas únicas de cada paciente

import numpy as np
import json
import time
import cv2
import os
import sys

# Agregar el directorio padre al path para poder importar emotion_processor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class PersonalCalibration:
    """
    Calibra el sistema para cada paciente individual.
    
    Proceso de calibración (5-10 minutos):
    1. Capturar estado neutral (30 segundos)
    2. Capturar cada emoción básica (10 segundos cada una)
    3. Calcular rangos personalizados
    4. Ajustar umbrales del sistema
    
    ¿Por qué es necesario?
    - Variabilidad individual: Algunas personas son muy expresivas, otras más contenidas
    - Diferencias culturales: Distintas culturas tienen expresiones diferentes
    - Neurodivergencia: Personas con autismo pueden tener expresiones atípicas
    - "Resting face": Algunas personas tienen cara de enojado/triste en estado neutral
    - Rango expresivo: Unos tienen sonrisas enormes, otros apenas mueven los labios
    """
    
    def __init__(self, emotion_recognition_system=None):
        """
        Inicializa el sistema de calibración.
        
        Args:
            emotion_recognition_system: Instancia del sistema de reconocimiento de emociones
        """
        self.emotion_system = emotion_recognition_system
        
        # Almacena líneas base personalizadas
        self.baseline_emotions = {
            'neutral': {},
            'happy': {},
            'sad': {},
            'angry': {},
            'fear': {},
            'surprise': {},
            'disgust': {}
        }
        
        # Rangos personalizados (min-max para cada emoción)
        self.personal_ranges = {}
        
        # Factores de ajuste
        self.adjustment_factors = {}
        
        # Emociones a calibrar
        self.emotions_to_calibrate = [
            ('happy', 'Felicidad', 'Sonría ampliamente, como si algo muy bueno hubiera pasado'),
            ('sad', 'Tristeza', 'Ponga cara triste, como si recibiera malas noticias'),
            ('angry', 'Enojo', 'Frunza el ceño y apriete la mandíbula, como si estuviera molesto'),
            ('fear', 'Miedo', 'Abra los ojos ampliamente, como si se asustara'),
            ('surprise', 'Sorpresa', 'Abra la boca y los ojos, como si algo inesperado pasara'),
            ('disgust', 'Disgusto', 'Arrugue la nariz, como si oliera algo desagradable')
        ]
    
    def start_calibration_wizard(self, camera, patient_id):
        """
        Asistente interactivo de calibración.
        
        ¿Cómo funciona?
        - Muestra instrucciones en pantalla
        - Guía al paciente paso a paso
        - Captura datos mientras el paciente expresa cada emoción
        - Calcula automáticamente los ajustes necesarios
        
        Args:
            camera: Instancia de la cámara
            patient_id: ID del paciente para guardar calibración
        """
        print("=" * 60)
        print("CALIBRACIÓN PERSONAL DEL SISTEMA")
        print("=" * 60)
        print("\nEste proceso tomará aproximadamente 5-7 minutos.")
        print("Por favor, siga las instrucciones en pantalla.\n")
        input("Presione ENTER cuando esté listo para comenzar...")
        
        # PASO 1: Calibrar estado neutral
        print("\n PASO 1/7: Estado Neutral")
        print("Por favor, mantenga una expresión facial relajada y neutral.")
        print("No sonría, no frunza el ceño, solo relájese.")
        self.calibrate_neutral(camera, duration=30)
        
        # PASO 2-7: Calibrar cada emoción
        for i, (emotion_key, emotion_name, instruction) in enumerate(self.emotions_to_calibrate, 2):
            print(f"\n PASO {i}/7: {emotion_name}")
            print(f"Instrucción: {instruction}")
            input("Presione ENTER cuando esté listo...")
            self.calibrate_emotion(camera, emotion_key, duration=10)
        
        # PASO FINAL: Calcular ajustes
        print("\nCalculando ajustes personalizados...")
        self.calculate_adjustment_factors()
        
        # Guardar calibración
        self.save_calibration(patient_id)
        
        print("\n¡Calibración completada!")
        print(f"El sistema ahora está personalizado para el paciente {patient_id}")
        print("\nResumen de calibración:")
        self.print_calibration_summary()
    
    def calibrate_neutral(self, camera, duration=30):
        """
        Captura el estado neutral del paciente.
        
        ¿Por qué es importante?
        - Establece la línea base de comparación
        - Identifica la "cara de descanso" del paciente
        - Permite detectar desviaciones de lo normal
        
        Args:
            camera: Instancia de la cámara
            duration: Duración de la captura en segundos
        """
        print(f"Capturando durante {duration} segundos...")
        
        samples = []
        start_time = time.time()
        countdown_shown = set()
        
        while time.time() - start_time < duration:
            ret, frame = camera.read()
            if not ret:
                continue
            
            # Procesar frame
            try:
                emotions = self._get_emotions_from_frame(frame)
                if emotions:
                    samples.append(emotions)
            except Exception as e:
                pass
            
            # Mostrar countdown
            remaining = int(duration - (time.time() - start_time))
            if remaining not in countdown_shown and remaining <= 10:
                print(f"  {remaining} segundos restantes...")
                countdown_shown.add(remaining)
            
            # Mostrar video con overlay
            cv2.putText(frame, "ESTADO NEUTRAL - Mantenga expresion relajada", 
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Tiempo restante: {remaining}s", 
                       (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Calibracion', frame)
            cv2.waitKey(1)
        
        cv2.destroyAllWindows()
        
        # Calcular promedios
        if samples:
            self.baseline_emotions['neutral'] = {
                emotion: np.mean([s[emotion] for s in samples])
                for emotion in samples[0].keys()
            }
            print(f"  Capturados {len(samples)} muestras de estado neutral")
        else:
            print("  No se pudieron capturar muestras. Intente de nuevo.")
    
    def calibrate_emotion(self, camera, emotion_key, duration=10):
        """
        Captura una emoción específica expresada por el paciente.
        
        ¿Qué se mide?
        - Intensidad máxima que el paciente puede expresar
        - Características faciales específicas de su expresión
        - Variabilidad en su expresión de esa emoción
        
        Args:
            camera: Instancia de la cámara
            emotion_key: Clave de la emoción a calibrar
            duration: Duración de la captura
        """
        print(f"  Exprese {emotion_key} durante {duration} segundos...")
        
        samples = []
        start_time = time.time()
        countdown_shown = set()
        
        while time.time() - start_time < duration:
            ret, frame = camera.read()
            if not ret:
                continue
            
            try:
                emotions = self._get_emotions_from_frame(frame)
                if emotions:
                    samples.append(emotions)
            except:
                pass
            
            remaining = int(duration - (time.time() - start_time))
            if remaining not in countdown_shown and remaining <= 5:
                print(f"    {remaining} segundos...")
                countdown_shown.add(remaining)
            
            # Mostrar video con overlay
            cv2.putText(frame, f"EXPRESE: {emotion_key.upper()}", 
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, f"Tiempo restante: {remaining}s", 
                       (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.imshow('Calibracion', frame)
            cv2.waitKey(1)
        
        cv2.destroyAllWindows()
        
        if samples:
            self.baseline_emotions[emotion_key] = {
                emotion: np.mean([s[emotion] for s in samples])
                for emotion in samples[0].keys()
            }
            print(f"    Capturados {len(samples)} muestras de {emotion_key}")
        else:
            print(f"    No se pudieron capturar muestras de {emotion_key}")
    
    def calculate_adjustment_factors(self):
        """
        Calcula factores de ajuste basados en calibración.
        
        ¿Cómo funciona?
        1. Compara neutral vs. cada emoción
        2. Calcula el rango personal (diferencia entre neutral y máximo)
        3. Crea factores de escala para normalizar
        
        Ejemplo:
        - Paciente A: neutral=20%, feliz=95% -> rango=75%
        - Paciente B: neutral=5%, feliz=45% -> rango=40%
        - Factor de ajuste para B: 75/40 = 1.875
        - Ahora 45% de B se escala a 84%, comparable con A
        """
        neutral = self.baseline_emotions.get('neutral', {})
        
        for emotion in ['happy', 'sad', 'angry', 'fear', 'surprise', 'disgust']:
            if emotion in self.baseline_emotions and self.baseline_emotions[emotion]:
                # Calcular rango personal
                neutral_value = neutral.get(emotion, 0)
                max_value = self.baseline_emotions[emotion].get(emotion, 0)
                personal_range = max_value - neutral_value
                
                # Rango "estándar" esperado (basado en población general)
                standard_range = 70  # Asumimos que el rango típico es 70%
                
                # Factor de ajuste
                if personal_range > 0:
                    adjustment_factor = standard_range / personal_range
                else:
                    adjustment_factor = 1.0
                
                self.adjustment_factors[emotion] = {
                    'neutral_baseline': neutral_value,
                    'max_observed': max_value,
                    'personal_range': personal_range,
                    'scale_factor': min(adjustment_factor, 3.0)  # Limitar factor máximo
                }
                
                self.personal_ranges[emotion] = {
                    'min': neutral_value,
                    'max': max_value
                }
    
    def adjust_emotion_score(self, emotion, raw_score):
        """
        Ajusta una puntuación de emoción usando calibración personal.
        
        Esta función se llama en tiempo real durante las sesiones.
        
        ¿Qué hace?
        1. Resta la línea base neutral
        2. Escala según el rango personal
        3. Limita entre 0-100
        
        Args:
            emotion: Nombre de la emoción
            raw_score: Puntuación original del sistema
            
        Returns:
            float: Puntuación ajustada
        """
        if emotion not in self.adjustment_factors:
            return raw_score  # Sin calibración, retornar valor original
        
        factors = self.adjustment_factors[emotion]
        
        # Restar línea base neutral
        adjusted = raw_score - factors['neutral_baseline']
        
        # Escalar según rango personal
        adjusted = adjusted * factors['scale_factor']
        
        # Limitar entre 0-100
        adjusted = max(0, min(100, adjusted))
        
        return adjusted
    
    def adjust_all_emotions(self, emotions_dict):
        """
        Ajusta todas las emociones en un diccionario.
        
        Args:
            emotions_dict: Diccionario con puntuaciones de emociones
            
        Returns:
            dict: Diccionario con puntuaciones ajustadas
        """
        adjusted = {}
        for emotion, score in emotions_dict.items():
            adjusted[emotion] = self.adjust_emotion_score(emotion, score)
        return adjusted
    
    def save_calibration(self, patient_id):
        """
        Guarda calibración para uso futuro.
        
        Args:
            patient_id: ID del paciente
        """
        calibration_data = {
            'patient_id': patient_id,
            'calibration_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'baseline_emotions': self.baseline_emotions,
            'adjustment_factors': self.adjustment_factors,
            'personal_ranges': self.personal_ranges
        }
        
        filename = f"calibration_{patient_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(calibration_data, f, indent=2, ensure_ascii=False)
        
        print(f"  Calibración guardada en: {filename}")
    
    def load_calibration(self, patient_id):
        """
        Carga calibración guardada previamente.
        
        Args:
            patient_id: ID del paciente
            
        Returns:
            bool: True si se cargó exitosamente, False si no
        """
        filename = f"calibration_{patient_id}.json"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                calibration_data = json.load(f)
            
            self.baseline_emotions = calibration_data['baseline_emotions']
            self.adjustment_factors = calibration_data['adjustment_factors']
            self.personal_ranges = calibration_data['personal_ranges']
            
            print(f"Calibración cargada para paciente {patient_id}")
            return True
        except FileNotFoundError:
            print(f"No se encontró calibración para {patient_id}")
            return False
        except Exception as e:
            print(f"Error cargando calibración: {e}")
            return False
    
    def print_calibration_summary(self):
        """Muestra resumen de la calibración"""
        print("\n" + "=" * 60)
        print("RESUMEN DE CALIBRACIÓN PERSONAL")
        print("=" * 60)
        
        for emotion, factors in self.adjustment_factors.items():
            print(f"\n{emotion.upper()}:")
            print(f"  Línea base neutral: {factors['neutral_baseline']:.1f}%")
            print(f"  Máximo observado: {factors['max_observed']:.1f}%")
            print(f"  Rango personal: {factors['personal_range']:.1f}%")
            print(f"  Factor de escala: {factors['scale_factor']:.2f}x")
    
    def _get_emotions_from_frame(self, frame):
        """
        Helper: Obtiene emociones de un frame.
        
        Args:
            frame: Frame de imagen
            
        Returns:
            dict: Diccionario con puntuaciones de emociones, o None si falla
        """
        if self.emotion_system:
            try:
                # Procesar frame
                self.emotion_system.frame_processing(frame)
                # Obtener últimas emociones detectadas
                emotions = self.emotion_system.emotions_recognition.last_emotions
                return emotions
            except:
                return None
        return None
    
    def is_calibrated(self):
        """
        Verifica si hay una calibración activa.
        
        Returns:
            bool: True si hay calibración, False si no
        """
        return len(self.adjustment_factors) > 0


class CalibratedEmotionRecognitionSystem:
    """
    Versión del sistema de reconocimiento de emociones que usa calibración personal.
    
    Este es un wrapper sobre el sistema original que aplica ajustes de calibración
    a las emociones detectadas.
    """
    
    def __init__(self, base_system, patient_id=None):
        """
        Inicializa el sistema calibrado.
        
        Args:
            base_system: Instancia de EmotionRecognitionSystem
            patient_id: ID del paciente para cargar calibración
        """
        self.base_system = base_system
        self.calibration = PersonalCalibration(base_system)
        self.last_calibrated_emotions = {}
        
        # Intentar cargar calibración existente
        if patient_id:
            self.calibration.load_calibration(patient_id)
    
    def frame_processing(self, face_image):
        """
        Procesa frame aplicando calibración personal.
        
        Args:
            face_image: Imagen del frame a procesar
            
        Returns:
            numpy.ndarray: Imagen procesada con visualización de emociones
        """
        # Procesamiento normal
        result = self.base_system.frame_processing(face_image)
        
        # Aplicar ajustes de calibración si existen
        if self.calibration.is_calibrated():
            try:
                # Obtener emociones originales
                original_emotions = self.base_system.emotions_recognition.last_emotions
                
                # Ajustar cada emoción
                self.last_calibrated_emotions = self.calibration.adjust_all_emotions(
                    original_emotions
                )
                
                # Actualizar visualización con emociones ajustadas
                result = self.base_system.emotions_visualization.main(
                    self.last_calibrated_emotions, 
                    result
                )
            except Exception as e:
                pass
        
        return result
    
    def run_calibration(self, camera, patient_id):
        """
        Ejecuta el proceso de calibración.
        
        Args:
            camera: Instancia de la cámara
            patient_id: ID del paciente
        """
        self.calibration.start_calibration_wizard(camera, patient_id)
    
    def get_calibrated_emotions(self):
        """
        Obtiene las últimas emociones calibradas.
        
        Returns:
            dict: Diccionario con emociones ajustadas
        """
        return self.last_calibrated_emotions
