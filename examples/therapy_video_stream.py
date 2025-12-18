# Video stream terapéutico con integración de herramientas clínicas
# Versión extendida de video_stream.py para uso en sesiones de terapia

import os
import sys
import cv2
import time

# Agregar el directorio padre al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from emotion_processor.main import EmotionRecognitionSystem
from camera import Camera

# Importar herramientas terapéuticas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from therapy_tools.session_database import SessionDatabase
from therapy_tools.privacy_manager import PrivacyManager
from therapy_tools.personal_calibration import PersonalCalibration, CalibratedEmotionRecognitionSystem
from therapy_tools.therapeutic_exercises import TherapeuticExercises


class TherapyVideoStream:
    """
    Stream de video terapéutico con funcionalidades clínicas.
    
    Funcionalidades:
    - Registro automático de emociones durante la sesión
    - Consentimiento informado antes de iniciar
    - Anonimización de datos del paciente
    - Calibración personal del sistema
    - Integración con ejercicios terapéuticos
    - Guardado de sesión en base de datos
    """
    
    def __init__(self, cam: Camera, emotion_recognition_system: EmotionRecognitionSystem,
                 patient_name: str, birth_date: str, session_type: str = 'regular'):
        """
        Inicializa el stream de video terapéutico.
        
        Args:
            cam: Instancia de la cámara
            emotion_recognition_system: Sistema de reconocimiento de emociones
            patient_name: Nombre del paciente (se anonimizará)
            birth_date: Fecha de nacimiento del paciente (formato: YYYY-MM-DD)
            session_type: Tipo de sesión (inicial, seguimiento, etc.)
        """
        self.camera = cam
        self.emotion_recognition_system = emotion_recognition_system
        self.session_type = session_type
        
        # Inicializar herramientas terapéuticas
        self.db = SessionDatabase()
        self.privacy = PrivacyManager()
        self.calibration = PersonalCalibration(emotion_recognition_system)
        
        # Solicitar consentimiento
        self.consent_given = self._request_consent(patient_name)
        
        if self.consent_given:
            # Anonimizar ID del paciente
            self.patient_id = self.privacy.anonymize_patient_id(patient_name, birth_date)
            print(f"  ID anónimo del paciente: {self.patient_id}")
            
            # Intentar cargar calibración existente
            if not self.calibration.load_calibration(self.patient_id):
                print("  No hay calibración previa. Considere ejecutar calibración.")
            
            # Variables de sesión
            self.session_id = None
            self.start_time = None
            self.last_save_time = 0
            self.save_interval = 1  # Guardar emociones cada segundo
        else:
            print("  Consentimiento rechazado. No se puede iniciar sesión.")
            self.patient_id = None
    
    def _request_consent(self, patient_name):
        """
        Solicita consentimiento informado al paciente.
        
        Args:
            patient_name: Nombre del paciente
            
        Returns:
            bool: True si acepta, False si rechaza
        """
        print("\n  Solicitando consentimiento informado...")
        return self.privacy.request_consent(patient_name)
    
    def run_calibration(self):
        """Ejecuta el proceso de calibración personal"""
        if not self.consent_given or not self.patient_id:
            print("  No se puede calibrar sin consentimiento.")
            return False
        
        print("\n  Iniciando calibración personal...")
        self.calibration.start_calibration_wizard(self.camera, self.patient_id)
        return True
    
    def run(self):
        """
        Ejecuta el stream de video terapéutico.
        
        Registra emociones automáticamente durante toda la sesión.
        """
        if not self.consent_given or not self.patient_id:
            print("  No se puede iniciar sesión sin consentimiento.")
            return
        
        # Iniciar sesión en la base de datos
        self.session_id = self.db.start_session(self.patient_id, self.session_type)
        self.start_time = time.time()
        
        print(f"\n  Sesión iniciada (ID: {self.session_id})")
        print("  Presione ESC para terminar la sesión.\n")
        
        # Registrar inicio
        self.privacy.log_access('START_SESSION', self.patient_id, 
                               f'Session {self.session_id} started')
        
        try:
            while True:
                ret, frame = self.camera.read()
                if ret:
                    # Procesar frame
                    frame = self.emotion_recognition_system.frame_processing(frame)
                    
                    # Guardar emociones periódicamente
                    current_time = time.time()
                    if current_time - self.last_save_time >= self.save_interval:
                        self._save_current_emotions()
                        self.last_save_time = current_time
                    
                    # Mostrar información de sesión
                    elapsed = int(current_time - self.start_time)
                    elapsed_min = elapsed // 60
                    elapsed_sec = elapsed % 60
                    
                    cv2.putText(frame, f"Sesion: {elapsed_min:02d}:{elapsed_sec:02d}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    cv2.imshow('Therapy Session', frame)
                    
                    if cv2.waitKey(5) == 27:  # ESC
                        break
                else:
                    print("  Error: No se pudo capturar frame de la cámara")
                    break
        
        finally:
            # Finalizar sesión
            self._end_session()
    
    def _save_current_emotions(self):
        """Guarda las emociones actuales en la base de datos"""
        try:
            emotions = self.emotion_recognition_system.emotions_recognition.last_emotions
            
            # Aplicar calibración si existe
            if self.calibration.is_calibrated():
                emotions = self.calibration.adjust_all_emotions(emotions)
            
            timestamp_offset = int(time.time() - self.start_time)
            self.db.save_emotion_snapshot(self.session_id, timestamp_offset, emotions)
        except Exception as e:
            pass  # Silenciar errores de guardado para no interrumpir sesión
    
    def _end_session(self, notes=''):
        """
        Finaliza la sesión de terapia.
        
        Args:
            notes: Notas opcionales del terapeuta
        """
        self.camera.release()
        cv2.destroyAllWindows()
        
        if self.session_id:
            self.db.end_session(self.session_id, notes)
            self.privacy.log_access('END_SESSION', self.patient_id, 
                                   f'Session {self.session_id} ended')
            
            # Mostrar resumen
            stats = self.db.get_session_statistics(self.session_id)
            if stats:
                print("\n" + "=" * 60)
                print("RESUMEN DE SESIÓN")
                print("=" * 60)
                print(f"  Duración: {stats['duration_seconds'] // 60} minutos")
                print(f"  Emoción dominante: {stats['dominant_emotion']}")
                print(f"  ID de sesión: {self.session_id}")
                print("=" * 60)
    
    def run_exercise(self, exercise_key):
        """
        Ejecuta un ejercicio terapéutico.
        
        Args:
            exercise_key: Clave del ejercicio a ejecutar
            
        Returns:
            dict: Resultados del ejercicio
        """
        if not self.consent_given:
            print("  No se puede ejecutar ejercicio sin consentimiento.")
            return None
        
        exercises = TherapeuticExercises(self.emotion_recognition_system, self.camera)
        results = exercises.start_exercise(exercise_key)
        
        # Guardar resultados en base de datos
        if results:
            self.db.save_exercise_results(self.patient_id, results, self.session_id)
        
        return results
    
    def list_exercises(self):
        """Muestra la lista de ejercicios disponibles"""
        exercises = TherapeuticExercises(self.emotion_recognition_system, self.camera)
        exercises.list_exercises()


def main():
    """Punto de entrada principal para el stream terapéutico"""
    print("=" * 60)
    print("SISTEMA DE RECONOCIMIENTO EMOCIONAL - MODO TERAPÉUTICO")
    print("=" * 60)
    
    # Solicitar datos del paciente
    print("\nPor favor ingrese los datos del paciente:")
    patient_name = input("Nombre completo: ")
    birth_date = input("Fecha de nacimiento (YYYY-MM-DD): ")
    
    print("\nTipo de sesión:")
    print("1. Inicial")
    print("2. Seguimiento")
    print("3. Evaluación")
    print("4. Ejercicio terapéutico")
    session_choice = input("Seleccione (1-4): ")
    
    session_types = {
        '1': 'inicial',
        '2': 'seguimiento',
        '3': 'evaluacion',
        '4': 'ejercicio'
    }
    session_type = session_types.get(session_choice, 'seguimiento')
    
    # Inicializar componentes
    camera = Camera(0, 1280, 720)
    emotion_system = EmotionRecognitionSystem()
    
    # Crear stream terapéutico
    therapy_stream = TherapyVideoStream(
        camera, emotion_system, 
        patient_name, birth_date, 
        session_type
    )
    
    if not therapy_stream.consent_given:
        print("\nSesión cancelada por falta de consentimiento.")
        return
    
    # Menú de opciones
    while True:
        print("\n" + "=" * 40)
        print("OPCIONES:")
        print("1. Iniciar sesión de monitoreo")
        print("2. Ejecutar calibración personal")
        print("3. Ver ejercicios disponibles")
        print("4. Ejecutar ejercicio de respiración 4-7-8")
        print("5. Ejecutar ejercicio de grounding 5-4-3-2-1")
        print("6. Ejecutar relajación progresiva")
        print("7. Ejecutar mindfulness")
        print("8. Salir")
        print("=" * 40)
        
        choice = input("Seleccione una opción: ")
        
        if choice == '1':
            therapy_stream.run()
            break
        elif choice == '2':
            therapy_stream.run_calibration()
        elif choice == '3':
            therapy_stream.list_exercises()
        elif choice == '4':
            therapy_stream.run_exercise('breathing_478')
        elif choice == '5':
            therapy_stream.run_exercise('grounding_54321')
        elif choice == '6':
            therapy_stream.run_exercise('progressive_relaxation')
        elif choice == '7':
            therapy_stream.run_exercise('mindfulness_breathing')
        elif choice == '8':
            print("\nSesión finalizada.")
            break
        else:
            print("Opción no válida.")
    
    # Cerrar base de datos
    therapy_stream.db.close()


if __name__ == "__main__":
    main()
