# Librería del propio speech_recognition
import speech_recognition as sr

class ReconocerVoz:
    def __init__(self):
        """
                Constructor de la clase ReconocerVoz.

                Inicializa el objeto Recognizer para el reconocimiento de voz.
                """
        self.r = sr.Recognizer()  # Crea un objeto Recognizer para el reconocimiento de voz

    def reconocer_voz(self):
        """
        Función para reconocer voz a través del micrófono.
        Utiliza el micrófono como fuente de audio para escuchar al usuario.
        Utiliza el reconocedor de voz de Google para convertir el audio a texto.
    
        Returns:
        - str: El texto reconocido a partir del audio, o None si no se reconoce nada.
        """
        intento = 0
        while intento < 2:
            try:
                with sr.Microphone() as source:
                    print("Escuchando...")
                    audio = self.r.listen(source, timeout=5)
                    print("Procesando audio...")
                    text = self.r.recognize_google(audio, language='es-ES')
                    if text:
                        return text
            except sr.UnknownValueError:
                print("Google Speech Recognition no pudo entender el audio, intenta de nuevo")
            except sr.RequestError as e:
                print("No se pudo solicitar resultados a Google Speech Recognition; {0}".format(e))
            except sr.WaitTimeoutError:
                print("Tiempo de espera agotado. No se detectó audio.")
            intento += 1
        print("Número máximo de intentos alcanzado. No se pudo reconocer el audio.")
        return ""
