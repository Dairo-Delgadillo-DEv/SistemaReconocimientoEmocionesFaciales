# Base de datos para almacenar sesiones terapéuticas
# Usa SQLite para almacenamiento local sin necesidad de servidor

import sqlite3
import json
from datetime import datetime


class SessionDatabase:
    """
    Base de datos para almacenar sesiones terapéuticas.
    Usa SQLite (archivo local, no requiere servidor).
    
    Beneficios:
    - Seguimiento a largo plazo del paciente
    - Evidencia objetiva para evaluar efectividad del tratamiento
    - Identificación de patrones emocionales
    - Reportes para documentación clínica
    """
    
    def __init__(self, db_path='therapy_sessions.db'):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """Crea las tablas necesarias si no existen"""
        # Tabla de sesiones
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
        
        # Tabla de snapshots de emociones
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
        
        # Tabla de resultados de ejercicios
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS exercise_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                patient_id TEXT NOT NULL,
                exercise_type TEXT,                  -- Tipo de ejercicio
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                initial_anxiety REAL,
                final_anxiety REAL,
                reduction REAL,
                reduction_percent REAL,
                success INTEGER,                     -- 1 si fue exitoso, 0 si no
                notes TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        ''')
        
        self.conn.commit()
    
    def start_session(self, patient_id, session_type='regular'):
        """
        Inicia una nueva sesión y retorna su ID.
        
        Args:
            patient_id: ID anónimo del paciente
            session_type: Tipo de sesión (inicial, seguimiento, etc.)
            
        Returns:
            int: ID de la sesión creada
        """
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
        
        Args:
            session_id: ID de la sesión actual
            timestamp_offset: Segundos desde el inicio de la sesión
            emotions: Diccionario con puntuaciones de emociones
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
        """
        Finaliza la sesión y calcula su duración.
        
        Args:
            session_id: ID de la sesión a finalizar
            notes: Notas opcionales del terapeuta
        """
        # Obtener timestamp de inicio
        cursor = self.conn.execute(
            'SELECT timestamp FROM sessions WHERE id = ?',
            (session_id,)
        )
        result = cursor.fetchone()
        
        if result:
            start_time = result[0]
            # Calcular duración
            try:
                start_dt = datetime.fromisoformat(start_time)
                duration = (datetime.now() - start_dt).seconds
            except:
                duration = 0
            
            self.conn.execute(
                'UPDATE sessions SET duration = ?, notes = ? WHERE id = ?',
                (duration, notes, session_id)
            )
            self.conn.commit()
    
    def get_patient_sessions(self, patient_id, limit=10):
        """
        Obtiene las últimas N sesiones de un paciente.
        
        Args:
            patient_id: ID anónimo del paciente
            limit: Número máximo de sesiones a retornar
            
        Returns:
            list: Lista de tuplas con datos de sesiones
        """
        cursor = self.conn.execute('''
            SELECT id, timestamp, duration, session_type, notes
            FROM sessions
            WHERE patient_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (patient_id, limit))
        return cursor.fetchall()
    
    def get_session_emotions(self, session_id):
        """
        Obtiene todos los snapshots de emociones de una sesión.
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            list: Lista de tuplas con datos de emociones
        """
        cursor = self.conn.execute('''
            SELECT timestamp_offset, happy, sad, angry, fear, surprise, disgust
            FROM emotion_snapshots
            WHERE session_id = ?
            ORDER BY timestamp_offset
        ''', (session_id,))
        return cursor.fetchall()
    
    def save_exercise_results(self, patient_id, results, session_id=None):
        """
        Guarda los resultados de un ejercicio terapéutico.
        
        Args:
            patient_id: ID anónimo del paciente
            results: Diccionario con resultados del ejercicio
            session_id: ID de sesión opcional
        """
        self.conn.execute('''
            INSERT INTO exercise_results 
            (session_id, patient_id, exercise_type, initial_anxiety, 
             final_anxiety, reduction, reduction_percent, success, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            patient_id,
            results.get('exercise', 'unknown'),
            results.get('initial_anxiety', 0),
            results.get('final_anxiety', 0),
            results.get('reduction', 0),
            results.get('reduction_percent', 0),
            1 if results.get('success', False) else 0,
            json.dumps(results.get('timeline', []))
        ))
        self.conn.commit()
    
    def get_patient_exercise_history(self, patient_id, limit=20):
        """
        Obtiene historial de ejercicios de un paciente.
        
        Args:
            patient_id: ID del paciente
            limit: Número máximo de resultados
            
        Returns:
            list: Lista de resultados de ejercicios
        """
        cursor = self.conn.execute('''
            SELECT exercise_type, timestamp, initial_anxiety, final_anxiety, 
                   reduction_percent, success
            FROM exercise_results
            WHERE patient_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (patient_id, limit))
        return cursor.fetchall()
    
    def get_session_statistics(self, session_id):
        """
        Calcula estadísticas de una sesión específica.
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            dict: Diccionario con estadísticas
        """
        emotions_data = self.get_session_emotions(session_id)
        
        if not emotions_data:
            return None
        
        # Calcular promedios y estadísticas
        import numpy as np
        
        stats = {
            'happy': {'mean': 0, 'max': 0, 'min': 0},
            'sad': {'mean': 0, 'max': 0, 'min': 0},
            'angry': {'mean': 0, 'max': 0, 'min': 0},
            'fear': {'mean': 0, 'max': 0, 'min': 0},
            'surprise': {'mean': 0, 'max': 0, 'min': 0},
            'disgust': {'mean': 0, 'max': 0, 'min': 0}
        }
        
        emotions = ['happy', 'sad', 'angry', 'fear', 'surprise', 'disgust']
        
        for i, emotion in enumerate(emotions):
            values = [row[i + 1] for row in emotions_data]  # +1 por timestamp_offset
            if values:
                stats[emotion] = {
                    'mean': float(np.mean(values)),
                    'max': float(np.max(values)),
                    'min': float(np.min(values)),
                    'std': float(np.std(values))
                }
        
        # Encontrar emoción dominante
        averages = {e: stats[e]['mean'] for e in emotions}
        dominant = max(averages, key=averages.get)
        
        stats['dominant_emotion'] = dominant
        stats['duration_seconds'] = emotions_data[-1][0] if emotions_data else 0
        
        return stats
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()
