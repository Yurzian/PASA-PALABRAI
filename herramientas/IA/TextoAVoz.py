# Libreria propia de pyttsx3
import pyttsx3

class TextoAVoz:
    def __init__(self):
        """
                Constructor de la clase TextoAVoz.

                Inicializa el motor de texto a voz con la velocidad y volumen del habla configurados.
                """
        self.engine = pyttsx3.init()
        # Establezco la velocidad y el volumen del habla
        self.engine.setProperty('rate', 150)  # Velocidad de habla (palabras por minuto)
        self.engine.setProperty('volume', 0.9)  # Volumen del habla (0.0 a 1.0)

    def convertir_texto(self, texto):
        """
                Convierte un texto a voz y lo guarda en un archivo de audio.

                Parameters:
                - texto (str): El texto que se convertirá a voz.
                """
        self.engine.save_to_file(texto, "recursos/audio/definicion.wav")
        self.engine.runAndWait()
