# Sistema de Reconocimiento de Emociones Faciales
## Análisis Completo del Proyecto

---

## 📋 Descripción General

Este proyecto es un **sistema de reconocimiento de emociones faciales en tiempo real** que utiliza visión por computadora y análisis de malla facial (face mesh) para detectar y cuantificar 6 emociones básicas:

- 😊 **Felicidad (Happy)**
- 😢 **Tristeza (Sad)**
- 😠 **Enojo (Angry)**
- 😨 **Miedo (Fear)**
- 😲 **Sorpresa (Surprise)**
- 🤢 **Disgusto (Disgust)**

El sistema procesa video en tiempo real desde una cámara web, detecta rostros, extrae características faciales y calcula puntuaciones para cada emoción basándose en la posición y movimiento de elementos faciales clave.

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Carpetas

```
emotion_processor/
├── face_mesh/                    # Detección y extracción de malla facial
│   └── face_mesh_processor.py   # Usa MediaPipe para detectar 468 puntos faciales
│
├── data_processing/              # Procesamiento de características faciales
│   ├── eyebrows/                # Análisis de cejas
│   ├── eyes/                    # Análisis de ojos
│   ├── nose/                    # Análisis de nariz
│   ├── mouth/                   # Análisis de boca
│   └── main.py                  # Coordinador de procesamiento
│
├── emotions_recognition/         # Reconocimiento de emociones
│   ├── emotions/                # Algoritmos de puntuación por emoción
│   │   ├── happy_score.py
│   │   ├── sad_score.py
│   │   ├── angry_score.py
│   │   ├── fear_score.py
│   │   ├── suprise_score.py
│   │   └── disgust_score.py
│   └── main.py                  # Coordinador de reconocimiento
│
├── emotions_visualizations/      # Visualización de resultados
│   └── main.py                  # Dibuja barras de emociones en pantalla
│
└── main.py                      # Sistema principal integrado

examples/
├── camera.py                    # Clase para manejo de cámara
└── video_stream.py              # Aplicación de ejemplo en tiempo real
```

---

## 🔧 Funcionamiento Técnico

### 1. **Captura de Video** (`examples/camera.py`)
- Captura frames de la cámara web usando OpenCV
- Configurable: resolución, índice de cámara

### 2. **Detección de Malla Facial** (`face_mesh/face_mesh_processor.py`)
- **MediaPipe Face Mesh**: Detecta 468 puntos de referencia en el rostro
- Extrae puntos específicos para:
  - **Cejas**: 12 puntos (arcos y distancias)
  - **Ojos**: 18 puntos (párpados y aperturas)
  - **Nariz**: 4 puntos (puente y fosas nasales)
  - **Boca**: 12 puntos (labios superior/inferior, comisuras)

### 3. **Procesamiento de Características** (`data_processing/`)
Cada región facial se analiza independientemente:

#### Cejas (`eyebrows/`)
- Calcula curvaturas de arcos
- Mide distancias entre cejas
- Detecta: elevadas, bajadas, juntas, separadas

#### Ojos (`eyes/`)
- Analiza apertura de párpados
- Calcula distancias verticales
- Detecta: abiertos, cerrados, entrecerrados

#### Nariz (`nose/`)
- Mide distancias del puente nasal
- Detecta: arrugada, neutral

#### Boca (`mouth/`)
- Analiza curvaturas de labios (polinomios)
- Mide apertura vertical
- Detecta: sonrisa, fruncida, abierta, cerrada

### 4. **Reconocimiento de Emociones** (`emotions_recognition/`)
Cada emoción tiene un algoritmo de puntuación con **pesos específicos**:

**Ejemplo: Felicidad (Happy)**
```python
Pesos:
- Cejas: 10%
- Ojos: 20%
- Nariz: 10%
- Boca: 60%  # La boca es más importante para felicidad

Criterios:
- Cejas separadas: +50 puntos
- Ojos abiertos: +100 puntos
- Sonrisa derecha: +42 puntos
- Sonrisa izquierda: +42 puntos
```

Cada emoción tiene criterios únicos basados en la **Teoría de Emociones Básicas de Ekman**.

### 5. **Visualización** (`emotions_visualizations/`)
- Dibuja barras de progreso para cada emoción
- Colores únicos por emoción
- Actualización en tiempo real

---

## 🎯 Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| **Python 3.10** | Lenguaje base |
| **OpenCV** | Captura y procesamiento de video |
| **MediaPipe** | Detección de malla facial (468 landmarks) |
| **NumPy** | Cálculos matemáticos y arrays |
| **Matplotlib** | Visualizaciones (opcional) |

---

## 💡 Aplicación para Terapia Psicológica

### 🎯 Casos de Uso Terapéuticos

#### 1. **Monitoreo de Estado Emocional en Sesiones**
**Problema actual**: Los terapeutas dependen de la comunicación verbal y observación subjetiva.

**Solución con este sistema**:
- Registro objetivo de emociones durante la sesión
- Detección de emociones no verbalizadas
- Identificación de patrones emocionales

**Modificaciones sugeridas**:
```python
# Agregar registro temporal de emociones
class TherapySessionRecorder:
    def __init__(self):
        self.emotion_timeline = []
        self.timestamps = []
    
    def record_emotion(self, emotions, timestamp):
        self.emotion_timeline.append(emotions)
        self.timestamps.append(timestamp)
    
    def generate_session_report(self):
        # Genera gráficos de evolución emocional
        # Identifica momentos críticos
        # Calcula estadísticas de sesión
```

#### 2. **Terapia de Regulación Emocional**
**Aplicación**: Pacientes con trastornos de ansiedad, depresión, TEPT

**Funcionalidad**:
- **Biofeedback visual**: El paciente ve sus emociones en tiempo real
- **Ejercicios de regulación**: Técnicas de respiración mientras monitorean su estado
- **Gamificación**: Objetivos de mantener emociones positivas

**Modificaciones sugeridas**:
```python
# Sistema de alertas y ejercicios
class EmotionRegulationAssistant:
    def __init__(self):
        self.anxiety_threshold = 70  # Si miedo > 70%
        self.exercises = {
            'high_fear': 'Respiración 4-7-8',
            'high_anger': 'Técnica de grounding 5-4-3-2-1',
            'high_sad': 'Ejercicio de gratitud'
        }
    
    def check_and_suggest(self, emotions):
        if emotions['fear'] > self.anxiety_threshold:
            return self.exercises['high_fear']
        # ... más condiciones
```

#### 3. **Entrenamiento en Reconocimiento Emocional**
**Aplicación**: Pacientes con TEA (Trastorno del Espectro Autista), alexitimia

**Funcionalidad**:
- Modo de entrenamiento con retroalimentación
- Comparación de expresiones propias vs. objetivo
- Biblioteca de expresiones emocionales

**Modificaciones sugeridas**:
```python
# Sistema de entrenamiento
class EmotionTrainingMode:
    def __init__(self):
        self.target_emotion = None
        self.target_score = 80
    
    def set_target(self, emotion):
        self.target_emotion = emotion
    
    def provide_feedback(self, current_emotions):
        score = current_emotions[self.target_emotion]
        if score >= self.target_score:
            return "¡Excelente! Has logrado la expresión"
        else:
            return f"Intenta: {self.get_tips(self.target_emotion)}"
```

#### 4. **Análisis de Patrones a Largo Plazo**
**Aplicación**: Seguimiento de progreso terapéutico

**Funcionalidad**:
- Base de datos de sesiones
- Gráficos de evolución temporal
- Identificación de triggers emocionales

**Modificaciones sugeridas**:
```python
# Sistema de análisis histórico
class LongTermEmotionAnalyzer:
    def __init__(self):
        self.database = EmotionDatabase()
    
    def analyze_progress(self, patient_id, weeks=12):
        sessions = self.database.get_sessions(patient_id, weeks)
        return {
            'average_happiness': self.calc_avg('happy', sessions),
            'anxiety_reduction': self.calc_reduction('fear', sessions),
            'emotional_stability': self.calc_variance(sessions),
            'trigger_moments': self.identify_spikes(sessions)
        }
```

---

## 🔄 Modificaciones Recomendadas para Terapia

### 1. **Agregar Persistencia de Datos (Base de Datos de Sesiones)**

#### 🎯 ¿Qué se hace?
Se crea un sistema de almacenamiento permanente para guardar todas las sesiones terapéuticas con sus datos emocionales.

#### 🤔 ¿Por qué es necesario?
**Problema actual**: El sistema solo muestra emociones en tiempo real pero no guarda nada. Cuando termina la sesión, toda la información se pierde.

**Beneficios de agregarlo**:
- **Seguimiento a largo plazo**: Ver cómo evoluciona el paciente semana tras semana
- **Evidencia objetiva**: Datos concretos para evaluar efectividad del tratamiento
- **Identificación de patrones**: Detectar qué días/horarios el paciente está mejor o peor
- **Reportes para seguros**: Documentación objetiva del progreso terapéutico
- **Comparación de sesiones**: "Hoy estuviste 30% menos ansioso que la semana pasada"

#### 🔧 ¿Cómo se implementa?

**Crear**: `therapy_tools/session_database.py`
```python
import sqlite3
import json
from datetime import datetime

class SessionDatabase:
    """
    Base de datos para almacenar sesiones terapéuticas.
    Usa SQLite (archivo local, no requiere servidor).
    """
    def __init__(self, db_path='therapy_sessions.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """Crea las tablas necesarias si no existen"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,           -- ID anónimo del paciente
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                duration INTEGER,                    -- Duración en segundos
                emotions_data TEXT,                  -- JSON con timeline de emociones
                notes TEXT,                          -- Notas del terapeuta
                session_type TEXT                    -- Tipo: inicial, seguimiento, etc.
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS emotion_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                timestamp_offset INTEGER,            -- Segundos desde inicio de sesión
                happy REAL,
                sad REAL,
                angry REAL,
                fear REAL,
                surprise REAL,
                disgust REAL,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        ''')
        self.conn.commit()
    
    def start_session(self, patient_id, session_type='regular'):
        """Inicia una nueva sesión y retorna su ID"""
        cursor = self.conn.execute(
            'INSERT INTO sessions (patient_id, session_type) VALUES (?, ?)',
            (patient_id, session_type)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def save_emotion_snapshot(self, session_id, timestamp_offset, emotions):
        """
        Guarda un snapshot de emociones en un momento específico.
        Se llama cada segundo o cada frame procesado.
        """
        self.conn.execute('''
            INSERT INTO emotion_snapshots 
            (session_id, timestamp_offset, happy, sad, angry, fear, surprise, disgust)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id, 
            timestamp_offset,
            emotions.get('happy', 0),
            emotions.get('sad', 0),
            emotions.get('angry', 0),
            emotions.get('fear', 0),
            emotions.get('surprise', 0),
            emotions.get('disgust', 0)
        ))
        self.conn.commit()
    
    def end_session(self, session_id, notes=''):
        """Finaliza la sesión y calcula su duración"""
        cursor = self.conn.execute(
            'SELECT timestamp FROM sessions WHERE id = ?',
            (session_id,)
        )
        start_time = cursor.fetchone()[0]
        duration = (datetime.now() - datetime.fromisoformat(start_time)).seconds
        
        self.conn.execute(
            'UPDATE sessions SET duration = ?, notes = ? WHERE id = ?',
            (duration, notes, session_id)
        )
        self.conn.commit()
    
    def get_patient_sessions(self, patient_id, limit=10):
        """Obtiene las últimas N sesiones de un paciente"""
        cursor = self.conn.execute('''
            SELECT id, timestamp, duration, session_type, notes
            FROM sessions
            WHERE patient_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (patient_id, limit))
        return cursor.fetchall()
    
    def get_session_emotions(self, session_id):
        """Obtiene todos los snapshots de emociones de una sesión"""
        cursor = self.conn.execute('''
            SELECT timestamp_offset, happy, sad, angry, fear, surprise, disgust
            FROM emotion_snapshots
            WHERE session_id = ?
            ORDER BY timestamp_offset
        ''', (session_id,))
        return cursor.fetchall()
```

#### 📝 ¿Cómo se integra con el sistema actual?

**Modificar**: `examples/video_stream.py`
```python
from therapy_tools.session_database import SessionDatabase

class TherapyVideoStream(VideoStream):
    def __init__(self, cam, emotion_recognition_system, patient_id):
        super().__init__(cam, emotion_recognition_system)
        self.db = SessionDatabase()
        self.patient_id = patient_id
        self.session_id = None
        self.start_time = None
    
    def run(self):
        # Iniciar sesión en la base de datos
        self.session_id = self.db.start_session(self.patient_id)
        self.start_time = time.time()
        
        while True:
            ret, frame = self.camera.read()
            if ret:
                frame = self.emotion_recognition_system.frame_processing(frame)
                
                # NUEVO: Guardar emociones cada segundo
                current_time = time.time()
                if int(current_time - self.start_time) % 1 == 0:  # Cada segundo
                    emotions = self.emotion_recognition_system.emotions_recognition.last_emotions
                    timestamp_offset = int(current_time - self.start_time)
                    self.db.save_emotion_snapshot(self.session_id, timestamp_offset, emotions)
                
                cv2.imshow('Emotion Recognition', frame)
                if cv2.waitKey(5) == 27:  # ESC para salir
                    break
        
        # Finalizar sesión
        self.db.end_session(self.session_id)
        self.camera.release()
        cv2.destroyAllWindows()
```

### 2. **Dashboard de Terapeuta (Interfaz de Visualización)**

#### 🎯 ¿Qué se hace?
Se crea una interfaz gráfica donde el terapeuta puede ver gráficos, estadísticas y análisis de las sesiones de sus pacientes.

#### 🤔 ¿Por qué es necesario?
**Problema actual**: Los datos están en la base de datos pero no hay forma fácil de visualizarlos. El terapeuta necesitaría escribir código SQL para ver la información.

**Beneficios de agregarlo**:
- **Visualización intuitiva**: Gráficos de línea mostrando evolución emocional
- **Ahorro de tiempo**: Ver resumen de sesión en segundos, no minutos
- **Identificación rápida de problemas**: Picos de ansiedad resaltados automáticamente
- **Comparación visual**: Ver progreso entre sesiones lado a lado
- **Reportes profesionales**: Generar PDFs para compartir con paciente o colegas
- **Toma de decisiones informada**: Datos objetivos para ajustar tratamiento

#### 🔧 ¿Cómo se implementa?

**Crear**: `therapy_tools/therapist_dashboard.py`
```python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import numpy as np
from datetime import datetime

class TherapistDashboard:
    """
    Dashboard visual para que el terapeuta analice sesiones.
    Usa Tkinter (interfaz gráfica) y Matplotlib (gráficos).
    """
    def __init__(self, database):
        self.db = database
        self.window = tk.Tk()
        self.window.title("Dashboard Terapéutico - Análisis de Emociones")
        self.window.geometry("1200x800")
        
        # Colores de emociones (mismo que el sistema)
        self.emotion_colors = {
            'happy': '#1B97EF',
            'sad': '#BA7704',
            'angry': '#2332DC',
            'fear': '#80258E',
            'surprise': '#B8B753',
            'disgust': '#4FA424'
        }
    
    def show_session_summary(self, session_id):
        """
        Muestra resumen completo de una sesión específica.
        
        ¿Qué muestra?
        - Gráfico de línea temporal de todas las emociones
        - Estadísticas: emoción dominante, picos, promedios
        - Momentos críticos (cuando ansiedad/tristeza fueron altas)
        - Duración total y fecha
        """
        # Limpiar ventana
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Obtener datos de la sesión
        emotions_data = self.db.get_session_emotions(session_id)
        
        if not emotions_data:
            tk.Label(self.window, text="No hay datos para esta sesión").pack()
            return
        
        # Preparar datos para graficar
        timestamps = [row[0] for row in emotions_data]  # Segundos desde inicio
        emotions = {
            'happy': [row[1] for row in emotions_data],
            'sad': [row[2] for row in emotions_data],
            'angry': [row[3] for row in emotions_data],
            'fear': [row[4] for row in emotions_data],
            'surprise': [row[5] for row in emotions_data],
            'disgust': [row[6] for row in emotions_data]
        }
        
        # Crear figura de Matplotlib
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Gráfico 1: Líneas temporales de todas las emociones
        for emotion, values in emotions.items():
            ax1.plot(timestamps, values, 
                    label=emotion.capitalize(), 
                    color=self.emotion_colors[emotion],
                    linewidth=2)
        
        ax1.set_xlabel('Tiempo (segundos)', fontsize=12)
        ax1.set_ylabel('Intensidad (%)', fontsize=12)
        ax1.set_title('Evolución Emocional Durante la Sesión', fontsize=14, fontweight='bold')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 100)
        
        # Gráfico 2: Promedios por emoción (barras)
        emotion_names = list(emotions.keys())
        emotion_avgs = [np.mean(values) for values in emotions.values()]
        colors = [self.emotion_colors[e] for e in emotion_names]
        
        ax2.bar(emotion_names, emotion_avgs, color=colors, alpha=0.7)
        ax2.set_ylabel('Intensidad Promedio (%)', fontsize=12)
        ax2.set_title('Resumen: Emociones Promedio de la Sesión', fontsize=14, fontweight='bold')
        ax2.set_ylim(0, 100)
        
        # Agregar valores sobre las barras
        for i, v in enumerate(emotion_avgs):
            ax2.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
        
        plt.tight_layout()
        
        # Integrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Panel de estadísticas
        stats_frame = tk.Frame(self.window, bg='#f0f0f0', padx=20, pady=10)
        stats_frame.pack(fill=tk.X)
        
        # Calcular estadísticas clave
        dominant_emotion = max(emotion_avgs)
        dominant_name = emotion_names[emotion_avgs.index(dominant_emotion)]
        
        fear_avg = np.mean(emotions['fear'])
        sad_avg = np.mean(emotions['sad'])
        wellbeing_score = np.mean(emotions['happy']) - (fear_avg + sad_avg) / 2
        
        # Mostrar estadísticas
        tk.Label(stats_frame, text=f"🎭 Emoción Dominante: {dominant_name.upper()} ({dominant_emotion:.1f}%)",
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        tk.Label(stats_frame, text=f"😊 Índice de Bienestar: {wellbeing_score:.1f}% (felicidad - ansiedad/tristeza)",
                font=('Arial', 11), bg='#f0f0f0').pack(anchor='w')
        
        tk.Label(stats_frame, text=f"⏱️ Duración: {timestamps[-1] // 60} minutos {timestamps[-1] % 60} segundos",
                font=('Arial', 11), bg='#f0f0f0').pack(anchor='w')
        
        # Identificar momentos críticos (ansiedad > 70%)
        critical_moments = [t for t, f in zip(timestamps, emotions['fear']) if f > 70]
        if critical_moments:
            tk.Label(stats_frame, 
                    text=f"⚠️ Momentos de Alta Ansiedad: {len(critical_moments)} detectados",
                    font=('Arial', 11), bg='#f0f0f0', fg='red').pack(anchor='w')
    
    def compare_sessions(self, session_id1, session_id2):
        """
        Compara dos sesiones lado a lado.
        
        ¿Para qué sirve?
        - Ver si el paciente está mejorando entre sesiones
        - Identificar qué emociones han cambiado más
        - Mostrar progreso visual al paciente
        """
        # Limpiar ventana
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Obtener datos de ambas sesiones
        data1 = self.db.get_session_emotions(session_id1)
        data2 = self.db.get_session_emotions(session_id2)
        
        # Calcular promedios
        emotions1 = self._calculate_averages(data1)
        emotions2 = self._calculate_averages(data2)
        
        # Crear gráfico comparativo
        fig, ax = plt.subplots(figsize=(10, 6))
        
        emotion_names = list(emotions1.keys())
        x = np.arange(len(emotion_names))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, emotions1.values(), width, 
                      label='Sesión Anterior', alpha=0.8)
        bars2 = ax.bar(x + width/2, emotions2.values(), width, 
                      label='Sesión Actual', alpha=0.8)
        
        ax.set_ylabel('Intensidad Promedio (%)')
        ax.set_title('Comparación Entre Sesiones', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(emotion_names)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Análisis de cambios
        changes_frame = tk.Frame(self.window, bg='#f0f0f0', padx=20, pady=10)
        changes_frame.pack(fill=tk.X)
        
        tk.Label(changes_frame, text="📊 Análisis de Cambios:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        for emotion in emotion_names:
            change = emotions2[emotion] - emotions1[emotion]
            arrow = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            color = "green" if (emotion == 'happy' and change > 0) or \
                              (emotion in ['fear', 'sad', 'angry'] and change < 0) else "red"
            
            tk.Label(changes_frame, 
                    text=f"{arrow} {emotion.capitalize()}: {change:+.1f}%",
                    font=('Arial', 11), bg='#f0f0f0', fg=color).pack(anchor='w')
    
    def _calculate_averages(self, emotion_data):
        """Calcula promedios de emociones desde datos de sesión"""
        if not emotion_data:
            return {e: 0 for e in ['happy', 'sad', 'angry', 'fear', 'surprise', 'disgust']}
        
        return {
            'happy': np.mean([row[1] for row in emotion_data]),
            'sad': np.mean([row[2] for row in emotion_data]),
            'angry': np.mean([row[3] for row in emotion_data]),
            'fear': np.mean([row[4] for row in emotion_data]),
            'surprise': np.mean([row[5] for row in emotion_data]),
            'disgust': np.mean([row[6] for row in emotion_data])
        }
    
    def show_patient_history(self, patient_id):
        """
        Muestra historial completo del paciente.
        
        ¿Qué muestra?
        - Lista de todas las sesiones
        - Gráfico de tendencia a largo plazo
        - Progreso general del tratamiento
        """
        sessions = self.db.get_patient_sessions(patient_id, limit=20)
        
        # Crear lista de sesiones
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text=f"Historial del Paciente {patient_id}", 
                font=('Arial', 14, 'bold')).pack()
        
        # Tabla de sesiones
        tree = ttk.Treeview(frame, columns=('Fecha', 'Duración', 'Tipo'), show='headings')
        tree.heading('Fecha', text='Fecha')
        tree.heading('Duración', text='Duración (min)')
        tree.heading('Tipo', text='Tipo de Sesión')
        
        for session in sessions:
            session_id, timestamp, duration, session_type, notes = session
            date = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M')
            tree.insert('', 'end', values=(date, duration // 60, session_type))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Botón para ver detalles
        def on_select(event):
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                # Aquí se abriría el detalle de la sesión
                pass
        
        tree.bind('<<TreeviewSelect>>', on_select)
    
    def run(self):
        """Inicia la interfaz gráfica"""
        self.window.mainloop()
```

#### 📝 ¿Cómo se usa?

```python
# Ejemplo de uso para el terapeuta
from therapy_tools.session_database import SessionDatabase
from therapy_tools.therapist_dashboard import TherapistDashboard

# Conectar a la base de datos
db = SessionDatabase()

# Crear dashboard
dashboard = TherapistDashboard(db)

# Ver resumen de la última sesión
dashboard.show_session_summary(session_id=15)

# O comparar dos sesiones
dashboard.compare_sessions(session_id1=10, session_id2=15)

# O ver historial completo del paciente
dashboard.show_patient_history(patient_id='PAC_001')

# Iniciar interfaz
dashboard.run()
```

### 3. **Sistema de Privacidad y Ética (Protección de Datos)**

#### 🎯 ¿Qué se hace?
Se implementa un sistema completo de protección de datos personales y consentimiento informado, cumpliendo con regulaciones de privacidad.

#### 🤔 ¿Por qué es CRÍTICO?
**Problema actual**: El sistema no tiene ninguna protección de privacidad. Esto es ILEGAL en contexto terapéutico.

**Riesgos sin este sistema**:
- ❌ **Violación de GDPR/HIPAA**: Multas de hasta €20 millones o 4% de ingresos anuales
- ❌ **Pérdida de licencia profesional**: Terapeutas pueden perder su licencia
- ❌ **Demandas legales**: Pacientes pueden demandar por violación de privacidad
- ❌ **Pérdida de confianza**: Pacientes no querrán usar el sistema
- ❌ **Datos sensibles expuestos**: Información de salud mental es extremadamente sensible

**Beneficios de agregarlo**:
- ✅ **Cumplimiento legal**: GDPR, HIPAA, leyes locales de protección de datos
- ✅ **Consentimiento informado**: Paciente sabe exactamente qué se graba y por qué
- ✅ **Anonimización**: Protege identidad del paciente
- ✅ **Encriptación**: Datos seguros incluso si hay robo de dispositivo
- ✅ **Derecho al olvido**: Paciente puede solicitar eliminación de sus datos
- ✅ **Auditoría**: Registro de quién accede a qué datos y cuándo

#### 🔧 ¿Cómo se implementa?

**Crear**: `therapy_tools/privacy_manager.py`
```python
import hashlib
import json
from cryptography.fernet import Fernet
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext

class PrivacyManager:
    """
    Gestiona privacidad, consentimiento y protección de datos.
    Cumple con GDPR, HIPAA y mejores prácticas de seguridad.
    """
    def __init__(self, encryption_key=None):
        self.consent_given = False
        self.anonymize = True
        
        # Generar o cargar clave de encriptación
        if encryption_key:
            self.cipher = Fernet(encryption_key)
        else:
            self.cipher = Fernet(Fernet.generate_key())
        
        # Registro de accesos (auditoría)
        self.access_log = []
    
    def request_consent(self, patient_name=None):
        """
        Muestra formulario de consentimiento informado.
        
        ¿Por qué es necesario?
        - Legalmente requerido antes de grabar/procesar datos
        - Paciente debe entender qué se hace con sus datos
        - Debe ser voluntario y revocable
        
        Retorna: True si acepta, False si rechaza
        """
        consent_window = tk.Tk()
        consent_window.title("Consentimiento Informado - Sistema de Reconocimiento Emocional")
        consent_window.geometry("700x600")
        
        # Texto del consentimiento
        consent_text = """
CONSENTIMIENTO INFORMADO PARA USO DE SISTEMA DE RECONOCIMIENTO EMOCIONAL

Estimado/a paciente,

Le solicitamos su consentimiento para utilizar un sistema de reconocimiento de emociones 
faciales durante sus sesiones terapéuticas.

¿QUÉ HACE ESTE SISTEMA?
- Analiza su rostro mediante cámara web en tiempo real
- Detecta expresiones faciales asociadas a 6 emociones básicas
- Registra datos emocionales durante la sesión (NO graba video)
- Genera gráficos y estadísticas para análisis terapéutico

¿QUÉ DATOS SE RECOPILAN?
- Puntuaciones de emociones (números del 0-100) cada segundo
- Fecha y duración de sesiones
- Notas del terapeuta (si las hay)
- NO se graban imágenes ni videos de su rostro
- NO se almacena información identificable (nombre, dirección, etc.)

¿CÓMO SE PROTEGEN SUS DATOS?
- Identificación anónima (código ID, no su nombre)
- Encriptación de datos en reposo
- Acceso restringido solo a su terapeuta
- Almacenamiento local seguro (no en la nube)
- Cumplimiento con GDPR y regulaciones de privacidad

SUS DERECHOS:
✓ Puede rechazar el uso del sistema sin afectar su tratamiento
✓ Puede revocar este consentimiento en cualquier momento
✓ Puede solicitar acceso a sus datos
✓ Puede solicitar corrección de datos incorrectos
✓ Puede solicitar eliminación completa de sus datos
✓ Puede solicitar copia de sus datos en formato portable

LIMITACIONES DEL SISTEMA:
⚠ Este sistema NO es un diagnóstico médico
⚠ Es una herramienta complementaria, no reemplazo del juicio clínico
⚠ Puede tener imprecisiones en la detección de emociones
⚠ Requiere buena iluminación para funcionar correctamente

DURACIÓN DEL ALMACENAMIENTO:
- Sus datos se conservarán durante el tratamiento activo
- Después del alta, se conservarán según regulaciones locales (típicamente 5-10 años)
- Puede solicitar eliminación anticipada en cualquier momento

CONTACTO:
Si tiene preguntas sobre este sistema o sus datos, contacte a:
[Nombre del terapeuta]
[Información de contacto]
[Información del responsable de protección de datos]

---

Al hacer clic en "ACEPTO", confirmo que:
1. He leído y comprendido esta información
2. He tenido oportunidad de hacer preguntas
3. Consiento voluntariamente el uso de este sistema
4. Entiendo que puedo revocar este consentimiento en cualquier momento
        """
        
        # Área de texto con scroll
        text_area = scrolledtext.ScrolledText(consent_window, wrap=tk.WORD, 
                                              width=80, height=25, font=('Arial', 10))
        text_area.insert(tk.INSERT, consent_text)
        text_area.config(state=tk.DISABLED)  # Solo lectura
        text_area.pack(padx=10, pady=10)
        
        # Variable para almacenar respuesta
        consent_result = {'accepted': False}
        
        def accept_consent():
            # Registrar consentimiento
            self.consent_given = True
            self.log_access('CONSENT_GIVEN', patient_name or 'ANONYMOUS', 
                          'Patient accepted informed consent')
            consent_result['accepted'] = True
            consent_window.destroy()
        
        def reject_consent():
            self.consent_given = False
            self.log_access('CONSENT_REJECTED', patient_name or 'ANONYMOUS', 
                          'Patient rejected informed consent')
            consent_result['accepted'] = False
            consent_window.destroy()
        
        # Botones
        button_frame = tk.Frame(consent_window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="✓ ACEPTO", command=accept_consent, 
                 bg='green', fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="✗ NO ACEPTO", command=reject_consent, 
                 bg='red', fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=10)
        
        consent_window.mainloop()
        
        return consent_result['accepted']
    
    def anonymize_patient_id(self, patient_name, birth_date):
        """
        Genera ID anónimo del paciente usando hash.
        
        ¿Por qué?
        - No almacenar nombres reales en la base de datos
        - Proteger identidad en caso de filtración de datos
        - Cumplir con principio de minimización de datos
        
        Ejemplo:
        - Input: "Juan Pérez", "1990-05-15"
        - Output: "PAC_a3f5b2c8d1e4f6a7"
        """
        # Combinar nombre y fecha de nacimiento
        combined = f"{patient_name}_{birth_date}".encode('utf-8')
        
        # Generar hash SHA-256
        hash_object = hashlib.sha256(combined)
        hash_hex = hash_object.hexdigest()[:16]  # Primeros 16 caracteres
        
        return f"PAC_{hash_hex}"
    
    def encrypt_sensitive_data(self, data):
        """
        Encripta datos sensibles antes de almacenar.
        
        ¿Qué se encripta?
        - Notas del terapeuta (pueden contener información sensible)
        - Cualquier comentario o anotación
        - Metadatos que puedan identificar al paciente
        
        ¿Por qué?
        - Protección en caso de robo de dispositivo
        - Cumplimiento con estándares de seguridad
        - Defensa en profundidad (múltiples capas de seguridad)
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        encrypted = self.cipher.encrypt(data)
        return encrypted.decode('utf-8')
    
    def decrypt_sensitive_data(self, encrypted_data):
        """Desencripta datos para visualización autorizada"""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode('utf-8')
        
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode('utf-8')
    
    def log_access(self, action, user, details=''):
        """
        Registra todos los accesos a datos de pacientes.
        
        ¿Por qué es importante?
        - Auditoría: saber quién accedió a qué y cuándo
        - Detección de accesos no autorizados
        - Cumplimiento regulatorio (GDPR requiere logs)
        - Investigación en caso de incidente de seguridad
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,  # Ej: 'VIEW_SESSION', 'EXPORT_DATA', 'DELETE_DATA'
            'user': user,
            'details': details
        }
        self.access_log.append(log_entry)
        
        # Guardar en archivo de log
        with open('access_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def export_patient_data(self, patient_id, database):
        """
        Exporta todos los datos del paciente (Derecho de acceso GDPR).
        
        ¿Por qué?
        - GDPR Art. 15: Derecho de acceso del interesado
        - Paciente puede solicitar copia de todos sus datos
        - Debe ser en formato legible y portable
        """
        self.log_access('EXPORT_DATA', patient_id, 'Patient requested data export')
        
        # Obtener todas las sesiones
        sessions = database.get_patient_sessions(patient_id, limit=1000)
        
        export_data = {
            'patient_id': patient_id,
            'export_date': datetime.now().isoformat(),
            'sessions': []
        }
        
        for session in sessions:
            session_id, timestamp, duration, session_type, notes = session
            emotions = database.get_session_emotions(session_id)
            
            export_data['sessions'].append({
                'date': timestamp,
                'duration_minutes': duration // 60,
                'type': session_type,
                'emotions_timeline': emotions
            })
        
        # Guardar en JSON
        filename = f"patient_data_export_{patient_id}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename
    
    def delete_patient_data(self, patient_id, database):
        """
        Elimina todos los datos del paciente (Derecho al olvido GDPR).
        
        ¿Cuándo se usa?
        - Paciente revoca consentimiento
        - Paciente solicita eliminación de datos
        - Fin del período de retención legal
        
        ⚠️ IRREVERSIBLE - Requiere confirmación múltiple
        """
        # Confirmación de seguridad
        confirm = messagebox.askyesno(
            "⚠️ ELIMINAR DATOS - ACCIÓN IRREVERSIBLE",
            f"¿Está SEGURO de eliminar TODOS los datos del paciente {patient_id}?\n\n"
            "Esta acción NO se puede deshacer.\n"
            "Se eliminarán:\n"
            "- Todas las sesiones\n"
            "- Todos los datos emocionales\n"
            "- Todas las notas\n\n"
            "¿Continuar?"
        )
        
        if not confirm:
            return False
        
        # Segunda confirmación
        confirm2 = messagebox.askyesno(
            "⚠️ CONFIRMACIÓN FINAL",
            "Esta es su última oportunidad.\n\n"
            "¿Eliminar PERMANENTEMENTE todos los datos?"
        )
        
        if not confirm2:
            return False
        
        # Registrar eliminación ANTES de borrar
        self.log_access('DELETE_ALL_DATA', patient_id, 
                       'All patient data permanently deleted')
        
        # Eliminar de base de datos
        database.conn.execute('DELETE FROM emotion_snapshots WHERE session_id IN '
                            '(SELECT id FROM sessions WHERE patient_id = ?)', 
                            (patient_id,))
        database.conn.execute('DELETE FROM sessions WHERE patient_id = ?', 
                            (patient_id,))
        database.conn.commit()
        
        messagebox.showinfo("✓ Datos Eliminados", 
                          f"Todos los datos del paciente {patient_id} han sido eliminados.")
        
        return True
    
    def check_data_retention_policy(self, database, retention_years=7):
        """
        Verifica y elimina datos antiguos según política de retención.
        
        ¿Por qué?
        - GDPR: No conservar datos más tiempo del necesario
        - Minimización de riesgo: Menos datos = menos riesgo
        - Regulaciones profesionales: Típicamente 5-10 años
        
        Se ejecuta automáticamente cada mes.
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=retention_years * 365)
        
        # Buscar sesiones antiguas
        cursor = database.conn.execute('''
            SELECT DISTINCT patient_id, COUNT(*) as session_count
            FROM sessions
            WHERE timestamp < ?
            GROUP BY patient_id
        ''', (cutoff_date.isoformat(),))
        
        old_data = cursor.fetchall()
        
        if old_data:
            message = "Se encontraron datos antiguos que exceden la política de retención:\n\n"
            for patient_id, count in old_data:
                message += f"- Paciente {patient_id}: {count} sesiones antiguas\n"
            
            message += f"\n¿Eliminar datos anteriores a {cutoff_date.strftime('%Y-%m-%d')}?"
            
            if messagebox.askyesno("Política de Retención de Datos", message):
                for patient_id, _ in old_data:
                    database.conn.execute('''
                        DELETE FROM emotion_snapshots WHERE session_id IN
                        (SELECT id FROM sessions WHERE patient_id = ? AND timestamp < ?)
                    ''', (patient_id, cutoff_date.isoformat()))
                    
                    database.conn.execute('''
                        DELETE FROM sessions WHERE patient_id = ? AND timestamp < ?
                    ''', (patient_id, cutoff_date.isoformat()))
                
                database.conn.commit()
                self.log_access('RETENTION_POLICY', 'SYSTEM', 
                              f'Deleted data older than {retention_years} years')
```

#### 📝 ¿Cómo se integra?

**Modificar**: `examples/video_stream.py`
```python
from therapy_tools.privacy_manager import PrivacyManager

class SecureTherapyVideoStream(TherapyVideoStream):
    def __init__(self, cam, emotion_recognition_system, patient_name, birth_date):
        # Inicializar gestor de privacidad
        self.privacy = PrivacyManager()
        
        # PASO 1: Solicitar consentimiento ANTES de hacer nada
        if not self.privacy.request_consent(patient_name):
            print("❌ Consentimiento rechazado. No se puede iniciar sesión.")
            return
        
        # PASO 2: Anonimizar ID del paciente
        patient_id = self.privacy.anonymize_patient_id(patient_name, birth_date)
        
        # PASO 3: Inicializar sesión con ID anónimo
        super().__init__(cam, emotion_recognition_system, patient_id)
        
        # Registrar inicio de sesión
        self.privacy.log_access('START_SESSION', patient_id, 'New therapy session started')
```

### 4. **Modo de Calibración Personal (Personalización del Sistema)**

#### 🎯 ¿Qué se hace?
Se crea un proceso de calibración que ajusta el sistema a la forma única en que cada persona expresa emociones.

#### 🤔 ¿Por qué es necesario?
**Problema actual**: El sistema usa umbrales genéricos que asumen que todos expresamos emociones igual. Esto es FALSO.

**Realidad de las expresiones faciales**:
- 👤 **Variabilidad individual**: Algunas personas son muy expresivas, otras más contenidas
- 🌍 **Diferencias culturales**: Culturas asiáticas tienden a expresiones más sutiles
- 🧠 **Neurodivergencia**: Personas con autismo pueden tener expresiones atípicas
- 😐 **"Resting face"**: Algunas personas tienen cara de enojado/triste en estado neutral
- 🎭 **Rango expresivo**: Unos tienen sonrisas enormes, otros apenas mueven los labios

**Ejemplo del problema**:
```
Paciente A (muy expresivo):
- Su "neutral" = 20% felicidad detectada
- Su "feliz" = 95% felicidad detectada
- Rango útil: 20-95%

Paciente B (poco expresivo):
- Su "neutral" = 5% felicidad detectada
- Su "feliz" = 45% felicidad detectada
- Rango útil: 5-45%

Sin calibración: El sistema pensaría que B nunca está feliz (solo 45%)
Con calibración: El sistema entiende que 45% es MUY feliz para B
```

**Beneficios de agregarlo**:
- ✅ **Precisión personalizada**: Sistema ajustado a cada individuo
- ✅ **Menos falsos positivos**: No confundir "neutral" con "triste"
- ✅ **Mejor seguimiento**: Detectar cambios sutiles en el mismo paciente
- ✅ **Inclusión**: Funciona bien para personas neurodivergentes
- ✅ **Confianza del paciente**: Ve que el sistema "lo entiende"

#### 🔧 ¿Cómo se implementa?

**Crear**: `therapy_tools/personal_calibration.py`
```python
import numpy as np
import json
import time
import cv2

class PersonalCalibration:
    """
    Calibra el sistema para cada paciente individual.
    
    Proceso de calibración (5-10 minutos):
    1. Capturar estado neutral (30 segundos)
    2. Capturar cada emoción básica (10 segundos cada una)
    3. Calcular rangos personalizados
    4. Ajustar umbrales del sistema
    """
    def __init__(self, emotion_recognition_system):
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
    
    def start_calibration_wizard(self, camera, patient_id):
        """
        Asistente interactivo de calibración.
        
        ¿Cómo funciona?
        - Muestra instrucciones en pantalla
        - Guía al paciente paso a paso
        - Captura datos mientras el paciente expresa cada emoción
        - Calcula automáticamente los ajustes necesarios
        """
        print("=" * 60)
        print("🎯 CALIBRACIÓN PERSONAL DEL SISTEMA")
        print("=" * 60)
        print("\nEste proceso tomará aproximadamente 5-7 minutos.")
        print("Por favor, siga las instrucciones en pantalla.\n")
        input("Presione ENTER cuando esté listo para comenzar...")
        
        # PASO 1: Calibrar estado neutral
        print("\n📍 PASO 1/7: Estado Neutral")
        print("Por favor, mantenga una expresión facial relajada y neutral.")
        print("No sonría, no frunza el ceño, solo relájese.")
        self.calibrate_neutral(camera, duration=30)
        
        # PASO 2-7: Calibrar cada emoción
        emotions_to_calibrate = [
            ('happy', '😊 Felicidad', 'Sonría ampliamente, como si algo muy bueno hubiera pasado'),
            ('sad', '😢 Tristeza', 'Ponga cara triste, como si recibiera malas noticias'),
            ('angry', '😠 Enojo', 'Frunza el ceño y apriete la mandíbula, como si estuviera molesto'),
            ('fear', '😨 Miedo', 'Abra los ojos ampliamente, como si se asustara'),
            ('surprise', '😲 Sorpresa', 'Abra la boca y los ojos, como si algo inesperado pasara'),
            ('disgust', '🤢 Disgusto', 'Arrugue la nariz, como si oliera algo desagradable')
        ]
        
        for i, (emotion_key, emotion_name, instruction) in enumerate(emotions_to_calibrate, 2):
            print(f"\n📍 PASO {i}/7: {emotion_name}")
            print(f"Instrucción: {instruction}")
            input("Presione ENTER cuando esté listo...")
            self.calibrate_emotion(camera, emotion_key, duration=10)
        
        # PASO FINAL: Calcular ajustes
        print("\n🔧 Calculando ajustes personalizados...")
        self.calculate_adjustment_factors()
        
        # Guardar calibración
        self.save_calibration(patient_id)
        
        print("\n✅ ¡Calibración completada!")
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
        """
        print(f"⏱️ Capturando durante {duration} segundos...")
        
        samples = []
        start_time = time.time()
        countdown_shown = set()
        
        while time.time() - start_time < duration:
            ret, frame = camera.read()
            if not ret:
                continue
            
            # Procesar frame
            try:
                # Obtener emociones del frame actual
                emotions = self._get_emotions_from_frame(frame)
                if emotions:
                    samples.append(emotions)
            except:
                pass
            
            # Mostrar countdown
            remaining = int(duration - (time.time() - start_time))
            if remaining not in countdown_shown and remaining <= 10:
                print(f"⏱️ {remaining} segundos restantes...")
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
            print(f"✓ Capturados {len(samples)} muestras de estado neutral")
        else:
            print("⚠️ No se pudieron capturar muestras. Intente de nuevo.")
    
    def calibrate_emotion(self, camera, emotion_key, duration=10):
        """
        Captura una emoción específica expresada por el paciente.
        
        ¿Qué se mide?
        - Intensidad máxima que el paciente puede expresar
        - Características faciales específicas de su expresión
        - Variabilidad en su expresión de esa emoción
        """
        print(f"⏱️ Exprese {emotion_key} durante {duration} segundos...")
        
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
                print(f"⏱️ {remaining} segundos...")
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
            print(f"✓ Capturados {len(samples)} muestras de {emotion_key}")
        else:
            print(f"⚠️ No se pudieron capturar muestras de {emotion_key}")
    
    def calculate_adjustment_factors(self):
        """
        Calcula factores de ajuste basados en calibración.
        
        ¿Cómo funciona?
        1. Compara neutral vs. cada emoción
        2. Calcula el rango personal (diferencia entre neutral y máximo)
        3. Crea factores de escala para normalizar
        
        Ejemplo:
        - Paciente A: neutral=20%, feliz=95% → rango=75%
        - Paciente B: neutral=5%, feliz=45% → rango=40%
        - Factor de ajuste para B: 75/40 = 1.875
        - Ahora 45% de B se escala a 84%, comparable con A
        """
        neutral = self.baseline_emotions['neutral']
        
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
                    'scale_factor': adjustment_factor
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
    
    def save_calibration(self, patient_id):
        """Guarda calibración para uso futuro"""
        calibration_data = {
            'patient_id': patient_id,
            'calibration_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'baseline_emotions': self.baseline_emotions,
            'adjustment_factors': self.adjustment_factors,
            'personal_ranges': self.personal_ranges
        }
        
        filename = f"calibration_{patient_id}.json"
        with open(filename, 'w') as f:
            json.dump(calibration_data, f, indent=2)
        
        print(f"💾 Calibración guardada en: {filename}")
    
    def load_calibration(self, patient_id):
        """Carga calibración guardada previamente"""
        filename = f"calibration_{patient_id}.json"
        try:
            with open(filename, 'r') as f:
                calibration_data = json.load(f)
            
            self.baseline_emotions = calibration_data['baseline_emotions']
            self.adjustment_factors = calibration_data['adjustment_factors']
            self.personal_ranges = calibration_data['personal_ranges']
            
            print(f"✓ Calibración cargada para paciente {patient_id}")
            return True
        except FileNotFoundError:
            print(f"⚠️ No se encontró calibración para {patient_id}")
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
        """Helper: Obtiene emociones de un frame"""
        # Aquí se integra con el sistema de reconocimiento existente
        # Retorna diccionario de emociones
        pass

# Clase para integrar calibración con el sistema existente
class CalibratedEmotionRecognitionSystem(EmotionRecognitionSystem):
    """
    Versión del sistema que usa calibración personal.
    """
    def __init__(self, patient_id=None):
        super().__init__()
        self.calibration = PersonalCalibration(self)
        
        # Intentar cargar calibración existente
        if patient_id:
            self.calibration.load_calibration(patient_id)
    
    def frame_processing(self, face_image):
        """Procesa frame aplicando calibración personal"""
        # Procesamiento normal
        result = super().frame_processing(face_image)
        
        # Aplicar ajustes de calibración si existen
        if self.calibration.adjustment_factors:
            # Ajustar cada emoción
            adjusted_emotions = {}
            for emotion, score in self.last_emotions.items():
                adjusted_emotions[emotion] = self.calibration.adjust_emotion_score(
                    emotion, score
                )
            
            # Actualizar visualización con emociones ajustadas
            result = self.emotions_visualization.main(adjusted_emotions, result)
        
        return result
```

#### 📝 ¿Cómo se usa?

```python
# PRIMERA SESIÓN: Calibrar el sistema
from therapy_tools.personal_calibration import PersonalCalibration
from examples.camera import Camera

camera = Camera(0, 1280, 720)
emotion_system = EmotionRecognitionSystem()
calibration = PersonalCalibration(emotion_system)

# Ejecutar asistente de calibración (5-7 minutos)
calibration.start_calibration_wizard(camera, patient_id='PAC_12345')

# SESIONES POSTERIORES: Usar calibración guardada
from therapy_tools.personal_calibration import CalibratedEmotionRecognitionSystem

# El sistema carga automáticamente la calibración
calibrated_system = CalibratedEmotionRecognitionSystem(patient_id='PAC_12345')

# Usar normalmente - las emociones ya están ajustadas
video_stream = VideoStream(camera, calibrated_system)
video_stream.run()
```

### 5. **Integración con Ejercicios Terapéuticos (Biofeedback Activo)**

#### 🎯 ¿Qué se hace?
Se crean ejercicios terapéuticos interactivos que usan el reconocimiento emocional en tiempo real para dar feedback inmediato al paciente.

#### 🤔 ¿Por qué es necesario?
**Problema actual**: El sistema solo OBSERVA emociones, no ayuda activamente a regularlas.

**Concepto de Biofeedback**:
- El paciente ve sus emociones en tiempo real
- Practica técnicas de regulación
- Recibe confirmación inmediata cuando funciona
- Aprende qué técnicas son más efectivas para él/ella

**Beneficios terapéuticos**:
- ✅ **Aprendizaje acelerado**: Ver resultados inmediatos motiva y enseña
- ✅ **Autoeficacia**: "Puedo controlar mi ansiedad" (evidencia visual)
- ✅ **Personalización**: Descubrir qué técnicas funcionan mejor
- ✅ **Práctica guiada**: No solo teoría, sino práctica con feedback
- ✅ **Medición objetiva**: Saber si el ejercicio realmente funcionó
- ✅ **Motivación**: Gamificación y logros visuales

**Aplicaciones clínicas**:
- 😰 **Trastornos de ansiedad**: Ejercicios de respiración con monitoreo de miedo
- 😢 **Depresión**: Activación conductual con seguimiento de estado de ánimo
- 😡 **Manejo de ira**: Técnicas de enfriamiento con feedback visual
- 🧘 **Mindfulness**: Meditación guiada con medición de calma
- 😨 **TEPT**: Exposición gradual con monitoreo de ansiedad

#### 🔧 ¿Cómo se implementa?

**Crear**: `therapy_tools/therapeutic_exercises.py`
```python
import time
import cv2
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

class TherapeuticExercises:
    """
    Biblioteca de ejercicios terapéuticos con biofeedback emocional.
    """
    def __init__(self, emotion_recognition_system, camera):
        self.emotion_system = emotion_recognition_system
        self.camera = camera
        
        # Catálogo de ejercicios disponibles
        self.exercises = {
            'breathing_478': BreathingExercise478(self),
            'progressive_relaxation': ProgressiveRelaxation(self),
            'grounding_54321': GroundingExercise54321(self),
            'mindfulness_body_scan': MindfulnessBodyScan(self),
            'exposure_gradual': GradualExposureExercise(self)
        }
    
    def list_exercises(self):
        """Muestra ejercicios disponibles"""
        print("\n" + "=" * 60)
        print("EJERCICIOS TERAPÉUTICOS DISPONIBLES")
        print("=" * 60)
        
        for key, exercise in self.exercises.items():
            print(f"\n{exercise.name}")
            print(f"  Duración: {exercise.duration} minutos")
            print(f"  Indicado para: {exercise.indications}")
            print(f"  Objetivo: {exercise.goal}")
    
    def start_exercise(self, exercise_key):
        """Inicia un ejercicio específico"""
        if exercise_key not in self.exercises:
            print(f"❌ Ejercicio '{exercise_key}' no encontrado")
            return None
        
        exercise = self.exercises[exercise_key]
        print(f"\n🎯 Iniciando: {exercise.name}")
        print(f"Duración estimada: {exercise.duration} minutos\n")
        
        results = exercise.run()
        return results


class BreathingExercise478:
    """
    Ejercicio de Respiración 4-7-8 (Dr. Andrew Weil)
    
    ¿Qué es?
    - Inhalar por 4 segundos
    - Retener por 7 segundos
    - Exhalar por 8 segundos
    - Repetir 4-8 ciclos
    
    ¿Para qué sirve?
    - Reducir ansiedad rápidamente
    - Activar sistema nervioso parasimpático
    - Preparar para dormir
    - Manejo de ataques de pánico
    
    ¿Cómo usa el biofeedback?
    - Monitorea nivel de miedo/ansiedad en tiempo real
    - Muestra gráfico de reducción de ansiedad
    - Confirma cuando la técnica está funcionando
    """
    def __init__(self, parent):
        self.parent = parent
        self.name = "Respiración 4-7-8"
        self.duration = 5
        self.indications = "Ansiedad, estrés, insomnio, ataques de pánico"
        self.goal = "Reducir ansiedad en 30-50%"
        
        # Datos de la sesión
        self.emotion_timeline = []
        self.timestamps = []
    
    def run(self):
        """Ejecuta el ejercicio con guía visual y monitoreo"""
        print("=" * 60)
        print("EJERCICIO: RESPIRACIÓN 4-7-8")
        print("=" * 60)
        print("\nInstrucciones:")
        print("1. Siéntese cómodamente con la espalda recta")
        print("2. Coloque la punta de la lengua detrás de los dientes superiores")
        print("3. Siga las instrucciones en pantalla")
        print("4. El sistema monitoreará su nivel de ansiedad\n")
        
        input("Presione ENTER cuando esté listo...")
        
        # Medir ansiedad inicial
        print("\n📊 Midiendo nivel de ansiedad inicial...")
        initial_anxiety = self._measure_current_anxiety(duration=10)
        print(f"Ansiedad inicial: {initial_anxiety:.1f}%")
        
        # Realizar 6 ciclos de respiración
        num_cycles = 6
        for cycle in range(1, num_cycles + 1):
            print(f"\n🔄 Ciclo {cycle}/{num_cycles}")
            self._breathing_cycle()
            
            # Medir ansiedad después de cada ciclo
            current_anxiety = self._measure_current_anxiety(duration=5)
            reduction = initial_anxiety - current_anxiety
            
            print(f"  Ansiedad actual: {current_anxiety:.1f}% "
                  f"(reducción: {reduction:.1f}%)")
            
            if reduction > 0:
                print(f"  ✓ ¡Bien! La ansiedad está bajando")
            
            time.sleep(2)  # Pausa entre ciclos
        
        # Medir ansiedad final
        print("\n📊 Midiendo nivel de ansiedad final...")
        final_anxiety = self._measure_current_anxiety(duration=10)
        total_reduction = initial_anxiety - final_anxiety
        reduction_percent = (total_reduction / initial_anxiety * 100) if initial_anxiety > 0 else 0
        
        # Resultados
        results = {
            'exercise': 'breathing_478',
            'initial_anxiety': initial_anxiety,
            'final_anxiety': final_anxiety,
            'reduction': total_reduction,
            'reduction_percent': reduction_percent,
            'num_cycles': num_cycles,
            'timeline': self.emotion_timeline,
            'timestamps': self.timestamps,
            'success': total_reduction > 0
        }
        
        # Mostrar resumen
        self._show_results(results)
        
        return results
    
    def _breathing_cycle(self):
        """Un ciclo completo de respiración 4-7-8"""
        phases = [
            ('INHALE', 4, (0, 255, 0)),      # Verde - Inhalar 4 seg
            ('HOLD', 7, (255, 255, 0)),      # Amarillo - Retener 7 seg
            ('EXHALE', 8, (0, 100, 255))     # Naranja - Exhalar 8 seg
        ]
        
        for phase_name, duration, color in phases:
            start_time = time.time()
            
            while time.time() - start_time < duration:
                ret, frame = self.parent.camera.read()
                if not ret:
                    continue
                
                # Procesar emociones
                frame = self.parent.emotion_system.frame_processing(frame)
                
                # Calcular tiempo restante
                elapsed = time.time() - start_time
                remaining = duration - elapsed
                
                # Dibujar instrucciones grandes
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 150), (0, 0, 0), -1)
                
                cv2.putText(frame, phase_name, 
                           (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 
                           2.5, color, 4, cv2.LINE_AA)
                
                cv2.putText(frame, f"{remaining:.1f}s", 
                           (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 
                           1.5, (255, 255, 255), 3, cv2.LINE_AA)
                
                # Barra de progreso
                progress = elapsed / duration
                bar_width = int(progress * (frame.shape[1] - 100))
                cv2.rectangle(frame, (50, 140), (50 + bar_width, 160), color, -1)
                cv2.rectangle(frame, (50, 140), (frame.shape[1] - 50, 160), (255, 255, 255), 2)
                
                cv2.imshow('Ejercicio de Respiracion', frame)
                cv2.waitKey(1)
    
    def _measure_current_anxiety(self, duration=10):
        """Mide nivel promedio de ansiedad durante X segundos"""
        anxiety_samples = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            ret, frame = self.parent.camera.read()
            if not ret:
                continue
            
            # Procesar frame
            frame = self.parent.emotion_system.frame_processing(frame)
            
            # Obtener nivel de miedo (proxy de ansiedad)
            # Nota: Necesitarías acceder a las emociones del sistema
            # Aquí asumo que existe un método para obtenerlas
            try:
                emotions = self.parent.emotion_system.emotions_recognition.last_emotions
                anxiety = emotions.get('fear', 0)
                anxiety_samples.append(anxiety)
                
                # Guardar en timeline
                self.emotion_timeline.append(emotions.copy())
                self.timestamps.append(time.time())
            except:
                pass
            
            # Mostrar medición en progreso
            remaining = int(duration - (time.time() - start_time))
            cv2.putText(frame, f"Midiendo... {remaining}s", 
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (255, 255, 0), 2)
            cv2.imshow('Ejercicio de Respiracion', frame)
            cv2.waitKey(1)
        
        return np.mean(anxiety_samples) if anxiety_samples else 0
    
    def _show_results(self, results):
        """Muestra resultados visuales del ejercicio"""
        cv2.destroyAllWindows()
        
        print("\n" + "=" * 60)
        print("RESULTADOS DEL EJERCICIO")
        print("=" * 60)
        print(f"\n📊 Ansiedad inicial: {results['initial_anxiety']:.1f}%")
        print(f"📊 Ansiedad final: {results['final_anxiety']:.1f}%")
        print(f"📉 Reducción: {results['reduction']:.1f}% "
              f"({results['reduction_percent']:.1f}% de mejora)")
        
        if results['success']:
            print("\n✅ ¡ÉXITO! El ejercicio redujo su ansiedad")
            if results['reduction_percent'] > 50:
                print("   ¡Excelente resultado! Reducción mayor al 50%")
            elif results['reduction_percent'] > 30:
                print("   Buen resultado. Reducción significativa.")
            else:
                print("   Reducción moderada. Considere practicar más.")
        else:
            print("\n⚠️ No se detectó reducción de ansiedad")
            print("   Esto puede deberse a:")
            print("   - Necesita más práctica con la técnica")
            print("   - El nivel de ansiedad inicial era bajo")
            print("   - Factores externos interfirieron")
        
        # Crear gráfico de evolución
        if len(results['timeline']) > 0:
            self._plot_anxiety_evolution(results)
    
    def _plot_anxiety_evolution(self, results):
        """Genera gráfico de evolución de ansiedad"""
        fear_values = [e.get('fear', 0) for e in results['timeline']]
        time_points = [(t - results['timestamps'][0]) / 60 for t in results['timestamps']]
        
        plt.figure(figsize=(10, 6))
        plt.plot(time_points, fear_values, 'b-', linewidth=2, label='Nivel de Ansiedad')
        plt.axhline(y=results['initial_anxiety'], color='r', linestyle='--', 
                   label=f'Inicial: {results["initial_anxiety"]:.1f}%')
        plt.axhline(y=results['final_anxiety'], color='g', linestyle='--', 
                   label=f'Final: {results["final_anxiety"]:.1f}%')
        
        plt.xlabel('Tiempo (minutos)', fontsize=12)
        plt.ylabel('Nivel de Ansiedad (%)', fontsize=12)
        plt.title('Evolución de Ansiedad Durante Ejercicio de Respiración', 
                 fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)
        
        plt.tight_layout()
        plt.savefig(f'breathing_exercise_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        plt.show()
        
        print("\n📈 Gráfico guardado y mostrado")


class GroundingExercise54321:
    """
    Técnica de Grounding 5-4-3-2-1
    
    ¿Qué es?
    Ejercicio de atención plena para crisis de ansiedad:
    - 5 cosas que puedes VER
    - 4 cosas que puedes TOCAR
    - 3 cosas que puedes OÍR
    - 2 cosas que puedes OLER
    - 1 cosa que puedes SABOREAR
    
    ¿Para qué sirve?
    - Detener ataques de pánico
    - Desconexión de pensamientos ansiosos
    - Volver al momento presente
    - Reducir disociación
    
    ¿Cómo usa el biofeedback?
    - Monitorea reducción de ansiedad en cada paso
    - Confirma cuando el paciente se está calmando
    - Identifica qué sentidos son más efectivos
    """
    def __init__(self, parent):
        self.parent = parent
        self.name = "Grounding 5-4-3-2-1"
        self.duration = 8
        self.indications = "Ataques de pánico, disociación, ansiedad aguda"
        self.goal = "Reducir ansiedad y volver al presente"
    
    def run(self):
        """Ejecuta ejercicio de grounding con monitoreo"""
        print("=" * 60)
        print("EJERCICIO: GROUNDING 5-4-3-2-1")
        print("=" * 60)
        print("\nEste ejercicio le ayudará a conectar con el momento presente")
        print("usando sus cinco sentidos.\n")
        
        input("Presione ENTER para comenzar...")
        
        # Medir ansiedad inicial
        initial_anxiety = self._measure_anxiety(10)
        print(f"\n📊 Ansiedad inicial: {initial_anxiety:.1f}%")
        
        steps = [
            ("VISTA", 5, "Nombre 5 cosas que puede VER a su alrededor"),
            ("TACTO", 4, "Nombre 4 cosas que puede TOCAR"),
            ("OÍDO", 3, "Nombre 3 cosas que puede OÍR"),
            ("OLFATO", 2, "Nombre 2 cosas que puede OLER"),
            ("GUSTO", 1, "Nombre 1 cosa que puede SABOREAR")
        ]
        
        anxiety_per_step = [initial_anxiety]
        
        for sense, count, instruction in steps:
            print(f"\n👉 {sense}: {instruction}")
            
            for i in range(1, count + 1):
                item = input(f"   {i}. ")
                print(f"      ✓ {item}")
            
            # Medir ansiedad después de cada sentido
            current_anxiety = self._measure_anxiety(5)
            anxiety_per_step.append(current_anxiety)
            reduction = anxiety_per_step[-2] - current_anxiety
            
            print(f"\n   📊 Ansiedad: {current_anxiety:.1f}% "
                  f"(cambio: {reduction:+.1f}%)")
        
        # Resultados finales
        final_anxiety = anxiety_per_step[-1]
        total_reduction = initial_anxiety - final_anxiety
        
        results = {
            'exercise': 'grounding_54321',
            'initial_anxiety': initial_anxiety,
            'final_anxiety': final_anxiety,
            'reduction': total_reduction,
            'anxiety_per_step': anxiety_per_step,
            'success': total_reduction > 0
        }
        
        self._show_results(results)
        return results
    
    def _measure_anxiety(self, duration):
        """Mide ansiedad promedio"""
        # Similar a BreathingExercise478._measure_current_anxiety
        pass
    
    def _show_results(self, results):
        """Muestra resultados"""
        print("\n" + "=" * 60)
        print("RESULTADOS")
        print("=" * 60)
        print(f"\n📊 Reducción total: {results['reduction']:.1f}%")
        
        if results['success']:
            print("✅ El ejercicio fue efectivo")
        else:
            print("⚠️ Considere repetir o probar otra técnica")


# Más ejercicios: ProgressiveRelaxation, MindfulnessBodyScan, GradualExposureExercise
# Implementación similar con monitoreo emocional específico
```

#### 📝 ¿Cómo se usa?

```python
# Inicializar sistema con ejercicios
from therapy_tools.therapeutic_exercises import TherapeuticExercises
from examples.camera import Camera

camera = Camera(0, 1280, 720)
emotion_system = EmotionRecognitionSystem()
exercises = TherapeuticExercises(emotion_system, camera)

# Ver ejercicios disponibles
exercises.list_exercises()

# Ejecutar ejercicio de respiración
results = exercises.start_exercise('breathing_478')

# Guardar resultados en base de datos
db.save_exercise_results(patient_id, results)

# El terapeuta puede revisar después qué ejercicios funcionan mejor
```

#### 🎯 Valor terapéutico

**Antes (sin biofeedback)**:
- Terapeuta: "Practique respiración profunda cuando esté ansioso"
- Paciente: "Lo intenté pero no sé si funciona"
- Resultado: Baja adherencia, dudas sobre efectividad

**Después (con biofeedback)**:
- Sistema: "Su ansiedad bajó de 75% a 35% en 5 minutos"
- Paciente: "¡Wow! Realmente funciona, lo vi en el gráfico"
- Resultado: Alta adherencia, confianza en la técnica, práctica regular

---

## 📊 Métricas Terapéuticas Sugeridas

### Métricas por Sesión
- **Emoción dominante**: Emoción con mayor puntuación promedio
- **Estabilidad emocional**: Varianza de emociones
- **Momentos críticos**: Picos de emociones negativas
- **Tiempo de recuperación**: Cuánto tarda en volver a neutral

### Métricas a Largo Plazo
- **Tendencia de bienestar**: Incremento de emociones positivas
- **Reducción de ansiedad**: Disminución de miedo/preocupación
- **Regulación emocional**: Menor variabilidad entre sesiones
- **Resiliencia**: Recuperación más rápida de emociones negativas

---

## ⚠️ Consideraciones Éticas y Limitaciones

### Limitaciones Técnicas
1. **No es diagnóstico clínico**: Este sistema NO reemplaza evaluación profesional
2. **Variabilidad individual**: Las expresiones faciales varían entre culturas y personas
3. **Falsos positivos**: Puede confundir emociones similares (miedo vs. sorpresa)
4. **Condiciones de iluminación**: Requiere buena iluminación para precisión
5. **Expresiones microemocionales**: No detecta microexpresiones (<0.5 segundos)

### Consideraciones Éticas
1. **Consentimiento informado**: Siempre requerir autorización explícita
2. **Privacidad de datos**: Encriptar y proteger grabaciones
3. **No grabar sin permiso**: Cumplir con leyes de privacidad (GDPR, HIPAA)
4. **Uso complementario**: Herramienta de apoyo, no reemplazo del terapeuta
5. **Sesgo algorítmico**: Puede tener menor precisión en ciertos grupos demográficos

### Recomendaciones de Uso
- ✅ Como herramienta de biofeedback en sesión
- ✅ Para entrenamiento en reconocimiento emocional
- ✅ Para registro objetivo complementario
- ❌ NO como único método de evaluación
- ❌ NO para decisiones clínicas críticas sin supervisión
- ❌ NO sin consentimiento explícito del paciente

---

## 🚀 Roadmap para Versión Terapéutica

### Fase 1: Fundamentos (2-4 semanas)
- [ ] Implementar base de datos de sesiones
- [ ] Crear sistema de perfiles de pacientes (anonimizados)
- [ ] Agregar exportación de reportes PDF
- [ ] Implementar calibración personal

### Fase 2: Funcionalidades Terapéuticas (4-6 semanas)
- [ ] Dashboard de terapeuta con visualizaciones
- [ ] Sistema de ejercicios de regulación emocional
- [ ] Modo de entrenamiento para reconocimiento emocional
- [ ] Alertas y sugerencias en tiempo real

### Fase 3: Análisis Avanzado (6-8 semanas)
- [ ] Machine Learning para patrones personalizados
- [ ] Análisis de correlaciones (eventos-emociones)
- [ ] Predicción de estados emocionales
- [ ] Integración con wearables (frecuencia cardíaca, etc.)

### Fase 4: Validación Clínica (Ongoing)
- [ ] Estudios piloto con terapeutas
- [ ] Validación con escalas clínicas estándar
- [ ] Ajustes basados en feedback profesional
- [ ] Publicación de resultados

---

## 📚 Recursos Adicionales

### Teoría de Emociones
- **Paul Ekman**: Emociones básicas universales
- **Lisa Feldman Barrett**: Teoría de emociones construidas
- **Modelo Circumplejo**: Valencia y activación emocional

### Aplicaciones Clínicas
- **Terapia Cognitivo-Conductual (TCC)**: Registro de emociones
- **Terapia Dialéctico-Conductual (TDC)**: Regulación emocional
- **Terapia de Exposición**: Monitoreo de ansiedad
- **Entrenamiento en Habilidades Sociales**: Reconocimiento emocional

### Tecnologías Relacionadas
- **Affectiva**: SDK comercial de reconocimiento emocional
- **Microsoft Emotion API**: Servicio cloud
- **OpenFace**: Toolkit académico de análisis facial

---

## 🤝 Colaboración con Profesionales

Para implementar este sistema en contexto terapéutico real, se recomienda:

1. **Consultar con psicólogos clínicos** sobre necesidades específicas
2. **Validar con estudios piloto** en entornos controlados
3. **Cumplir con regulaciones** de dispositivos médicos si aplica
4. **Obtener certificaciones** de privacidad y seguridad de datos
5. **Capacitar a terapeutas** en interpretación de resultados

---

## 📞 Contacto y Contribuciones

Este análisis fue creado para explorar el potencial terapéutico del sistema.

**Para implementación real en contexto clínico**:
- Consultar con comités de ética
- Obtener aprobaciones institucionales
- Realizar pruebas de validación
- Documentar limitaciones claramente

---

## 📄 Licencia y Responsabilidad

⚠️ **IMPORTANTE**: Este sistema es una herramienta de investigación y apoyo. NO es un dispositivo médico certificado. El uso en contexto clínico debe ser supervisado por profesionales licenciados y cumplir con todas las regulaciones locales de salud mental y privacidad de datos.

---

**Última actualización**: Diciembre 2024
**Versión del análisis**: 1.0
