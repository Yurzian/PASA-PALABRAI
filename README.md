# PASA-PALABRAI


# Descripción

Este proyecto es una aplicación que usa distintos tipos de IA para hacer un juego parecido al programa Pasapalabra.

# Archivos
- ClienteOpenAI.py: se utiliza para interactuar con la API de OpenAI para la generación de palabras aleatorias.
- ReconocerVoz.py: implementa la funcionalidad de reconocimiento de voz de speech recognition utilizando el micrófono como fuente de entrada de audio.
- TextoAVoz.py: proporciona métodos para convertir texto a voz utilizando el motor pyttsx3.
- JuegoPygame.py: se utiliza Pygame para hacer un diseño de juego para la aplicación.
- Tablero.py: objeto tablero para usado en el juego, el cual tiene palabras y definiciones.
- manejo_archivos.py: contiene funciones para leer y modificar archivos JSON.
- obtener_definiciones.py: hace web scraping a la página de la RAE y devuelve definiciones de una palabra dada.
- credenciales.py: archivo con la clave de OpenAI.
- main.py: fichero que hay que ejecutar para poder jugar.

# Cómo usasr la aplicación
1. Tener una key de OpenAI.
2. Meter la key en openai_key = "" del archivo credenciales.py.
3. Instalar las siguientes librerías:
   - pip install pygame
   - pip install openai
   - pip install SpeechRecognition
   - pip install pyttsx3
   - pip install beautifulsoup4

# Autor
Daniel García Pérez
