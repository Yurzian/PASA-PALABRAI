# Mis librerías para la api de openai, para obtener definiciones de la rae y modificar archivos json
from ..IA.ClienteOpenAI import ClienteOpenAI
from ..web.obtener_definiciones import obtener_definiciones_rae
from ..archivos.manejo_archivos import buscar_diccionario_por_nombre, agregar_datos_a_json


class Tablero:
    def __init__(self):
        """
                Constructor de la clase Tablero.

                Inicializa las listas para almacenar palabras, definiciones y estados de las palabras.
                """
        self.palabras = []
        self.definiciones = []
        self.estado_palabras = []
        self.indice_palabras = 0
        self.indice_definiciones = 0

    def generar_tablero(self, dificultad="", tema=""):
        """
                Función para generar el tablero del juego con palabras y definiciones.

                Parameters:
                - dificultad (str): La dificultad de las palabras a generar.
                - tema (str): El tema de las palabras a generar.
                """
        openai_API = ClienteOpenAI()

        palabras = openai_API.generar_lista_palabras(dificultad=dificultad, tema=tema)

        for palabra in palabras:
            definiciones = obtener_definiciones_rae(palabra)
            if len(definiciones) > 0:
                self.palabras.append(palabra)
                self.definiciones.append(definiciones)
                self.estado_palabras.append(None)

        agregar_datos_a_json(palabras=self.palabras, definiciones=self.definiciones, tema=tema, dificultad=dificultad)

    def obtener_tablero(self, nombre=""):
        """
                Función para obtener un tablero previamente creado según el nombre proporcionado.

                Parameters:
                - nombre (str): El nombre del tablero a obtener.
                """
        palabras_definiciones = buscar_diccionario_por_nombre(nombre)
        for palabra, definicion in palabras_definiciones:
            self.palabras.append(palabra)
            self.definiciones.append(definicion)
            self.estado_palabras.append(None)

    def seguir_jugando(self, seguir=True):
        """
                Verifica si el juego debe continuar.

                Si hay palabras sin adivinar y el jugador desea seguir, retorna True.

                Parameters:
                - seguir (bool): Indica si el jugador desea seguir jugando.

                Returns:
                - bool: True si hay palabras sin adivinar y el jugador desea seguir, False en caso contrario.
                """
        return None in self.estado_palabras and seguir

    def comprobar_palabra(self, palabra):
        """
                Comprueba si la palabra proporcionada coincide con la palabra actual del tablero.

                Si la palabra es correcta, actualiza el estado de la palabra y avanza al siguiente si es necesario.
                Si la palabra es incorrecta, actualiza el estado de la palabra y avanza al siguiente si es necesario.

                Parameters:
                - palabra (str): La palabra proporcionada por el jugador.

                Returns:
                - tuple: Una tupla que contiene un booleano que indica si la palabra es correcta y la palabra actual del tablero.
                """
        palabra_a_comprobar = self.palabra_actual().lower()
        if palabra.lower() == palabra_a_comprobar:
            self.estado_palabras[self.indice_palabras] = True
            if self.seguir_jugando():
                self.siguiente_palabra()
            return True, palabra_a_comprobar
        else:
            self.estado_palabras[self.indice_palabras] = False
            if self.seguir_jugando():
                self.siguiente_palabra()
            return False, palabra_a_comprobar

    def siguiente_palabra(self):
        """
                Avanza al siguiente índice de palabra que aún no ha sido adivinada.

                Calcula el siguiente índice y lo asigna como índice de la palabra actual.
                """
        # Reinicio el índice de las definiciones para mostrar la primera definición de la siguiente palabra
        self.indice_definiciones = 0
        # Calculo el siguiente índice
        siguiente_indice = self.indice_palabras + 1
        # Sigo sumando hasta encontrar una palabra que su estado esté en None
        while self.estado_palabras[siguiente_indice % len(self.estado_palabras)] is not None:
            siguiente_indice += 1
        # Actualizo el índice de la palabra actual
        self.indice_palabras = siguiente_indice % len(self.estado_palabras)

    def siguiente_definicion(self):
        """
               Avanza a la siguiente definición de la palabra actual si hay más de una definición disponible.

               Returns:
               - bool: True si se ha avanzado a la siguiente definición, False si no hay más definiciones.
               """
        if len(self.definiciones[self.indice_palabras]) == 1:
            return False

        if self.indice_definiciones + 1 >= len(self.definiciones[self.indice_palabras]):
            self.indice_definiciones = 0
        else:
            self.indice_definiciones += 1

        return True

    def palabra_actual(self):
        """
                Devuelve la palabra actual del tablero.

                Returns:
                - str: La palabra actual del tablero.
                """
        return self.palabras[self.indice_palabras]

    def definicion_actual(self):
        """
                Devuelve la definición actual de la palabra actual del tablero.

                Returns:
                - str: La definición actual de la palabra actual del tablero.
                """
        return self.definiciones[self.indice_palabras][self.indice_definiciones]

    def todos_estados(self):
        """
                Devuelve el estado actual de todas las palabras en el tablero.

                Returns:
                - list: Una lista que contiene los estados actuales de todas las palabras en el tablero.
                """
        return self.estado_palabras