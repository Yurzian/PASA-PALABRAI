from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re


def obtener_definiciones_rae(palabra):
    """
        Obtiene las definiciones de una palabra desde el DLE de la RAE.
        Sacada de un ejercicio otorgado por el profesor Miguel Ángel.

        Parameters:
        - palabra (str): La palabra para la cual se buscarán las definiciones.

        Returns:
        - list: Una lista de hasta tres definiciones de la palabra, procesadas y limpias.
        """
    try:
        # Esquema de la URL
        esquema = "https://"
        # Servidor donde se encuentra el DLE de la RAE
        servidor = "dle.rae.es/"
        # Recurso: la palabra consultada, codificada apropiadamente para URL
        recurso = urllib.parse.quote(palabra, safe='')

        # Construir la dirección URL completa
        direccion = esquema + servidor + recurso

        # Variable para almacenar la respuesta del servidor
        respuesta = ""
        # Encabezados HTTP para la solicitud
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Crear una solicitud URL con los encabezados definidos
        req = urllib.request.Request(direccion, headers=headers)

        # Realizar la solicitud HTTP
        with urllib.request.urlopen(req) as url:
            # Obtener el código de estado de la respuesta
            estado = url.getcode()

            # Verificar si la respuesta fue exitosa (código de estado 200)
            if estado == 200:
                # Leer y decodificar la respuesta en formato UTF-8
                respuesta = url.read().decode('utf-8')
            else:
                # Si el código de estado no es 200, lanzar una excepción con un mensaje de error
                raise Exception("Error HTTP " + str(estado))

        # Crear un objeto BeautifulSoup para analizar el HTML de la respuesta
        soup = BeautifulSoup(respuesta, 'html.parser')
        # Encontrar todas las etiquetas <p> con la clase 'j' que contienen definiciones
        definitions = soup.find_all('p', class_='j')

        result_definitions = []
        patrones = (
            r'<.*?>', r'Sin\.:[^\.]*\.?', r'Ant\.:[^\.]*\.?', r'\d+\.', r'adj\. ', r'm\. ', r'f\. ', r'm\. y f\.',
            r'poét\. ', r'coloq\. ', r' Der\. ', r' U\. t\. c\. adj\.', r'loc\. ', r'locs\. ', r'verbs\. ', r'‖ ',
            r'Alq\. ', r'Apl\. ', r', u\. ', r'.u\. ', r'U\.', r't\. ', r'c\. ', r's\. ', r'Astrol\. ', r'Ec\. ',
            r'Med\. ', r'Psicol\. ', r'a pers\.', r'Ret ', r'tr\. ', r'\bt\b', r'\ba p\b', r' prnl\.', r'Mar\. ',
            r'Dep\. ', r' s\.')

        for i, definition in enumerate(definitions[:3]):
            def_text = definition.get_text()
            for patron in patrones:
                def_text = re.sub(patron, '', def_text)
            def_text = def_text.strip()  # Eliminar espacios en blanco al inicio y al final
            result_definitions.append(def_text)

        return result_definitions

    except Exception as e:
        # Imprimir el mensaje de la excepción
        print(e)
        # Devolver una lista vacía en caso de error
        return []


