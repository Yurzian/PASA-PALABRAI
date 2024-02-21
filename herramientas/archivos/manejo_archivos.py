# Librería para poder modificar archivos json
import json

def buscar_diccionario_por_nombre(nombre):
    """
    Busca un diccionario por su nombre en un archivo JSON.

    Parameters:
    - nombre (str): El nombre del diccionario a buscar.

    Returns:
    - dict or None: El diccionario encontrado o None si no se encuentra.
    """
    with open('recursos/json/opciones.json', 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)
        for item in data:
            if item['nombre'] == nombre:
                return item['diccionario']
    return None

def agregar_datos_a_json(palabras, definiciones, tema, dificultad):
    """
        Agrega datos a un archivo JSON.

        Parameters:
        - palabras (list): Lista de palabras.
        - definiciones (list): Lista de definiciones correspondientes a las palabras.
        - tema (str): El tema asociado a las palabras y definiciones.
        - dificultad (str): La dificultad asociada a las palabras y definiciones.
        """
    try:
        with open("recursos/json/palabras.json", 'r') as file:
            # Lee el contenido del archivo JSON
            lista_datos = json.load(file)
    except FileNotFoundError:
        # Si el archivo no existe, crea una lista vacía
        lista_datos = []

    diccionario = {}
    for palabra, definicion in zip(palabras, definiciones):
        diccionario[palabra] = definicion

    datos = {
        "dificultad": dificultad,
        "tema": tema,
        "diccionario": list(diccionario.items())
    }

    # Agrega los nuevos datos a la lista existente
    lista_datos.append(datos)

    # Escribe los datos actualizados al archivo JSON
    with open("recursos/json/palabras.json", 'w') as file:
        json.dump(lista_datos, file, indent=4)


def agregar_partida_a_json(nombre_usuario, aciertos):
    """
       Agrega información de una partida a un archivo JSON.

       Parameters:
       - nombre_usuario (str): El nombre del usuario que jugó la partida.
       - aciertos (int): La cantidad de aciertos en la partida.
       """
    nombre_archivo = 'recursos/json/datos_usuario.json'
    try:
        with open(nombre_archivo, 'r') as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        # Si el archivo no existe, se crea y se añade la primera partida
        datos = {"usuarios": []}

    encontrado = False
    # Comprobar si el usuario ya existe en el archivo JSON
    for usuario in datos['usuarios']:
        if usuario['Nombre'] == nombre_usuario:
            usuario['Partidas jugadas'] += 1
            usuario['Aciertos'] += aciertos
            encontrado = True
            break

    # Si el usuario no se encuentra, se añade a la lista de usuarios
    if not encontrado:
        datos['usuarios'].append({
            "Nombre": nombre_usuario,
            "Partidas jugadas": 1,
            "Aciertos": aciertos
        })

    # Guardar los datos actualizados en el archivo JSON
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos, archivo, indent=4)
