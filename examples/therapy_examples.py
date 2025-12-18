# Ejemplo de uso de las herramientas terapéuticas
# Este archivo muestra cómo usar cada componente del módulo therapy_tools

"""
EJEMPLO DE USO DE HERRAMIENTAS TERAPÉUTICAS
============================================

Este archivo demuestra cómo utilizar las herramientas clínicas/psiquiátricas
implementadas en el módulo therapy_tools.

Componentes disponibles:
1. SessionDatabase - Base de datos para sesiones terapéuticas
2. TherapistDashboard - Dashboard visual para análisis
3. PrivacyManager - Gestión de privacidad y consentimiento
4. PersonalCalibration - Calibración del sistema para cada paciente
5. TherapeuticExercises - Ejercicios terapéuticos con biofeedback

REQUISITOS:
- Python 3.10+
- OpenCV
- NumPy
- Matplotlib (opcional, para gráficos)
- Tkinter (incluido en Python estándar)
- cryptography (opcional, para encriptación avanzada)
"""

import os
import sys

# Agregar el directorio padre al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ============================================================
# EJEMPLO 1: Base de datos de sesiones
# ============================================================
def ejemplo_base_datos():
    """
    Demuestra el uso de la base de datos de sesiones.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 1: BASE DE DATOS DE SESIONES")
    print("=" * 60)
    
    from therapy_tools.session_database import SessionDatabase
    
    # Crear/conectar a la base de datos
    db = SessionDatabase('ejemplo_sesiones.db')
    print("Base de datos creada/conectada")
    
    # Iniciar una nueva sesión
    patient_id = "PAC_ejemplo123"
    session_id = db.start_session(patient_id, session_type='ejemplo')
    print(f"Sesión iniciada con ID: {session_id}")
    
    # Simular guardado de emociones
    emociones_ejemplo = {
        'happy': 65.5,
        'sad': 15.2,
        'angry': 8.3,
        'fear': 22.1,
        'surprise': 12.0,
        'disgust': 5.8
    }
    
    # Guardar varias snapshots
    for i in range(5):
        db.save_emotion_snapshot(session_id, i, emociones_ejemplo)
        print(f"  Snapshot {i+1} guardada")
    
    # Finalizar sesión
    db.end_session(session_id, notes="Sesión de prueba")
    print("Sesión finalizada")
    
    # Obtener historial del paciente
    sesiones = db.get_patient_sessions(patient_id)
    print(f"\nSesiones del paciente: {len(sesiones)}")
    
    # Obtener estadísticas
    stats = db.get_session_statistics(session_id)
    if stats:
        print(f"Emoción dominante: {stats['dominant_emotion']}")
    
    db.close()
    print("\nBase de datos cerrada")


# ============================================================
# EJEMPLO 2: Dashboard del terapeuta
# ============================================================
def ejemplo_dashboard():
    """
    Demuestra el uso del dashboard visual.
    NOTA: Requiere una sesión existente en la base de datos.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 2: DASHBOARD DEL TERAPEUTA")
    print("=" * 60)
    
    from therapy_tools.session_database import SessionDatabase
    from therapy_tools.therapist_dashboard import TherapistDashboard
    
    # Conectar a base de datos con datos
    db = SessionDatabase('ejemplo_sesiones.db')
    
    # Crear dashboard
    dashboard = TherapistDashboard(db)
    
    # Obtener una sesión existente
    sesiones = db.get_patient_sessions("PAC_ejemplo123", limit=1)
    
    if sesiones:
        session_id = sesiones[0][0]
        print(f"Mostrando resumen de sesión {session_id}")
        
        # Mostrar resumen (abre ventana de Tkinter)
        dashboard.show_session_summary(session_id)
        dashboard.run()
    else:
        print("No hay sesiones. Ejecute primero ejemplo_base_datos()")
    
    db.close()


# ============================================================
# EJEMPLO 3: Gestión de privacidad
# ============================================================
def ejemplo_privacidad():
    """
    Demuestra el uso del sistema de privacidad.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 3: GESTIÓN DE PRIVACIDAD")
    print("=" * 60)
    
    from therapy_tools.privacy_manager import PrivacyManager
    
    # Crear gestor de privacidad
    privacy = PrivacyManager()
    
    # Anonimizar ID de paciente
    patient_id = privacy.anonymize_patient_id("Juan Pérez", "1990-05-15")
    print(f"ID anónimo generado: {patient_id}")
    
    # Encriptar datos sensibles
    nota_sensible = "El paciente mostró signos de ansiedad severa"
    nota_encriptada = privacy.encrypt_sensitive_data(nota_sensible)
    print(f"Nota encriptada: {nota_encriptada[:50]}...")
    
    # Desencriptar
    nota_desencriptada = privacy.decrypt_sensitive_data(nota_encriptada)
    print(f"Nota desencriptada: {nota_desencriptada}")
    
    # Registrar acceso
    privacy.log_access('VIEW_EXAMPLE', patient_id, 'Ejemplo de acceso')
    print("Acceso registrado en log")
    
    # Obtener log de accesos
    log = privacy.get_access_log()
    print(f"Entradas en log: {len(log)}")


# ============================================================
# EJEMPLO 4: Solicitar consentimiento
# ============================================================
def ejemplo_consentimiento():
    """
    Demuestra el formulario de consentimiento informado.
    NOTA: Abre una ventana de Tkinter
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 4: CONSENTIMIENTO INFORMADO")
    print("=" * 60)
    
    from therapy_tools.privacy_manager import PrivacyManager
    
    privacy = PrivacyManager()
    
    print("Abriendo formulario de consentimiento...")
    consintio = privacy.request_consent("Paciente de Prueba")
    
    if consintio:
        print("El paciente ACEPTÓ el consentimiento")
    else:
        print("El paciente RECHAZÓ el consentimiento")


# ============================================================
# EJEMPLO 5: Calibración personal (requiere cámara)
# ============================================================
def ejemplo_calibracion():
    """
    Demuestra el sistema de calibración personal.
    NOTA: Requiere cámara conectada y sistema de reconocimiento.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 5: CALIBRACIÓN PERSONAL")
    print("=" * 60)
    print("\nEste ejemplo requiere una cámara conectada.")
    print("Consulte therapy_video_stream.py para ver la implementación completa.")
    
    # Código de ejemplo (no ejecutable sin cámara):
    """
    from examples.camera import Camera
    from emotion_processor.main import EmotionRecognitionSystem
    from therapy_tools.personal_calibration import PersonalCalibration
    
    camera = Camera(0, 1280, 720)
    emotion_system = EmotionRecognitionSystem()
    calibration = PersonalCalibration(emotion_system)
    
    # Ejecutar asistente de calibración
    calibration.start_calibration_wizard(camera, 'PAC_ejemplo123')
    
    # Cargar calibración en sesión posterior
    calibration.load_calibration('PAC_ejemplo123')
    
    # Ajustar emociones detectadas
    emociones_raw = {'happy': 45, 'sad': 30, ...}
    emociones_ajustadas = calibration.adjust_all_emotions(emociones_raw)
    """


# ============================================================
# EJEMPLO 6: Ejercicios terapéuticos (requiere cámara)
# ============================================================
def ejemplo_ejercicios():
    """
    Demuestra los ejercicios terapéuticos disponibles.
    NOTA: Requiere cámara conectada.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 6: EJERCICIOS TERAPÉUTICOS")
    print("=" * 60)
    print("\nEjercicios disponibles:")
    print("1. breathing_478 - Respiración 4-7-8")
    print("2. grounding_54321 - Grounding 5-4-3-2-1")
    print("3. progressive_relaxation - Relajación progresiva")
    print("4. mindfulness_breathing - Respiración consciente")
    print("\nConsulte therapy_video_stream.py para ver la implementación completa.")
    
    # Código de ejemplo (no ejecutable sin cámara):
    """
    from examples.camera import Camera
    from emotion_processor.main import EmotionRecognitionSystem
    from therapy_tools.therapeutic_exercises import TherapeuticExercises
    
    camera = Camera(0, 1280, 720)
    emotion_system = EmotionRecognitionSystem()
    exercises = TherapeuticExercises(emotion_system, camera)
    
    # Ver ejercicios disponibles
    exercises.list_exercises()
    
    # Ejecutar ejercicio de respiración
    resultados = exercises.start_exercise('breathing_478')
    
    # Ver resultados
    print(f"Reducción de ansiedad: {resultados['reduction']:.1f}%")
    """


# ============================================================
# MENÚ PRINCIPAL
# ============================================================
def main():
    """Menú principal de ejemplos"""
    while True:
        print("\n" + "=" * 60)
        print("EJEMPLOS DE HERRAMIENTAS TERAPÉUTICAS")
        print("=" * 60)
        print("1. Base de datos de sesiones")
        print("2. Dashboard del terapeuta (requiere sesión existente)")
        print("3. Gestión de privacidad")
        print("4. Consentimiento informado (abre ventana)")
        print("5. Calibración personal (info)")
        print("6. Ejercicios terapéuticos (info)")
        print("7. Salir")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            ejemplo_base_datos()
        elif opcion == '2':
            ejemplo_dashboard()
        elif opcion == '3':
            ejemplo_privacidad()
        elif opcion == '4':
            ejemplo_consentimiento()
        elif opcion == '5':
            ejemplo_calibracion()
        elif opcion == '6':
            ejemplo_ejercicios()
        elif opcion == '7':
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()
