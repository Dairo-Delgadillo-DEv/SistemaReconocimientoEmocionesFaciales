# Biblioteca de ejercicios terapéuticos con biofeedback emocional
# Incluye ejercicios de respiración, grounding, relajación y más

import time
import cv2
import numpy as np
from datetime import datetime
import os
import sys

# Agregar el directorio padre al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Intentar importar matplotlib
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class TherapeuticExercises:
    """
    Biblioteca de ejercicios terapéuticos con biofeedback emocional.
    
    Beneficios terapéuticos:
    - Aprendizaje acelerado: Ver resultados inmediatos motiva y enseña
    - Autoeficacia: "Puedo controlar mi ansiedad" (evidencia visual)
    - Personalización: Descubrir qué técnicas funcionan mejor
    - Práctica guiada: No solo teoría, sino práctica con feedback
    - Medición objetiva: Saber si el ejercicio realmente funcionó
    
    Aplicaciones clínicas:
    - Trastornos de ansiedad: Ejercicios de respiración con monitoreo de miedo
    - Depresión: Activación conductual con seguimiento de estado de ánimo
    - Manejo de ira: Técnicas de enfriamiento con feedback visual
    - Mindfulness: Meditación guiada con medición de calma
    - TEPT: Exposición gradual con monitoreo de ansiedad
    """
    
    def __init__(self, emotion_recognition_system, camera):
        """
        Inicializa el sistema de ejercicios terapéuticos.
        
        Args:
            emotion_recognition_system: Instancia del sistema de reconocimiento
            camera: Instancia de la cámara
        """
        self.emotion_system = emotion_recognition_system
        self.camera = camera
        
        # Catálogo de ejercicios disponibles
        self.exercises = {
            'breathing_478': BreathingExercise478(self),
            'grounding_54321': GroundingExercise54321(self),
            'progressive_relaxation': ProgressiveRelaxation(self),
            'mindfulness_breathing': MindfulnessBreathing(self)
        }
    
    def list_exercises(self):
        """Muestra ejercicios disponibles"""
        print("\n" + "=" * 60)
        print("EJERCICIOS TERAPÉUTICOS DISPONIBLES")
        print("=" * 60)
        
        for key, exercise in self.exercises.items():
            print(f"\n  {exercise.name}")
            print(f"  Clave: {key}")
            print(f"  Duración: {exercise.duration} minutos")
            print(f"  Indicado para: {exercise.indications}")
            print(f"  Objetivo: {exercise.goal}")
    
    def start_exercise(self, exercise_key):
        """
        Inicia un ejercicio específico.
        
        Args:
            exercise_key: Clave del ejercicio a iniciar
            
        Returns:
            dict: Resultados del ejercicio o None si no se encontró
        """
        if exercise_key not in self.exercises:
            print(f"Ejercicio '{exercise_key}' no encontrado")
            return None
        
        exercise = self.exercises[exercise_key]
        print(f"\nIniciando: {exercise.name}")
        print(f"Duración estimada: {exercise.duration} minutos\n")
        
        results = exercise.run()
        return results
    
    def get_exercise_info(self, exercise_key):
        """
        Obtiene información de un ejercicio.
        
        Args:
            exercise_key: Clave del ejercicio
            
        Returns:
            dict: Información del ejercicio
        """
        if exercise_key not in self.exercises:
            return None
        
        exercise = self.exercises[exercise_key]
        return {
            'name': exercise.name,
            'duration': exercise.duration,
            'indications': exercise.indications,
            'goal': exercise.goal
        }


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
        """
        Inicializa el ejercicio.
        
        Args:
            parent: Instancia de TherapeuticExercises
        """
        self.parent = parent
        self.name = "Respiración 4-7-8"
        self.duration = 5
        self.indications = "Ansiedad, estrés, insomnio, ataques de pánico"
        self.goal = "Reducir ansiedad en 30-50%"
        
        # Datos de la sesión
        self.emotion_timeline = []
        self.timestamps = []
    
    def run(self):
        """
        Ejecuta el ejercicio con guía visual y monitoreo.
        
        Returns:
            dict: Resultados del ejercicio
        """
        print("=" * 60)
        print("EJERCICIO: RESPIRACIÓN 4-7-8")
        print("=" * 60)
        print("\nInstrucciones:")
        print("1. Siéntese cómodamente con la espalda recta")
        print("2. Coloque la punta de la lengua detrás de los dientes superiores")
        print("3. Siga las instrucciones en pantalla")
        print("4. El sistema monitoreará su nivel de ansiedad\n")
        
        input("Presione ENTER cuando esté listo...")
        
        # Reiniciar datos
        self.emotion_timeline = []
        self.timestamps = []
        
        # Medir ansiedad inicial
        print("\n  Midiendo nivel de ansiedad inicial...")
        initial_anxiety = self._measure_current_anxiety(duration=10)
        print(f"Ansiedad inicial: {initial_anxiety:.1f}%")
        
        # Realizar 6 ciclos de respiración
        num_cycles = 6
        for cycle in range(1, num_cycles + 1):
            print(f"\n  Ciclo {cycle}/{num_cycles}")
            self._breathing_cycle()
            
            # Medir ansiedad después de cada ciclo
            current_anxiety = self._measure_current_anxiety(duration=5)
            reduction = initial_anxiety - current_anxiety
            
            print(f"  Ansiedad actual: {current_anxiety:.1f}% "
                  f"(reducción: {reduction:.1f}%)")
            
            if reduction > 0:
                print(f"  ¡Bien! La ansiedad está bajando")
            
            time.sleep(2)  # Pausa entre ciclos
        
        # Medir ansiedad final
        print("\n  Midiendo nivel de ansiedad final...")
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
        """
        Mide nivel promedio de ansiedad durante X segundos.
        
        Args:
            duration: Segundos de medición
            
        Returns:
            float: Nivel promedio de ansiedad
        """
        anxiety_samples = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            ret, frame = self.parent.camera.read()
            if not ret:
                continue
            
            # Procesar frame
            frame = self.parent.emotion_system.frame_processing(frame)
            
            # Obtener nivel de miedo (proxy de ansiedad)
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
        """
        Muestra resultados visuales del ejercicio.
        
        Args:
            results: Diccionario con resultados
        """
        cv2.destroyAllWindows()
        
        print("\n" + "=" * 60)
        print("RESULTADOS DEL EJERCICIO")
        print("=" * 60)
        print(f"\n  Ansiedad inicial: {results['initial_anxiety']:.1f}%")
        print(f"  Ansiedad final: {results['final_anxiety']:.1f}%")
        print(f"  Reducción: {results['reduction']:.1f}% "
              f"({results['reduction_percent']:.1f}% de mejora)")
        
        if results['success']:
            print("\n  ¡ÉXITO! El ejercicio redujo su ansiedad")
            if results['reduction_percent'] > 50:
                print("   ¡Excelente resultado! Reducción mayor al 50%")
            elif results['reduction_percent'] > 30:
                print("   Buen resultado. Reducción significativa.")
            else:
                print("   Reducción moderada. Considere practicar más.")
        else:
            print("\n  No se detectó reducción de ansiedad")
            print("   Esto puede deberse a:")
            print("   - Necesita más práctica con la técnica")
            print("   - El nivel de ansiedad inicial era bajo")
            print("   - Factores externos interfirieron")
        
        # Crear gráfico de evolución si matplotlib está disponible
        if MATPLOTLIB_AVAILABLE and len(results['timeline']) > 0:
            self._plot_anxiety_evolution(results)
    
    def _plot_anxiety_evolution(self, results):
        """
        Genera gráfico de evolución de ansiedad.
        
        Args:
            results: Diccionario con resultados
        """
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
        filename = f'breathing_exercise_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(filename)
        plt.show()
        
        print(f"\n  Gráfico guardado en: {filename}")


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
        """
        Inicializa el ejercicio.
        
        Args:
            parent: Instancia de TherapeuticExercises
        """
        self.parent = parent
        self.name = "Grounding 5-4-3-2-1"
        self.duration = 8
        self.indications = "Ataques de pánico, disociación, ansiedad aguda"
        self.goal = "Reducir ansiedad y volver al presente"
        
        self.emotion_timeline = []
        self.timestamps = []
    
    def run(self):
        """
        Ejecuta ejercicio de grounding con monitoreo.
        
        Returns:
            dict: Resultados del ejercicio
        """
        print("=" * 60)
        print("EJERCICIO: GROUNDING 5-4-3-2-1")
        print("=" * 60)
        print("\nEste ejercicio le ayudará a conectar con el momento presente")
        print("usando sus cinco sentidos.\n")
        
        input("Presione ENTER para comenzar...")
        
        # Reiniciar datos
        self.emotion_timeline = []
        self.timestamps = []
        
        # Medir ansiedad inicial
        initial_anxiety = self._measure_anxiety(10)
        print(f"\n  Ansiedad inicial: {initial_anxiety:.1f}%")
        
        steps = [
            ("VISTA", 5, "Nombre 5 cosas que puede VER a su alrededor"),
            ("TACTO", 4, "Nombre 4 cosas que puede TOCAR"),
            ("OÍDO", 3, "Nombre 3 cosas que puede OÍR"),
            ("OLFATO", 2, "Nombre 2 cosas que puede OLER"),
            ("GUSTO", 1, "Nombre 1 cosa que puede SABOREAR")
        ]
        
        anxiety_per_step = [initial_anxiety]
        step_data = []
        
        for sense, count, instruction in steps:
            print(f"\n  {sense}: {instruction}")
            
            items = []
            for i in range(1, count + 1):
                item = input(f"   {i}. ")
                items.append(item)
                print(f"      ✓ {item}")
            
            # Medir ansiedad después de cada sentido
            current_anxiety = self._measure_anxiety(5)
            anxiety_per_step.append(current_anxiety)
            reduction = anxiety_per_step[-2] - current_anxiety
            
            step_data.append({
                'sense': sense,
                'items': items,
                'anxiety': current_anxiety,
                'reduction': reduction
            })
            
            print(f"\n     Ansiedad: {current_anxiety:.1f}% "
                  f"(cambio: {reduction:+.1f}%)")
        
        # Resultados finales
        final_anxiety = anxiety_per_step[-1]
        total_reduction = initial_anxiety - final_anxiety
        
        results = {
            'exercise': 'grounding_54321',
            'initial_anxiety': initial_anxiety,
            'final_anxiety': final_anxiety,
            'reduction': total_reduction,
            'reduction_percent': (total_reduction / initial_anxiety * 100) if initial_anxiety > 0 else 0,
            'anxiety_per_step': anxiety_per_step,
            'step_data': step_data,
            'timeline': self.emotion_timeline,
            'timestamps': self.timestamps,
            'success': total_reduction > 0
        }
        
        self._show_results(results)
        return results
    
    def _measure_anxiety(self, duration):
        """
        Mide ansiedad promedio.
        
        Args:
            duration: Segundos de medición
            
        Returns:
            float: Nivel promedio de ansiedad
        """
        anxiety_samples = []
        start_time = time.time()
        
        print(f"     Midiendo nivel de ansiedad ({duration}s)...")
        
        while time.time() - start_time < duration:
            ret, frame = self.parent.camera.read()
            if not ret:
                continue
            
            # Procesar frame
            frame = self.parent.emotion_system.frame_processing(frame)
            
            try:
                emotions = self.parent.emotion_system.emotions_recognition.last_emotions
                anxiety = emotions.get('fear', 0)
                anxiety_samples.append(anxiety)
                
                self.emotion_timeline.append(emotions.copy())
                self.timestamps.append(time.time())
            except:
                pass
            
            cv2.imshow('Grounding Exercise', frame)
            cv2.waitKey(1)
        
        return np.mean(anxiety_samples) if anxiety_samples else 0
    
    def _show_results(self, results):
        """
        Muestra resultados del ejercicio.
        
        Args:
            results: Diccionario con resultados
        """
        cv2.destroyAllWindows()
        
        print("\n" + "=" * 60)
        print("RESULTADOS")
        print("=" * 60)
        print(f"\n  Reducción total: {results['reduction']:.1f}%")
        
        if results['success']:
            print("  ¡El ejercicio fue efectivo!")
            
            # Mostrar qué paso fue más efectivo
            max_reduction = 0
            best_step = None
            for step in results['step_data']:
                if step['reduction'] > max_reduction:
                    max_reduction = step['reduction']
                    best_step = step['sense']
            
            if best_step:
                print(f"  El paso más efectivo fue: {best_step}")
        else:
            print("  Considere repetir o probar otra técnica")


class ProgressiveRelaxation:
    """
    Relajación Muscular Progresiva (Jacobson)
    
    ¿Qué es?
    - Tensionar y relajar grupos musculares sistemáticamente
    - Desde los pies hasta la cabeza
    - 5-7 segundos de tensión, 20-30 segundos de relajación
    
    ¿Para qué sirve?
    - Reducir tensión muscular crónica
    - Aliviar síntomas físicos de ansiedad
    - Mejorar conciencia corporal
    - Preparar para dormir
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.name = "Relajación Muscular Progresiva"
        self.duration = 15
        self.indications = "Tensión muscular, ansiedad, estrés crónico"
        self.goal = "Reducir tensión física y mental"
        
        self.muscle_groups = [
            ("Pies", "Curve los dedos de los pies hacia abajo"),
            ("Pantorrillas", "Apunte los pies hacia arriba"),
            ("Muslos", "Apriete los muslos"),
            ("Glúteos", "Contraiga los glúteos"),
            ("Abdomen", "Contraiga el abdomen"),
            ("Pecho", "Respire profundo y retenga"),
            ("Manos", "Haga puños apretados"),
            ("Brazos", "Doble los brazos y tense los bíceps"),
            ("Hombros", "Suba los hombros hacia las orejas"),
            ("Cara", "Arrugue toda la cara")
        ]
        
        self.emotion_timeline = []
        self.timestamps = []
    
    def run(self):
        """
        Ejecuta la relajación progresiva.
        
        Returns:
            dict: Resultados del ejercicio
        """
        print("=" * 60)
        print("EJERCICIO: RELAJACIÓN MUSCULAR PROGRESIVA")
        print("=" * 60)
        print("\nEste ejercicio le enseñará a reconocer y liberar tensión muscular.")
        print("\nPara cada grupo muscular:")
        print("1. Tensar el músculo por 5-7 segundos")
        print("2. Relajar y notar la diferencia por 20 segundos\n")
        
        input("Presione ENTER para comenzar...")
        
        # Reiniciar datos
        self.emotion_timeline = []
        self.timestamps = []
        
        # Medir ansiedad inicial
        initial_anxiety = self._measure_anxiety(10)
        print(f"\n  Ansiedad inicial: {initial_anxiety:.1f}%")
        
        # Realizar ejercicio para cada grupo muscular
        for i, (muscle, instruction) in enumerate(self.muscle_groups, 1):
            print(f"\n  [{i}/{len(self.muscle_groups)}] {muscle}")
            print(f"  {instruction}")
            
            # Fase de tensión
            self._show_phase("TENSAR", muscle, 6, (0, 0, 255))  # Rojo
            
            # Fase de relajación
            self._show_phase("RELAJAR", muscle, 20, (0, 255, 0))  # Verde
        
        # Medir ansiedad final
        print("\n  Midiendo nivel de ansiedad final...")
        final_anxiety = self._measure_anxiety(10)
        total_reduction = initial_anxiety - final_anxiety
        
        results = {
            'exercise': 'progressive_relaxation',
            'initial_anxiety': initial_anxiety,
            'final_anxiety': final_anxiety,
            'reduction': total_reduction,
            'reduction_percent': (total_reduction / initial_anxiety * 100) if initial_anxiety > 0 else 0,
            'muscle_groups_completed': len(self.muscle_groups),
            'timeline': self.emotion_timeline,
            'timestamps': self.timestamps,
            'success': total_reduction > 0
        }
        
        self._show_results(results)
        return results
    
    def _show_phase(self, phase_name, muscle, duration, color):
        """
        Muestra una fase del ejercicio.
        
        Args:
            phase_name: Nombre de la fase (TENSAR/RELAJAR)
            muscle: Nombre del músculo
            duration: Duración en segundos
            color: Color BGR para la visualización
        """
        start_time = time.time()
        
        while time.time() - start_time < duration:
            ret, frame = self.parent.camera.read()
            if not ret:
                continue
            
            frame = self.parent.emotion_system.frame_processing(frame)
            
            # Registrar emociones
            try:
                emotions = self.parent.emotion_system.emotions_recognition.last_emotions
                self.emotion_timeline.append(emotions.copy())
                self.timestamps.append(time.time())
            except:
                pass
            
            # Overlay
            remaining = int(duration - (time.time() - start_time))
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 0, 0), -1)
            cv2.putText(frame, f"{phase_name}: {muscle}", 
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
            cv2.putText(frame, f"{remaining}s", 
                       (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            cv2.imshow('Relajacion Progresiva', frame)
            cv2.waitKey(1)
    
    def _measure_anxiety(self, duration):
        """Mide ansiedad promedio."""
        anxiety_samples = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            ret, frame = self.parent.camera.read()
            if not ret:
                continue
            
            frame = self.parent.emotion_system.frame_processing(frame)
            
            try:
                emotions = self.parent.emotion_system.emotions_recognition.last_emotions
                anxiety_samples.append(emotions.get('fear', 0))
            except:
                pass
            
            cv2.imshow('Relajacion Progresiva', frame)
            cv2.waitKey(1)
        
        return np.mean(anxiety_samples) if anxiety_samples else 0
    
    def _show_results(self, results):
        """Muestra resultados del ejercicio."""
        cv2.destroyAllWindows()
        
        print("\n" + "=" * 60)
        print("RESULTADOS")
        print("=" * 60)
        print(f"\n  Ansiedad inicial: {results['initial_anxiety']:.1f}%")
        print(f"  Ansiedad final: {results['final_anxiety']:.1f}%")
        print(f"  Reducción: {results['reduction']:.1f}%")
        
        if results['success']:
            print("\n  ¡El ejercicio fue efectivo!")
        else:
            print("\n  Practique regularmente para mejores resultados")


class MindfulnessBreathing:
    """
    Respiración Consciente (Mindfulness)
    
    ¿Qué es?
    - Observar la respiración sin modificarla
    - Notar sensaciones sin juzgar
    - Volver a la respiración cuando la mente divague
    
    ¿Para qué sirve?
    - Desarrollar atención plena
    - Reducir rumiación mental
    - Mejorar regulación emocional
    - Reducir estrés crónico
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.name = "Respiración Consciente (Mindfulness)"
        self.duration = 5
        self.indications = "Estrés, rumiación, dificultad de concentración"
        self.goal = "Desarrollar atención plena y calma"
        
        self.emotion_timeline = []
        self.timestamps = []
    
    def run(self):
        """
        Ejecuta la práctica de mindfulness.
        
        Returns:
            dict: Resultados del ejercicio
        """
        print("=" * 60)
        print("EJERCICIO: RESPIRACIÓN CONSCIENTE (MINDFULNESS)")
        print("=" * 60)
        print("\nInstrucciones:")
        print("1. Observe su respiración natural, sin cambiarla")
        print("2. Note las sensaciones: aire entrando, pecho expandiendo")
        print("3. Cuando su mente divague, suavemente vuelva a la respiración")
        print("4. No juzgue los pensamientos, solo obsérvelos pasar\n")
        
        duration_seconds = self.duration * 60  # Convertir a segundos
        input(f"La práctica durará {self.duration} minutos. Presione ENTER para comenzar...")
        
        # Reiniciar datos
        self.emotion_timeline = []
        self.timestamps = []
        
        # Medir estado inicial
        initial_anxiety = self._measure_anxiety(10)
        initial_happiness = self._measure_happiness(5)
        print(f"\n  Ansiedad inicial: {initial_anxiety:.1f}%")
        print(f"  Bienestar inicial: {initial_happiness:.1f}%")
        
        print("\n  Comenzando práctica de mindfulness...")
        
        # Práctica principal
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            ret, frame = self.parent.camera.read()
            if not ret:
                continue
            
            frame = self.parent.emotion_system.frame_processing(frame)
            
            try:
                emotions = self.parent.emotion_system.emotions_recognition.last_emotions
                self.emotion_timeline.append(emotions.copy())
                self.timestamps.append(time.time())
            except:
                pass
            
            # Mostrar tiempo restante y recordatorios suaves
            elapsed = time.time() - start_time
            remaining = duration_seconds - elapsed
            remaining_min = int(remaining // 60)
            remaining_sec = int(remaining % 60)
            
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (0, 0, 0), -1)
            cv2.putText(frame, "Observe su respiracion...", 
                       (50, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Tiempo restante: {remaining_min}:{remaining_sec:02d}", 
                       (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            cv2.imshow('Mindfulness', frame)
            
            # Permitir salir con ESC
            if cv2.waitKey(1) == 27:
                break
        
        # Medir estado final
        print("\n  Midiendo estado final...")
        final_anxiety = self._measure_anxiety(10)
        final_happiness = self._measure_happiness(5)
        
        results = {
            'exercise': 'mindfulness_breathing',
            'initial_anxiety': initial_anxiety,
            'final_anxiety': final_anxiety,
            'initial_happiness': initial_happiness,
            'final_happiness': final_happiness,
            'anxiety_reduction': initial_anxiety - final_anxiety,
            'happiness_increase': final_happiness - initial_happiness,
            'duration_completed': time.time() - start_time,
            'timeline': self.emotion_timeline,
            'timestamps': self.timestamps,
            'success': (initial_anxiety - final_anxiety) > 0 or (final_happiness - initial_happiness) > 0
        }
        
        self._show_results(results)
        return results
    
    def _measure_anxiety(self, duration):
        """Mide ansiedad promedio."""
        samples = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            ret, frame = self.parent.camera.read()
            if not ret:
                continue
            
            frame = self.parent.emotion_system.frame_processing(frame)
            
            try:
                emotions = self.parent.emotion_system.emotions_recognition.last_emotions
                samples.append(emotions.get('fear', 0))
            except:
                pass
            
            cv2.imshow('Mindfulness', frame)
            cv2.waitKey(1)
        
        return np.mean(samples) if samples else 0
    
    def _measure_happiness(self, duration):
        """Mide felicidad promedio."""
        samples = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            ret, frame = self.parent.camera.read()
            if not ret:
                continue
            
            frame = self.parent.emotion_system.frame_processing(frame)
            
            try:
                emotions = self.parent.emotion_system.emotions_recognition.last_emotions
                samples.append(emotions.get('happy', 0))
            except:
                pass
            
            cv2.imshow('Mindfulness', frame)
            cv2.waitKey(1)
        
        return np.mean(samples) if samples else 0
    
    def _show_results(self, results):
        """Muestra resultados del ejercicio."""
        cv2.destroyAllWindows()
        
        print("\n" + "=" * 60)
        print("RESULTADOS")
        print("=" * 60)
        print(f"\n  Ansiedad: {results['initial_anxiety']:.1f}% → {results['final_anxiety']:.1f}%")
        print(f"  Bienestar: {results['initial_happiness']:.1f}% → {results['final_happiness']:.1f}%")
        
        if results['anxiety_reduction'] > 0:
            print(f"\n  ✓ Reducción de ansiedad: {results['anxiety_reduction']:.1f}%")
        
        if results['happiness_increase'] > 0:
            print(f"  ✓ Aumento de bienestar: {results['happiness_increase']:.1f}%")
        
        if results['success']:
            print("\n  ¡La práctica tuvo efectos positivos!")
        else:
            print("\n  Continúe practicando regularmente")
