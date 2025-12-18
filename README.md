# Módulo de Herramientas Terapéuticas

## Descripción

Este módulo proporciona herramientas clínicas y psiquiátricas para complementar el sistema de reconocimiento de emociones faciales. Está diseñado para uso en contextos terapéuticos profesionales.

## Componentes

### 1. Base de Datos de Sesiones (`session_database.py`)

Almacenamiento persistente para sesiones terapéuticas usando SQLite.

**Características:**
- Registro de sesiones con datos de paciente anonimizado
- Almacenamiento de snapshots de emociones cada segundo
- Resultados de ejercicios terapéuticos
- Estadísticas y análisis de sesiones

**Uso básico:**
```python
from therapy_tools.session_database import SessionDatabase

db = SessionDatabase()
session_id = db.start_session("PAC_123", "seguimiento")
db.save_emotion_snapshot(session_id, timestamp, emotions)
db.end_session(session_id, notes="Notas del terapeuta")
```

---

### 2. Dashboard del Terapeuta (`therapist_dashboard.py`)

Interfaz visual para análisis de sesiones con gráficos y estadísticas.

**Características:**
- Gráficos de evolución emocional durante sesiones
- Comparación entre sesiones
- Historial del paciente
- Estadísticas de ejercicios terapéuticos

**Uso básico:**
```python
from therapy_tools.therapist_dashboard import TherapistDashboard

dashboard = TherapistDashboard(database)
dashboard.show_session_summary(session_id)
dashboard.compare_sessions(session1, session2)
dashboard.show_patient_history(patient_id)
dashboard.run()
```

---

### 3. Gestión de Privacidad (`privacy_manager.py`)

Sistema completo de protección de datos y cumplimiento normativo.

**Características:**
- Consentimiento informado interactivo
- Anonimización de ID de pacientes (SHA-256)
- Encriptación de datos sensibles (Fernet/base64)
- Registro de auditoría de accesos
- Exportación de datos (GDPR Art. 15)
- Eliminación de datos (GDPR Art. 17)
- Política de retención de datos

**Uso básico:**
```python
from therapy_tools.privacy_manager import PrivacyManager

privacy = PrivacyManager()
consintio = privacy.request_consent("Juan Pérez")
patient_id = privacy.anonymize_patient_id("Juan Pérez", "1990-01-15")
encrypted = privacy.encrypt_sensitive_data("datos sensibles")
privacy.log_access('VIEW_SESSION', patient_id, 'detalles')
```

---

### 4. Calibración Personal (`personal_calibration.py`)

Ajusta el sistema a las características expresivas únicas de cada paciente.

**Características:**
- Asistente de calibración paso a paso
- Captura de estado neutral y cada emoción
- Cálculo de factores de ajuste personalizados
- Guardado/carga de calibración por paciente

**Uso básico:**
```python
from therapy_tools.personal_calibration import PersonalCalibration, CalibratedEmotionRecognitionSystem

calibration = PersonalCalibration(emotion_system)
calibration.start_calibration_wizard(camera, patient_id)
calibration.load_calibration(patient_id)
adjusted = calibration.adjust_emotion_score('happy', raw_score)
```

---

### 5. Ejercicios Terapéuticos (`therapeutic_exercises.py`)

Biblioteca de ejercicios con biofeedback emocional en tiempo real.

**Ejercicios disponibles:**
1. **Respiración 4-7-8** - Reducción rápida de ansiedad
2. **Grounding 5-4-3-2-1** - Ataques de pánico, disociación
3. **Relajación Muscular Progresiva** - Tensión muscular crónica
4. **Respiración Consciente (Mindfulness)** - Estrés, rumiación

**Uso básico:**
```python
from therapy_tools.therapeutic_exercises import TherapeuticExercises

exercises = TherapeuticExercises(emotion_system, camera)
exercises.list_exercises()
results = exercises.start_exercise('breathing_478')
print(f"Reducción: {results['reduction']:.1f}%")
```

---

## Archivos de Ejemplo

### `examples/therapy_video_stream.py`
Stream de video terapéutico completo que integra todos los componentes:
- Consentimiento informado automático
- Anonimización de pacientes
- Calibración opcional
- Registro de sesión en base de datos
- Menú de ejercicios terapéuticos

### `examples/therapy_examples.py`
Ejemplos simples de cada componente para aprender a usar el módulo.

---

## Requisitos Adicionales

El módulo funciona con las dependencias existentes del proyecto, pero opcionalmente puede agregar:

```
cryptography  # Para encriptación avanzada (opcional, hay fallback a base64)
```

---

## Consideraciones Éticas y Legales

⚠️ **IMPORTANTE:**

1. **No es diagnóstico médico** - Este sistema es una herramienta de apoyo, no reemplaza el juicio clínico profesional.

2. **Consentimiento informado** - Siempre debe obtenerse antes de usar el sistema con pacientes.

3. **Protección de datos** - Cumplir con GDPR, HIPAA y regulaciones locales de privacidad.

4. **Uso supervisado** - Solo debe ser operado por profesionales de salud mental licenciados.

5. **Limitaciones técnicas** - El sistema tiene limitaciones de precisión y variabilidad entre individuos.

---

## Estructura del Módulo

```
therapy_tools/
├── __init__.py              # Exporta todos los componentes
├── session_database.py      # Base de datos SQLite
├── therapist_dashboard.py   # Visualización con Tkinter/Matplotlib
├── privacy_manager.py       # Privacidad y cumplimiento GDPR
├── personal_calibration.py  # Calibración por paciente
└── therapeutic_exercises.py # Ejercicios con biofeedback
```

---

## Licencia

Este módulo está diseñado para uso terapéutico profesional. El uso en contexto clínico debe cumplir con todas las regulaciones locales de salud mental y privacidad de datos.
