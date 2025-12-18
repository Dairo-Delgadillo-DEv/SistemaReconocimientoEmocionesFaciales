# Dashboard visual para que el terapeuta analice sesiones
# Usa Tkinter para la interfaz y Matplotlib para gráficos

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
    
    Beneficios:
    - Visualización intuitiva de evolución emocional
    - Ahorro de tiempo en análisis de sesiones
    - Identificación rápida de momentos críticos
    - Comparación visual entre sesiones
    - Reportes profesionales
    """
    
    def __init__(self, database):
        """
        Inicializa el dashboard.
        
        Args:
            database: Instancia de SessionDatabase
        """
        self.db = database
        self.window = None
        
        # Colores de emociones (mismo que el sistema de visualización)
        self.emotion_colors = {
            'happy': '#1B97EF',     # Azul
            'sad': '#BA7704',       # Marrón/Naranja
            'angry': '#2332DC',     # Azul oscuro
            'fear': '#80258E',      # Púrpura
            'surprise': '#B8B753',  # Amarillo/Verde
            'disgust': '#4FA424'    # Verde
        }
        
        # Nombres en español de las emociones
        self.emotion_names_es = {
            'happy': 'Felicidad',
            'sad': 'Tristeza',
            'angry': 'Enojo',
            'fear': 'Miedo',
            'surprise': 'Sorpresa',
            'disgust': 'Disgusto'
        }
    
    def _create_window(self, title="Dashboard Terapéutico", size="1200x800"):
        """Crea o recrea la ventana principal"""
        if self.window:
            self.window.destroy()
        
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(size)
        return self.window
    
    def show_session_summary(self, session_id):
        """
        Muestra resumen completo de una sesión específica.
        
        ¿Qué muestra?
        - Gráfico de línea temporal de todas las emociones
        - Estadísticas: emoción dominante, picos, promedios
        - Momentos críticos (cuando ansiedad/tristeza fueron altas)
        - Duración total y fecha
        
        Args:
            session_id: ID de la sesión a visualizar
        """
        self._create_window("Resumen de Sesión - Dashboard Terapéutico")
        
        # Obtener datos de la sesión
        emotions_data = self.db.get_session_emotions(session_id)
        
        if not emotions_data:
            tk.Label(self.window, text="No hay datos para esta sesión", 
                    font=('Arial', 14)).pack(pady=50)
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
                    label=self.emotion_names_es[emotion], 
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
        
        ax2.bar([self.emotion_names_es[e] for e in emotion_names], 
               emotion_avgs, color=colors, alpha=0.7)
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
        dominant_emotion_value = max(emotion_avgs)
        dominant_idx = emotion_avgs.index(dominant_emotion_value)
        dominant_name = emotion_names[dominant_idx]
        
        fear_avg = np.mean(emotions['fear'])
        sad_avg = np.mean(emotions['sad'])
        happy_avg = np.mean(emotions['happy'])
        wellbeing_score = happy_avg - (fear_avg + sad_avg) / 2
        
        # Mostrar estadísticas
        tk.Label(stats_frame, 
                text=f"Emoción Dominante: {self.emotion_names_es[dominant_name].upper()} ({dominant_emotion_value:.1f}%)",
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        tk.Label(stats_frame, 
                text=f"Índice de Bienestar: {wellbeing_score:.1f}% (felicidad - ansiedad/tristeza)",
                font=('Arial', 11), bg='#f0f0f0').pack(anchor='w')
        
        duration_min = timestamps[-1] // 60 if timestamps else 0
        duration_sec = timestamps[-1] % 60 if timestamps else 0
        tk.Label(stats_frame, 
                text=f"Duración: {duration_min} minutos {duration_sec} segundos",
                font=('Arial', 11), bg='#f0f0f0').pack(anchor='w')
        
        # Identificar momentos críticos (ansiedad > 70%)
        critical_moments = [t for t, f in zip(timestamps, emotions['fear']) if f > 70]
        if critical_moments:
            tk.Label(stats_frame, 
                    text=f"Momentos de Alta Ansiedad: {len(critical_moments)} detectados",
                    font=('Arial', 11), bg='#f0f0f0', fg='red').pack(anchor='w')
    
    def compare_sessions(self, session_id1, session_id2):
        """
        Compara dos sesiones lado a lado.
        
        ¿Para qué sirve?
        - Ver si el paciente está mejorando entre sesiones
        - Identificar qué emociones han cambiado más
        - Mostrar progreso visual al paciente
        
        Args:
            session_id1: ID de la primera sesión (anterior)
            session_id2: ID de la segunda sesión (actual)
        """
        self._create_window("Comparación de Sesiones - Dashboard Terapéutico")
        
        # Obtener datos de ambas sesiones
        data1 = self.db.get_session_emotions(session_id1)
        data2 = self.db.get_session_emotions(session_id2)
        
        if not data1 or not data2:
            tk.Label(self.window, text="No hay datos suficientes para comparar",
                    font=('Arial', 14)).pack(pady=50)
            return
        
        # Calcular promedios
        emotions1 = self._calculate_averages(data1)
        emotions2 = self._calculate_averages(data2)
        
        # Crear gráfico comparativo
        fig, ax = plt.subplots(figsize=(10, 6))
        
        emotion_names = list(emotions1.keys())
        x = np.arange(len(emotion_names))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, 
                      [emotions1[e] for e in emotion_names], 
                      width, label='Sesión Anterior', alpha=0.8)
        bars2 = ax.bar(x + width/2, 
                      [emotions2[e] for e in emotion_names], 
                      width, label='Sesión Actual', alpha=0.8)
        
        ax.set_ylabel('Intensidad Promedio (%)')
        ax.set_title('Comparación Entre Sesiones', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([self.emotion_names_es[e] for e in emotion_names])
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 100)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Análisis de cambios
        changes_frame = tk.Frame(self.window, bg='#f0f0f0', padx=20, pady=10)
        changes_frame.pack(fill=tk.X)
        
        tk.Label(changes_frame, text="Análisis de Cambios:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        for emotion in emotion_names:
            change = emotions2[emotion] - emotions1[emotion]
            arrow = "+" if change > 0 else "" if change < 0 else "="
            
            # Determinar si el cambio es positivo o negativo
            if emotion == 'happy':
                color = "green" if change > 0 else "red" if change < 0 else "gray"
            else:  # Para emociones negativas, reducción es buena
                color = "green" if change < 0 else "red" if change > 0 else "gray"
            
            tk.Label(changes_frame, 
                    text=f"  {self.emotion_names_es[emotion]}: {arrow}{change:.1f}%",
                    font=('Arial', 11), bg='#f0f0f0', fg=color).pack(anchor='w')
    
    def _calculate_averages(self, emotion_data):
        """
        Calcula promedios de emociones desde datos de sesión.
        
        Args:
            emotion_data: Lista de tuplas con datos de emociones
            
        Returns:
            dict: Diccionario con promedios de cada emoción
        """
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
        
        Args:
            patient_id: ID anónimo del paciente
        """
        self._create_window(f"Historial del Paciente - Dashboard Terapéutico")
        
        sessions = self.db.get_patient_sessions(patient_id, limit=20)
        
        if not sessions:
            tk.Label(self.window, text=f"No hay sesiones para el paciente {patient_id}",
                    font=('Arial', 14)).pack(pady=50)
            return
        
        # Frame principal
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(main_frame, text=f"Historial del Paciente: {patient_id}", 
                font=('Arial', 14, 'bold')).pack()
        
        # Tabla de sesiones
        tree = ttk.Treeview(main_frame, 
                           columns=('ID', 'Fecha', 'Duración', 'Tipo'), 
                           show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Fecha', text='Fecha')
        tree.heading('Duración', text='Duración (min)')
        tree.heading('Tipo', text='Tipo de Sesión')
        
        tree.column('ID', width=50)
        tree.column('Fecha', width=150)
        tree.column('Duración', width=100)
        tree.column('Tipo', width=150)
        
        for session in sessions:
            session_id, timestamp, duration, session_type, notes = session
            try:
                date = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M')
            except:
                date = timestamp
            
            duration_min = duration // 60 if duration else 0
            tree.insert('', 'end', values=(session_id, date, duration_min, session_type or 'N/A'))
        
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botones de acción
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        def view_selected_session():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                session_id = item['values'][0]
                self.show_session_summary(session_id)
        
        tk.Button(button_frame, text="Ver Sesión Seleccionada", 
                 command=view_selected_session,
                 font=('Arial', 11), padx=10, pady=5).pack(side=tk.LEFT, padx=5)
    
    def show_exercise_results(self, patient_id):
        """
        Muestra historial de ejercicios terapéuticos del paciente.
        
        Args:
            patient_id: ID del paciente
        """
        self._create_window("Resultados de Ejercicios - Dashboard Terapéutico")
        
        exercises = self.db.get_patient_exercise_history(patient_id, limit=20)
        
        if not exercises:
            tk.Label(self.window, text="No hay ejercicios registrados",
                    font=('Arial', 14)).pack(pady=50)
            return
        
        # Frame principal
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text=f"Historial de Ejercicios: {patient_id}",
                font=('Arial', 14, 'bold')).pack()
        
        # Tabla de ejercicios
        tree = ttk.Treeview(main_frame,
                           columns=('Ejercicio', 'Fecha', 'Inicio', 'Final', 'Reducción', 'Éxito'),
                           show='headings')
        tree.heading('Ejercicio', text='Tipo')
        tree.heading('Fecha', text='Fecha')
        tree.heading('Inicio', text='Ansiedad Inicial')
        tree.heading('Final', text='Ansiedad Final')
        tree.heading('Reducción', text='Reducción %')
        tree.heading('Éxito', text='Resultado')
        
        for exercise in exercises:
            exercise_type, timestamp, initial, final, reduction, success = exercise
            try:
                date = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M')
            except:
                date = timestamp
            
            result = "✓ Exitoso" if success else "✗ Sin efecto"
            tree.insert('', 'end', values=(
                exercise_type, date, f"{initial:.1f}%", f"{final:.1f}%", 
                f"{reduction:.1f}%", result
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def run(self):
        """Inicia la interfaz gráfica"""
        if self.window:
            self.window.mainloop()
