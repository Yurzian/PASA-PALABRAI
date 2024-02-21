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
                - str: El texto reconocido a partir del audio.
                """
        while True:
            try:
                # Usa el micrófono como fuente de audio
                with sr.Microphone() as source:
                    # Escucha el audio a través del micrófono
                    audio = self.r.listen(source, timeout=5)  # Se establece un tiempo límite de 5 segundos

                    # Usa el reconocedor de voz de Google para convertir el audio a texto
                    text = self.r.recognize_google(audio, language='es-ES')
                    if text:
                        return text
            except sr.UnknownValueError:
                print("Google Speech Recognition no pudo entender el audio, intenta de nuevo")
            except sr.RequestError as e:
                print("No se pudo solicitar resultados a Google Speech Recognition; {0}".format(e))
            except sr.WaitTimeoutError:  # Agregar una excepción para el tiempo de espera
                print("Tiempo de espera agotado. No se detectó audio.")