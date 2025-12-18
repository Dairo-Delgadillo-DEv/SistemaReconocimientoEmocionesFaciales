# Importa las clases abstractas base para verificar características faciales
from emotion_processor.emotions_recognition.features.feature_check import (EyebrowsCheck, EyesCheck, NoseCheck,
                                                                           MouthCheck)


# Implementación básica para verificar el estado de las cejas
class BasicEyebrowsCheck(EyebrowsCheck):
    # Analiza las métricas de las cejas y retorna una descripción textual de su estado
    def check_eyebrows(self, eyebrows: dict) -> str:
        # Lista para almacenar los resultados del análisis
        results = []
        # Extrae las distancias de la ceja derecha al ojo y a la frente
        eye_right, forehead_right = eyebrows['eye_right_distance'], eyebrows['forehead_right_distance']
        # Extrae las distancias de la ceja izquierda al ojo y a la frente
        eye_left, forehead_left = eyebrows['eye_left_distance'], eyebrows['forehead_left_distance']
        # Extrae la distancia entre cejas y la distancia a la frente
        eyebrows_distance, forehead_distance = eyebrows['eyebrows_distance'], eyebrows['eyebrow_distance_forehead']

        # Determina si las cejas están separadas o juntas
        if eyebrows_distance > forehead_distance:
            results.append('eyebrows separated')
        else:
            results.append('eyebrows together')

        # Determina si la ceja derecha está levantada o bajada
        results.append('right eyebrow: raised' if eye_right > forehead_right else 'right eyebrow: lowered')
        # Determina si la ceja izquierda está levantada o bajada
        results.append('left eyebrow: raised' if eye_left > forehead_left else 'left eyebrow: lowered')

        # Retorna todos los resultados unidos por comas
        return ', '.join(results)


# Implementación básica para verificar el estado de los ojos
class BasicEyesCheck(EyesCheck):
    # Analiza las métricas de los ojos y retorna una descripción textual de su estado
    def check_eyes(self, eyes: dict) -> str:
        # Extrae las distancias de los párpados superior e inferior del ojo derecho
        right_eyelid_upper, right_eyelid_lower = eyes['right_upper_eyelid_distance'], eyes[
            'right_lower_eyelid_distance']
        # Extrae las distancias de los párpados superior e inferior del ojo izquierdo
        left_eyelid_upper, left_eyelid_lower = eyes['left_upper_eyelid_distance'], eyes['left_lower_eyelid_distance']

        # Determina si los ojos están abiertos o cerrados comparando párpados
        results = ['open eyes' if right_eyelid_upper > right_eyelid_lower else 'closed eyes']

        # Retorna el resultado como string
        return ', '.join(results)


# Implementación básica para verificar el estado de la nariz
class BasicNoseCheck(NoseCheck):
    # Analiza las métricas de la nariz y retorna una descripción textual de su estado
    def check_nose(self, nose: dict) -> str:
        # Extrae las distancias de la nariz a la boca y de la parte inferior de la nariz
        mouth_upper, nose_lower = nose['mouth_upper_distance'], nose['nose_lower_distance']

        # Determina si la nariz está arrugada o neutral
        return 'wrinkled nose' if mouth_upper > nose_lower else 'neutral nose'


# Implementación básica para verificar el estado de la boca
class BasicMouthCheck(MouthCheck):
    # Analiza las métricas de la boca y retorna una descripción textual de su estado
    def check_mouth(self, mouth: dict) -> str:
        # Lista para almacenar los resultados del análisis
        results = []
        # Extrae las distancias de apertura de los labios superior e inferior
        lips_upper, lips_lower = mouth['mouth_upper_distance'], mouth['mouth_lower_distance']
        # Extrae las distancias de la sonrisa y labio derechos
        right_smile, right_lip = mouth['right_smile_distance'], mouth['right_lip_distance']
        # Extrae las distancias de la sonrisa y labio izquierdos
        left_smile, left_lip = mouth['left_smile_distance'], mouth['left_lip_distance']

        # Determina si la boca está abierta o cerrada
        if lips_upper > lips_lower:
            results.append('open mouth')
        else:
            results.append('closed mouth')

        # Determina si hay sonrisa en el lado derecho
        results.append('right smile' if right_lip > right_smile else 'no right smile')
        # Determina si hay sonrisa en el lado izquierdo
        results.append('left smile' if left_lip > left_smile else 'no left smile')

        # Retorna todos los resultados unidos por comas
        return ', '.join(results)
