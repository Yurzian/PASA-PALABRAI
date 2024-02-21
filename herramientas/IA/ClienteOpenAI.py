# Librería principal de openai
from openai import OpenAI
# Librería donde se encuentra la credencial de openai
from credenciales import openai_key

class ClienteOpenAI:
    def __init__(self):
        """
                Inicializa la clase ClienteOpenAI.

                Crea un cliente para interactuar con la API de OpenAI, usando la key del archivo credenciales
                """
        self.client = OpenAI(api_key=openai_key)

    def generar_lista_palabras(self, dificultad="", tema=""):
        """
                Genera una lista de palabras utilizando la API de OpenAI.
                La funcionalidad está sacada del github de OpenAI.

                Parameters:
                - dificultad (str): La dificultad de las palabras a generar.
                - tema (str): El tema relacionado con las palabras a generar.

                Returns:
                - list: Una lista de palabras generadas.
                """
        if tema != "":
            tema = f"que tengan que ver con {tema}"
        # Texto de entrada para GPT-3.5
        prompt = (f" respondeme solo con una palabra de dificultad {dificultad}, totalmente aleatorias, en español,"
                         f" {tema}, que empiece con cada una de estas letras(A B C D E F G H I J L M N O P Q R S T U V Z)"
                         f", separadas por comas. Cada palabra tiene que tener al menos una definción en la RAE.")

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        # Obtiene las palabras generadas
        palabras = response.choices[0].message.content

        # Las limpia y las separa por comas
        palabras = palabras.replace(".", "")
        palabras = palabras.split(", ")

        return palabras