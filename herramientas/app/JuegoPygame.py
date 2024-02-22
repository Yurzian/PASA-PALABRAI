# Mis librerías con tablero, api de texto a voz, api de voz a texto y manejo de archivos
from herramientas.app.Tablero import Tablero
from herramientas.IA.TextoAVoz import TextoAVoz
from herramientas.IA.ReconocerVoz import ReconocerVoz
from herramientas.archivos.manejo_archivos import agregar_partida_a_json
#Librería de la aplicación pygame
import pygame
from pygame.locals import *
#Librería para calcular el ángulo y radio del rosco
import math


class JuegoPygame:
    def __init__(self):
        """
                Constructor de la clase JyegoPygame.

                Inicializa los valores necesarios para correr una aplicación en pygame
                """
        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()

        # Inicializar el tablero de juego y las api para pasar texto a audio y reconocer voz
        self.tablero = Tablero()
        self.textoAVoz = TextoAVoz()
        self.reconocerVoz = ReconocerVoz()
        self.jugador = ""

        # Configuración de Pygame
        infoObject = pygame.display.Info()
        pygame.display.set_caption('Pasa-PalabrAI')  # Nombre de la pestaña
        self.ANCHO, self.ALTO = infoObject.current_w, infoObject.current_h  # Tamaño de la pantalla
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO), pygame.FULLSCREEN)  # Tamaño de la pantalla
        self.fuente = pygame.font.SysFont(None, 50)  # Fuente de los textos
        self.fondo = pygame.image.load('recursos/imágenes/fondo.gif')  # Imágen de fondo
        self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))  # Imágen de fondo
        self.reloj = pygame.time.Clock()

    def reproducir_audio(self, texto):
        """
                Reproduce el audio correspondiente al texto pasado como argumento.

                Parameters:
                texto (str): El texto que se convertirá a audio y se reproducirá.

                Returns:
                bool: False para el bucle de seguir jugando
                """
        # Utilizo la funcion para generar el audio con al definición de la palabra actual
        self.textoAVoz.convertir_texto(texto)
        # Vuelvo a coger el audio, ahora cambiado
        definicion = pygame.mixer.Sound("recursos/audio/definicion.wav")
        # Reproduzco en al aplicación el sonido
        definicion.play()
        return False

    def dibujar_rosco(self):
        """
           Dibuja el rosco de palabras en la pantalla del juego.
           Hecho con ayuda de ChatGPT.
           """
        # Obtengo el centro de x e y de la pantalla
        center_x, center_y = self.ANCHO // 2, self.ALTO // 2

        # Obtengo el número de letras que tendrá el rosco
        num_letras = len(self.tablero.palabras)

        # Calculo el primer ángulo
        primer_angulo = -math.pi / 2

        # Obtengo el ángulo que hay entre cada letra del rosco
        incremento_angulo = 2 * math.pi / num_letras

        # Obtengo todos los estados para saber el color
        estados = self.tablero.estado_palabras

        # Por cada letra del tablero
        for i in range(len(self.tablero.palabras)):
            # Calculo el ángulo
            angle = primer_angulo + i * incremento_angulo

            # Calculo las coordenadas en las que se dibujará la letra
            x = center_x + int(300 * math.cos(angle))
            y = center_y + int(300 * math.sin(angle))

            # Compruebo si la palabra está acertada
            if estados[i] is True:
                color = (0, 255, 0)  # Verde
            # Compruebo si la palabra está fallada
            elif estados[i] is False:
                color = (255, 0, 0)  # Rojo
            else:
                color = (0, 0, 0)  # Blanco

            # Compruebo si la palabra es la actual
            if i == self.tablero.indice_palabras:
                color = (0, 0, 255)  # Azul

            # Dibujar la letra en la pantalla
            self.escribir_texto_centrado(self.tablero.palabras[i][0].upper(), self.fuente, color, self.pantalla, x, y)

    def escribir_texto_centrado(self, text, font, color, surface, x, y):
        """
                Escribe texto centrado en una posición específica en la superficie especificada.

                Parameters:
                text (str): El texto que se escribirá.
                font (pygame.font.Font): La fuente que se utilizará para escribir el texto.
                color ((int, int, int)): El color del texto en formato RGB.
                surface (pygame.Surface): La superficie en la que se escribirá el texto.
                x (int): La coordenada x del centro del texto.
                y (int): La coordenada y del centro del texto.
                """
        # Renderizo el texto con la fuente y color pasados
        text_surface = font.render(text, True, color)
        # Obtengo el rectángulo del área que va a ocupar el texto y calculo el centro
        text_rect = text_surface.get_rect(center=(x, y))
        # Escribo el texto
        surface.blit(text_surface, text_rect)

    def ajustar_texto(self, texto, fuente, ancho_maximo):
        """
                Ajusta el texto para que quepa dentro de un ancho máximo dado.
                Hecho con ayuda de ChatGPT

                Parameters:
                texto (str): El texto que se ajustará.
                fuente (pygame.font.Font): La fuente utilizada para renderizar el texto.
                ancho_maximo (int): El ancho máximo permitido para el texto.

                Returns:
                list: Una lista de líneas de texto ajustadas.
                """
        # Dividir el texto en palabras
        palabras = texto.split(' ')
        # Inicializar una lista para almacenar las líneas envueltas
        lineas = []
        # Inicializar una cadena para la línea actual
        linea_actual = ''

        # Iterar sobre cada palabra en el texto
        for palabra in palabras:
            # Añado la palabra a la línea
            linea_texto = linea_actual + ' ' + palabra if linea_actual != '' else palabra
            # Si la línea no se pasa del ancho
            if fuente.size(linea_texto)[0] < ancho_maximo:
                # Actualizo la línea
                linea_actual = linea_texto
            # Si la linea se pasa del ancho
            else:
                lineas.append(linea_actual)
                # Establecer la palabra actual como la nueva línea actual
                linea_actual = palabra

        # Agregar la última línea (o la única línea si solo hay una) a la lista de líneas
        lineas.append(linea_actual)
        # Devolver la lista de líneas envueltas
        return lineas

    def pantalla_formulario(self):
        """
                Funcion para mostrar un formulario para que el jugador pueda ingresar su nombre, el tema y la dificultad,
                o elegir entre varias opciones ya creadas.
                Diseño hecho con ayuda de ChatGPT.
                """
        # Definir las posiciones de los botones
        input_nombre = pygame.Rect(self.ANCHO * 0.1, self.ALTO * 0.1, self.ANCHO * 0.2, self.ALTO * 0.05)
        input_tema = pygame.Rect(self.ANCHO * 0.1, self.ALTO * 0.2, self.ANCHO * 0.2, self.ALTO * 0.05)
        boton_facil = pygame.Rect(self.ANCHO * 0.1, self.ALTO * 0.3, self.ANCHO * 0.1, self.ALTO * 0.05)
        boton_medio = pygame.Rect(self.ANCHO * 0.2, self.ALTO * 0.3, self.ANCHO * 0.1, self.ALTO * 0.05)
        boton_dificil = pygame.Rect(self.ANCHO * 0.3, self.ALTO * 0.3, self.ANCHO * 0.1, self.ALTO * 0.05)
        boton_avanzar = pygame.Rect(self.ANCHO * 0.1, self.ALTO * 0.4, self.ANCHO * 0.1, self.ALTO * 0.05)
        boton_opcion = pygame.Rect(self.ANCHO * 0.1, self.ALTO * 0.6, self.ANCHO * 0.2, self.ALTO * 0.05)

        # Inicializo los valores de los input, de los botones y del bucle
        texto_nombre = ''
        texto_tema = ''
        dificultad = ''
        input_activo = None
        ejecutando = True

        while ejecutando:
            # Compruebo el evento
            for event in pygame.event.get():
                # Si se cierra la ventana
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Si se hace clic, comprobar dónde se ha hecho
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si es en el input del nombre
                    if input_nombre.collidepoint(event.pos):
                        # Pongo ese input como activo para poder escribir
                        input_activo = input_nombre
                    # Si es en el input del tema
                    elif input_tema.collidepoint(event.pos):
                        # Pongo ese input como activo para poder escribir
                        input_activo = input_tema
                    # Si es en alguno de los botones de dificultad, cambio el valor al clicado
                    elif boton_facil.collidepoint(event.pos):
                        dificultad = "facil"
                    elif boton_medio.collidepoint(event.pos):
                        dificultad = "media"
                    elif boton_dificil.collidepoint(event.pos):
                        dificultad = "dificil"
                    # Si hago click en avanzar, genero el tablero con los valores que hayamos introducido
                    elif boton_avanzar.collidepoint(event.pos):
                        self.tablero.generar_tablero(dificultad=dificultad, tema=texto_tema)
                        self.jugador = texto_nombre
                        ejecutando = False  # Salir del bucle
                    # Si hago click en el botón de opciones
                    elif boton_opcion.collidepoint(event.pos):
                        self.pantalla_opciones()  # Me voy a la pantalla de las opciones
                        ejecutando = False
                # Si se pulsa una tecla
                if event.type == KEYDOWN:
                    # Si es el escape
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        quit()
                    # Compruebo que input está activo
                    if input_activo == input_nombre:
                        if event.key == pygame.K_BACKSPACE:
                            texto_nombre = texto_nombre[:-1]  # Quito una letra al input
                        else:
                            texto_nombre += event.unicode  # Añado la letra al input
                    elif input_activo == input_tema:
                        if event.key == pygame.K_BACKSPACE:
                            texto_tema = texto_tema[:-1]  # Quito una letra al input
                        else:
                            texto_tema += event.unicode  # Añado la letra al input

            self.pantalla.fill((30, 30, 30))

            # Dibujo el rectángulo y el contenido del input Nombre
            txt_surface = self.fuente.render('Nombre: ' + texto_nombre, True, (255, 255, 255))
            self.pantalla.blit(txt_surface, (input_nombre.x, input_nombre.y + 10))
            pygame.draw.rect(self.pantalla, pygame.Color('lightskyblue3'), input_nombre, 2)

            # Dibujo el rectángulo y el contenido del input Tema
            txt_surface = self.fuente.render('Tema: ' + texto_tema, True, (255, 255, 255))
            self.pantalla.blit(txt_surface, (input_tema.x, input_tema.y + 10))
            pygame.draw.rect(self.pantalla, pygame.Color('lightskyblue3'), input_tema, 2)

            # Dibujo el rectangulo de los botones
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton_facil)
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton_medio)
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton_dificil)
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton_avanzar)
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton_opcion)

            # Escribo el texto de los botones
            txt_boton = self.fuente.render('Fácil', True, (0, 0, 0))
            self.pantalla.blit(txt_boton, (boton_facil.x + (boton_facil.width - txt_boton.get_width()) // 2, boton_facil.y + 5))
            txt_boton = self.fuente.render('Medio', True, (0, 0, 0))
            self.pantalla.blit(txt_boton, (boton_medio.x + (boton_medio.width - txt_boton.get_width()) // 2, boton_medio.y + 5))
            txt_boton = self.fuente.render('Difícil', True, (0, 0, 0))
            self.pantalla.blit(txt_boton,
                          (boton_dificil.x + (boton_dificil.width - txt_boton.get_width()) // 2, boton_dificil.y + 5))
            txt_boton = self.fuente.render('Avanzar', True, (0, 0, 0))
            self.pantalla.blit(txt_boton,
                          (boton_avanzar.x + (boton_avanzar.width - txt_boton.get_width()) // 2, boton_avanzar.y + 5))
            txt_boton = self.fuente.render('Opciones', True, (0, 0, 0))
            self.pantalla.blit(txt_boton,
                          (boton_opcion.x + (boton_opcion.width - txt_boton.get_width()) // 2, boton_opcion.y + 5))

            pygame.display.flip()

        self.pantalla_juego()

    def pantalla_opciones(self):
        """
            Función para mostrar la pantalla de opciones y permitir al jugador elegir un tema para jugar.

            Se muestran una serie de botones con diferentes temas. Al hacer clic en uno de los botones,
            se genera un tablero con palabras asociadas al tema elegido y se muestra la pantalla de juego.
            Diseño hecho con ayuda de ChatGPT.

            """
        # Definir las posiciones de los botones
        boton1 = pygame.Rect(self.ANCHO * 0.1, self.ALTO * 0.1, self.ANCHO * 0.2, self.ALTO * 0.1)
        boton2 = pygame.Rect(self.ANCHO * 0.1, self.ALTO * 0.3, self.ANCHO * 0.2, self.ALTO * 0.1)
        boton3 = pygame.Rect(self.ANCHO * 0.1, self.ALTO * 0.5, self.ANCHO * 0.2, self.ALTO * 0.1)
        boton4 = pygame.Rect(self.ANCHO * 0.5, self.ALTO * 0.1, self.ANCHO * 0.2, self.ALTO * 0.1)
        boton5 = pygame.Rect(self.ANCHO * 0.5, self.ALTO * 0.3, self.ANCHO * 0.2, self.ALTO * 0.1)
        boton6 = pygame.Rect(self.ANCHO * 0.5, self.ALTO * 0.5, self.ANCHO * 0.2, self.ALTO * 0.1)

        # Inicializo la variable para el bucle
        ejecutando = True

        while ejecutando:
            # Compruebo el evento
            for event in pygame.event.get():
                # Si cierro la ventana
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Si presiono una tecla
                if event.type == KEYDOWN:
                    # Si es el escape
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        quit()
                # Si hago click, comprobar donde se hace el click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Compruebo en qué botón se hace click, y en función de botón, se genera el tablero con
                    # el diccionario ya creado del tema que hayamos elegido
                    if boton1.collidepoint(event.pos):
                        self.tablero.obtener_tablero(nombre="futbol")
                        ejecutando = False
                    elif boton2.collidepoint(event.pos):
                        self.tablero.obtener_tablero(nombre="cine")
                        ejecutando = False
                    elif boton3.collidepoint(event.pos):
                        self.tablero.obtener_tablero(nombre="animales")
                        ejecutando = False
                    elif boton4.collidepoint(event.pos):
                        self.tablero.obtener_tablero(nombre="facil")
                        ejecutando = False
                    elif boton5.collidepoint(event.pos):
                        self.tablero.obtener_tablero(nombre="medio")
                        ejecutando = False
                    elif boton6.collidepoint(event.pos):
                        self.tablero.obtener_tablero(nombre="dificil")
                        ejecutando = False

            self.pantalla.fill((30, 30, 30))

            # Dibujar botones
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton1)
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton2)
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton3)
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton4)
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton5)
            pygame.draw.rect(self.pantalla, pygame.Color('grey'), boton6)

            # Escribir texto de los botones
            txt_boton1 = self.fuente.render('Fútbol', True, (0, 0, 0))
            self.pantalla.blit(txt_boton1, (boton1.x + (boton1.width - txt_boton1.get_width()) // 2, boton1.y + (boton1.height - txt_boton1.get_height()) // 2))
            txt_boton2 = self.fuente.render('Cine', True, (0, 0, 0))
            self.pantalla.blit(txt_boton2, (boton2.x + (boton2.width - txt_boton2.get_width()) // 2, boton2.y + (boton2.height - txt_boton2.get_height()) // 2))
            txt_boton3 = self.fuente.render('Animales', True, (0, 0, 0))
            self.pantalla.blit(txt_boton3, (boton3.x + (boton3.width - txt_boton3.get_width()) // 2, boton3.y + (boton3.height - txt_boton3.get_height()) // 2))
            txt_boton4 = self.fuente.render('Fácil', True, (0, 0, 0))
            self.pantalla.blit(txt_boton4, (boton4.x + (boton4.width - txt_boton4.get_width()) // 2, boton4.y + (boton4.height - txt_boton4.get_height()) // 2))
            txt_boton5 = self.fuente.render('Medio', True, (0, 0, 0))
            self.pantalla.blit(txt_boton5, (boton5.x + (boton5.width - txt_boton5.get_width()) // 2, boton5.y + (boton5.height - txt_boton5.get_height()) // 2))
            txt_boton6 = self.fuente.render('Difícil', True, (0, 0, 0))
            self.pantalla.blit(txt_boton6, (boton6.x + (boton6.width - txt_boton6.get_width()) // 2, boton6.y + (boton6.height - txt_boton6.get_height()) // 2))

            pygame.display.flip()

        self.pantalla_juego()

    def pantalla_juego(self):
        """
            Función para mostrar la pantalla de juego y permitir al jugador interactuar con él.
            Diseño hecho con ayuda de ChatGPT.

            """
        # Definir las posiciones de los botones
        boton_definicion = pygame.Rect(0, 0, self.ANCHO, 140)
        boton_siguiente_definicion = pygame.Rect(0, self.ALTO - 100, self.ANCHO // 3, 100)
        boton_microfono = pygame.Rect(self.ANCHO // 3, self.ALTO - 100, self.ANCHO // 3, 100)
        boton_pasapalabra = pygame.Rect(2 * self.ANCHO // 3, self.ALTO - 100, self.ANCHO // 3, 100)
        boton_input = pygame.Rect(0, self.ALTO - 2 * 100, self.ANCHO, 100)

        # Inicializo las variables para el input, el audio y el bucle
        texto_ingresado = ""
        seguir_audio = True
        ejecutando = True

        while self.tablero.seguir_jugando() and ejecutando:
            # Comprueba el evento
            for event in pygame.event.get():
                # Si se cierra el juego
                if event.type == QUIT:
                    ejecutando = False
                    pygame.quit()
                    quit()
                # Si se presiona una tecla
                elif event.type == KEYDOWN:
                    # Tecla ESCAPE presionada
                    if event.key == K_ESCAPE:
                        ejecutando = False
                        pygame.quit()
                        quit()
                    # Tecla ENTER presionada
                    elif event.key == K_RETURN:
                        # Reinicio el audio
                        pygame.mixer.stop()
                        seguir_audio = True
                        # Compruebo si es la palabra a adivinar
                        correcto, palabra_comparada = self.tablero.comprobar_palabra(texto_ingresado)
                        if correcto:
                            self.reproducir_audio("¡Correcto!")
                        else:
                            self.reproducir_audio(f"¡Incorrecto! La palabra era, {palabra_comparada}")
                        seguir_audio = True
                        texto_ingresado = ""

                        # Esperar hasta que se termine de reproducir el audio
                        while pygame.mixer.get_busy():
                            pygame.time.wait(40)
                    # Tecla ATRAS presionada
                    elif event.key == K_BACKSPACE:
                        texto_ingresado = texto_ingresado[:-1]  # Quito una letra al input
                    # Cualquiero otra tecla, se añade al input
                    else:
                        texto_ingresado += event.unicode
                # Si se hace click, comprobamos donde se ha hecho el click
                elif event.type == MOUSEBUTTONDOWN:
                    # Si se ha hecho click en el botón de siguiente
                    if boton_siguiente_definicion.collidepoint(event.pos):
                        # Reiniciar el audio
                        pygame.mixer.stop()
                        seguir_audio = True
                        # Compruebo si hay más definiciones
                        if not self.tablero.siguiente_definicion():
                            # Si no hay más definiciones, el audio avisa
                            seguir_audio = self.reproducir_audio("No tengo más definiciones")
                    # Si se ha hecho click en el botón del micrófono
                    elif boton_microfono.collidepoint(event.pos):
                        pygame.draw.rect(self.pantalla, (57, 180, 250), boton_microfono)
                        pygame.display.flip()  # Actualiza la pantalla
                        pygame.mixer.stop()
                        # Utilizo el reconocimiento de voz
                        voz = self.reconocerVoz.reconocer_voz()
                        # Si se reconoce pasapalabra
                        if voz == "pasapalabra":
                            self.tablero.siguiente_palabra()
                            texto_ingresado = ""
                            pygame.mixer.stop()
                            seguir_audio = True
                        # Si se reconoce siguiente definición
                        elif voz == "siguiente definición":
                            # Reiniciar el audio
                            pygame.mixer.stop()
                            seguir_audio = True
                            # Compruebo si hay más definiciones
                            if not self.tablero.siguiente_definicion():
                                # Si no hay más definiciones, el audio avisa
                                seguir_audio = self.reproducir_audio("No tengo más definiciones")
                        else:
                            texto_ingresado = voz
                    # Si se ha hecho click en el botón de pasapalabra
                    elif boton_pasapalabra.collidepoint(event.pos):
                        # Pasar a la siguiente palabra del tablero
                        self.tablero.siguiente_palabra()
                        # Borro el texto del input
                        texto_ingresado = ""
                        # Reinicio el audio
                        pygame.mixer.stop()
                        seguir_audio = True

            # Dibujar la imagen de fondo
            self.pantalla.blit(self.fondo, (0, 0))

            # Dibujar el rosco con las letras
            self.dibujar_rosco()

            # Dibujar zona y los bordes de todos los botones
            for rect in [boton_definicion, boton_siguiente_definicion, boton_microfono, boton_pasapalabra, boton_input]:
                pygame.draw.rect(self.pantalla, (255, 255, 255), rect)  # Luego rellenar con blanco
                pygame.draw.rect(self.pantalla, (0, 0, 0), rect, 2)  # Dibujar el borde negro primero

            # Escribir el texto que se va escribiendo en el botón del input
            texto_ingresado_render = self.fuente.render(texto_ingresado, True, (0, 0, 0))
            text_rect = texto_ingresado_render.get_rect(center=boton_input.center)
            self.pantalla.blit(texto_ingresado_render, text_rect)

            # Obtengo la definición para poder ponerla en su botón
            definicion_text = self.tablero.definicion_actual()
            # Separar la definicion en líneas para que pueda estar dentro del ancho del botón
            definicion_lines = self.ajustar_texto(definicion_text, self.fuente, boton_definicion.width - 10)
            # Inicializo la posición vertical, que es la del botón y un poco más abajo
            y_pos = boton_definicion.y + 5
            # Por cada línea de definición
            for line in definicion_lines:
                # Escribo esa línea de la definición
                definicion_render = self.fuente.render(line, True, (0, 0, 0))
                self.pantalla.blit(definicion_render, (boton_definicion.x + 5, y_pos))
                # Modifico la posición vertical, para que la siguiente línea se escriba más abajo
                y_pos += self.fuente.get_height()

            # Dibujo el texto de los botones de abajo
            self.escribir_texto_centrado("Siguiente Definición", self.fuente, (0, 0, 0), self.pantalla, boton_siguiente_definicion.centerx, boton_siguiente_definicion.centery)
            self.escribir_texto_centrado("Micrófono", self.fuente, (0, 0, 0), self.pantalla, boton_microfono.centerx, boton_microfono.centery)
            self.escribir_texto_centrado("Pasapalabra", self.fuente, (0, 0, 0), self.pantalla, boton_pasapalabra.centerx, boton_pasapalabra.centery)

            # Comprobar si se puede reproducir el audio
            if seguir_audio:
                seguir_audio = self.reproducir_audio(f'Con la {self.tablero.palabras[self.tablero.indice_palabras][0]}'
                                                     f' . .{definicion_text}')

            pygame.display.flip()

            self.reloj.tick(30)

        pygame.mixer.stop()

        if not self.tablero.seguir_jugando():
         self.pantalla_final()

    def pantalla_final(self):
        """
            Función para mostrar la pantalla final del juego, mostrando el puntaje obtenido por el jugador.

            Si el jugador ha ingresado su nombre, se agrega la partida al registro de partidas.
            Diseño hecho con ayuda de ChatGPT.

            """
        # Inicializo la variable para el bucle y añado la partida al json si se ha ingresado el nombre
        if self.jugador != "":
            agregar_partida_a_json(nombre_usuario=self.jugador, aciertos=self.tablero.estado_palabras.count(True))
        ejecutando = True

        while ejecutando:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        quit()
                if event.type == MOUSEBUTTONDOWN:
                    pygame.quit()
                    quit()

            self.pantalla.fill((255, 255, 255))

            # Mostrar texto FIN
            fin_texto = self.fuente.render('FIN', True, (0, 0, 0))
            fin_rect = fin_texto.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 50))
            self.pantalla.blit(fin_texto, fin_rect)

            # Mostrar texto con los aciertos
            aciertos_texto = self.fuente.render(f'Aciertos: {self.tablero.estado_palabras.count(True)}', True, (0, 0, 0))
            aciertos_rect = aciertos_texto.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 + 50))
            self.pantalla.blit(aciertos_texto, aciertos_rect)

            # Mostrar texto con los errores
            errores_texto = self.fuente.render(f'Errores: {self.tablero.estado_palabras.count(False)}', True, (0, 0, 0))
            errores_rect = errores_texto.get_rect(center=(self.ANCHO // 2, self.ALTO // 2))
            self.pantalla.blit(errores_texto, errores_rect)

            # Dibujar el botón de salir
            pygame.draw.rect(self.pantalla, (0, 0, 0), (self.ANCHO // 2 - 100, self.ALTO // 2 + 100, 200, 50))
            salir_texto = self.fuente.render('Salir', True, (255, 255, 255))
            boton_salir = salir_texto.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 + 125))
            self.pantalla.blit(salir_texto, boton_salir)

            pygame.display.flip()
