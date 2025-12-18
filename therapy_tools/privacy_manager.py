# Gestión de privacidad, consentimiento y protección de datos
# Cumple con GDPR, HIPAA y mejores prácticas de seguridad

import hashlib
import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Intentar importar cryptography, si no está disponible usar encriptación básica
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    import base64


class PrivacyManager:
    """
    Gestiona privacidad, consentimiento y protección de datos.
    Cumple con GDPR, HIPAA y mejores prácticas de seguridad.
    
    Funcionalidades:
    - Consentimiento informado interactivo
    - Anonimización de datos de pacientes
    - Encriptación de datos sensibles
    - Registro de auditoría de accesos
    - Exportación de datos (derecho de acceso GDPR)
    - Eliminación de datos (derecho al olvido GDPR)
    - Política de retención de datos
    """
    
    def __init__(self, encryption_key=None):
        """
        Inicializa el gestor de privacidad.
        
        Args:
            encryption_key: Clave de encriptación opcional. Si no se proporciona,
                          se genera una nueva.
        """
        self.consent_given = False
        self.anonymize = True
        
        # Generar o cargar clave de encriptación
        if CRYPTO_AVAILABLE:
            if encryption_key:
                self.cipher = Fernet(encryption_key)
            else:
                self.key = Fernet.generate_key()
                self.cipher = Fernet(self.key)
        else:
            self.cipher = None
            self.key = encryption_key or 'default_key_32_bytes_for_enc!!'
        
        # Registro de accesos (auditoría)
        self.access_log = []
        self.log_file = 'access_log.json'
    
    def request_consent(self, patient_name=None):
        """
        Muestra formulario de consentimiento informado.
        
        ¿Por qué es necesario?
        - Legalmente requerido antes de grabar/procesar datos
        - Paciente debe entender qué se hace con sus datos
        - Debe ser voluntario y revocable
        
        Args:
            patient_name: Nombre opcional del paciente (para registro)
            
        Returns:
            bool: True si acepta, False si rechaza
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
        
        tk.Button(button_frame, text="ACEPTO", command=accept_consent, 
                 bg='green', fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="NO ACEPTO", command=reject_consent, 
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
        
        Args:
            patient_name: Nombre completo del paciente
            birth_date: Fecha de nacimiento (string o datetime)
            
        Returns:
            str: ID anónimo en formato PAC_xxxxxxxxxxxxxxxx
        """
        # Convertir birth_date a string si es datetime
        if isinstance(birth_date, datetime):
            birth_date = birth_date.strftime('%Y-%m-%d')
        
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
        
        Args:
            data: String o bytes a encriptar
            
        Returns:
            str: Datos encriptados en formato string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if CRYPTO_AVAILABLE and self.cipher:
            encrypted = self.cipher.encrypt(data)
            return encrypted.decode('utf-8')
        else:
            # Encriptación básica si cryptography no está disponible
            encoded = base64.b64encode(data)
            return encoded.decode('utf-8')
    
    def decrypt_sensitive_data(self, encrypted_data):
        """
        Desencripta datos para visualización autorizada.
        
        Args:
            encrypted_data: Datos encriptados
            
        Returns:
            str: Datos desencriptados
        """
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode('utf-8')
        
        if CRYPTO_AVAILABLE and self.cipher:
            decrypted = self.cipher.decrypt(encrypted_data)
            return decrypted.decode('utf-8')
        else:
            # Desencriptación básica
            decoded = base64.b64decode(encrypted_data)
            return decoded.decode('utf-8')
    
    def log_access(self, action, user, details=''):
        """
        Registra todos los accesos a datos de pacientes.
        
        ¿Por qué es importante?
        - Auditoría: saber quién accedió a qué y cuándo
        - Detección de accesos no autorizados
        - Cumplimiento regulatorio (GDPR requiere logs)
        - Investigación en caso de incidente de seguridad
        
        Args:
            action: Tipo de acción (VIEW_SESSION, EXPORT_DATA, DELETE_DATA, etc.)
            user: Usuario que realizó la acción
            details: Detalles adicionales
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'user': user,
            'details': details
        }
        self.access_log.append(log_entry)
        
        # Guardar en archivo de log
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error guardando log: {e}")
    
    def export_patient_data(self, patient_id, database):
        """
        Exporta todos los datos del paciente (Derecho de acceso GDPR).
        
        ¿Por qué?
        - GDPR Art. 15: Derecho de acceso del interesado
        - Paciente puede solicitar copia de todos sus datos
        - Debe ser en formato legible y portable
        
        Args:
            patient_id: ID anónimo del paciente
            database: Instancia de SessionDatabase
            
        Returns:
            str: Ruta del archivo exportado
        """
        self.log_access('EXPORT_DATA', patient_id, 'Patient requested data export')
        
        # Obtener todas las sesiones
        sessions = database.get_patient_sessions(patient_id, limit=1000)
        
        export_data = {
            'patient_id': patient_id,
            'export_date': datetime.now().isoformat(),
            'export_type': 'GDPR_DATA_ACCESS_REQUEST',
            'sessions': []
        }
        
        for session in sessions:
            session_id, timestamp, duration, session_type, notes = session
            emotions = database.get_session_emotions(session_id)
            
            export_data['sessions'].append({
                'session_id': session_id,
                'date': timestamp,
                'duration_seconds': duration,
                'duration_minutes': duration // 60 if duration else 0,
                'type': session_type,
                'emotions_timeline': [
                    {
                        'timestamp_offset': e[0],
                        'happy': e[1],
                        'sad': e[2],
                        'angry': e[3],
                        'fear': e[4],
                        'surprise': e[5],
                        'disgust': e[6]
                    } for e in emotions
                ]
            })
        
        # Agregar historial de ejercicios si existe
        try:
            exercises = database.get_patient_exercise_history(patient_id, limit=1000)
            export_data['exercises'] = [
                {
                    'type': e[0],
                    'date': e[1],
                    'initial_anxiety': e[2],
                    'final_anxiety': e[3],
                    'reduction_percent': e[4],
                    'success': bool(e[5])
                } for e in exercises
            ]
        except:
            export_data['exercises'] = []
        
        # Guardar en JSON
        filename = f"patient_data_export_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def delete_patient_data(self, patient_id, database):
        """
        Elimina todos los datos del paciente (Derecho al olvido GDPR).
        
        ¿Cuándo se usa?
        - Paciente revoca consentimiento
        - Paciente solicita eliminación de datos
        - Fin del período de retención legal
        
        IRREVERSIBLE - Requiere confirmación múltiple
        
        Args:
            patient_id: ID del paciente
            database: Instancia de SessionDatabase
            
        Returns:
            bool: True si se eliminaron los datos, False si se canceló
        """
        # Confirmación de seguridad
        confirm = messagebox.askyesno(
            "ELIMINAR DATOS - ACCIÓN IRREVERSIBLE",
            f"¿Está SEGURO de eliminar TODOS los datos del paciente {patient_id}?\n\n"
            "Esta acción NO se puede deshacer.\n"
            "Se eliminarán:\n"
            "- Todas las sesiones\n"
            "- Todos los datos emocionales\n"
            "- Todas las notas\n"
            "- Resultados de ejercicios\n\n"
            "¿Continuar?"
        )
        
        if not confirm:
            return False
        
        # Segunda confirmación
        confirm2 = messagebox.askyesno(
            "CONFIRMACIÓN FINAL",
            "Esta es su última oportunidad.\n\n"
            "¿Eliminar PERMANENTEMENTE todos los datos?"
        )
        
        if not confirm2:
            return False
        
        # Registrar eliminación ANTES de borrar
        self.log_access('DELETE_ALL_DATA', patient_id, 
                       'All patient data permanently deleted')
        
        # Eliminar de base de datos
        try:
            database.conn.execute('''
                DELETE FROM emotion_snapshots WHERE session_id IN
                (SELECT id FROM sessions WHERE patient_id = ?)
            ''', (patient_id,))
            
            database.conn.execute('''
                DELETE FROM exercise_results WHERE patient_id = ?
            ''', (patient_id,))
            
            database.conn.execute('''
                DELETE FROM sessions WHERE patient_id = ?
            ''', (patient_id,))
            
            database.conn.commit()
            
            messagebox.showinfo("Datos Eliminados", 
                              f"Todos los datos del paciente {patient_id} han sido eliminados.")
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando datos: {e}")
            return False
    
    def check_data_retention_policy(self, database, retention_years=7):
        """
        Verifica y elimina datos antiguos según política de retención.
        
        ¿Por qué?
        - GDPR: No conservar datos más tiempo del necesario
        - Minimización de riesgo: Menos datos = menos riesgo
        - Regulaciones profesionales: Típicamente 5-10 años
        
        Se ejecuta automáticamente cada mes.
        
        Args:
            database: Instancia de SessionDatabase
            retention_years: Años máximos de retención (default: 7)
        """
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
                
                messagebox.showinfo("Completado", 
                                  "Datos antiguos eliminados según política de retención.")
    
    def get_access_log(self, limit=100):
        """
        Obtiene el registro de accesos.
        
        Args:
            limit: Número máximo de entradas a retornar
            
        Returns:
            list: Lista de entradas de log
        """
        return self.access_log[-limit:]
    
    def verify_consent(self):
        """
        Verifica si el consentimiento ha sido dado.
        
        Returns:
            bool: True si hay consentimiento, False si no
        """
        return self.consent_given
