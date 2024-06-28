import pygame
import copy
import json

# Colores básicos
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Otros colores
AMARILLO = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

AZUL_FONDO = (47, 116, 181)

# Colores grises
GRIS_CLARO = (200, 200, 200)
GRIS_MEDIO = (150, 150, 150)
GRIS_OSCURO = (100, 100, 100)

# Colores adicionales
AZUL_CLARO = (135, 206, 250)
VERDE_CLARO = (144, 238, 144)
VERDE_OSCURO = (0, 100, 0)
ROSA = (255, 192, 203)
NARANJA = (255, 165, 0)
VIOLETA = (238, 130, 238)
CREMITA = (255, 253, 208)


colores_niveles = [
    (NARANJA, 300, 332),
    (VERDE_CLARO, 400, 332),
    (AMARILLO, 500, 332),
    (AZUL_CLARO, 600, 332),
    (ROJO, 700, 332),
    (VIOLETA, 800, 332, "Avanza 1"),
    (CREMITA, 900, 332),
    (VERDE, 1000, 332),
    (VIOLETA, 800, 432, ""),
    (AZUL_CLARO, 600, 432, "Retrocede 1")
]

# Nombre del archivo JSON para guardar los puntajes
archivo_puntajes = "puntajes.json"

# def procesar_preguntas(lista:list) -> list:
#     lista_preguntas = []  # Lista para almacenar las sub-listas de preguntas
#     lista_opciones = []  # Lista para almacenar las sub-listas de opciones
#     lista_temas = []  # Lista para almacenar las sub-listas de temas
#     lista_respuestas = []  # Lista para almacenar las sub-listas de respuestas correctas

#     for pregunta in lista:  # Recorremos la lista principal
#         pregunta_dict = {}  # Diccionario para almacenar la pregunta actual
#         opciones_dict = {}  # Diccionario para almacenar las opciones actuales
#         tema_dict = {}  # Diccionario para almacenar el tema actual
#         respuesta = None  # Variable para almacenar la respuesta correcta

#         # Extracción de información del diccionario
#         pregunta_dict["pregunta"] = pregunta.get("pregunta")  # Obtenemos la pregunta
#         opciones_dict["a"] = pregunta.get("a")  # Obtenemos la opción a
#         opciones_dict["b"] = pregunta.get("b")  # Obtenemos la opción b
#         opciones_dict["c"] = pregunta.get("c")  # Obtenemos la opción c
#         tema_dict["tema"] = pregunta.get("tema")  # Obtenemos el tema
#         respuesta = pregunta.get(pregunta.get("correcta"))  # Obtenemos la respuesta correcta


#         # Añadir información a las listas
#         lista_preguntas.append(pregunta_dict)
#         lista_opciones.append(opciones_dict)
#         lista_temas.append(tema_dict)
#         lista_respuestas.append(respuesta)


def procesar_pregunta(lista: list, lista_copiada: list, key: str) -> list:
    

    print(lista)

    for pregunta in lista:
        pregunta_copiada = None

        if key in pregunta:  # Validamos si la clave existe
            pregunta_copiada = pregunta[key]

        if pregunta_copiada is not None:  # Validamos si el valor no es None
            lista_copiada.append(pregunta_copiada)

    return lista_copiada






def dibujar_texto(text:str, font, color, surface, position):
    """
    Toma un texto, una fuente, un color, una superficie y una posición, y dibuja el texto en la superficie con la fuente y el color especificados.

    Parametros:
    - text (str): El texto que se va a dibujar.
    - font: La fuente que se utilizará para dibujar el texto.
    - color: El color del texto.
    - surface: La superficie en la que se dibujará el texto.
    - position: La posición en la que se dibujará el texto en la superficie, especificada como una tupla de coordenadas (x, y).

    Retorno:
    - text_rect: Un objeto Rect que representa el rectángulo que contiene el texto dibujado en la superficie.
    """
    
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=position)
    
    surface.blit(text_surface, text_rect)
    
    return text_rect




def mostrar_pregunta(screen, font, lista_preguntas:list, indice_pregunta_actual:int, mostrar_opciones:bool):
    """
    Toma la pantalla, la fuente, la lista de preguntas, el índice de la pregunta actual y una bandera para mostrar las opciones. Si se permite mostrar las opciones, dibuja el tema y la pregunta en la pantalla.

    Parametros:
    - screen: La pantalla en la que se mostrará la pregunta y el tema.
    - font: La fuente que se utilizará para mostrar el texto.
    - lista_preguntas: Una lista de diccionarios que representa las preguntas del juego.
    - indice_pregunta_actual: El índice de la pregunta actual en la lista de preguntas.
    - mostrar_opciones: Una bandera booleana que indica si se deben mostrar las opciones de respuesta.
    """
    
    if mostrar_opciones:
    
        # Toma el diccionario en el indice indicado
        pregunta_actual = lista_preguntas[indice_pregunta_actual]

        # Mostrar pregunta
        dibujar_texto(pregunta_actual, font, BLANCO, screen, (480, 100))




def mostrar_respuestas(screen, font, lista_a: list, lista_b :list, lista_c :list, 
                       indice_pregunta_actual: int, mostrar_opciones: bool) -> list:
    """
    Toma la pantalla, la fuente, la lista de preguntas, el índice de la pregunta actual y una bandera para indicar si se deben mostrar las opciones de respuesta. Si se permite mostrar las opciones, dibuja las opciones de respuesta en la pantalla y devuelve una lista de rectángulos que representan las áreas clicables de las opciones.

    Parametros:
    - screen: La pantalla en la que se mostrarán las opciones de respuesta.
    - font: La fuente que se utilizará para mostrar el texto.
    - lista_preguntas: Una lista de diccionarios que representa las preguntas del juego.
    - indice_pregunta_actual: El índice de la pregunta actual en la lista de preguntas.
    - mostrar_opciones: Una bandera booleana que indica si se deben mostrar las opciones de respuesta.

    Retorno:
    - opciones_rects: Una lista de tuplas que contiene los rectángulos y las opciones de respuesta dibujadas en la pantalla.
    """
    
    if mostrar_opciones:
    
        # Toma el diccionario en el indice indicado
        opcion_actual_a = lista_a[indice_pregunta_actual]
        opcion_actual_b = lista_b[indice_pregunta_actual]
        opcion_actual_c = lista_c[indice_pregunta_actual]

        # Mostrar opciones de respuesta
        rect_a = dibujar_texto(f"A. {opcion_actual_a}", font, NEGRO, screen, (389, 200))
        rect_b = dibujar_texto(f"B. {opcion_actual_b}", font, NEGRO, screen, (550, 200))
        rect_c = dibujar_texto(f"C. {opcion_actual_c}", font, NEGRO, screen, (700, 200))
                
        # Guardar rectángulos y opciones en la lista
        opciones_rects = [(rect_a, "a"), (rect_b, "b"), (rect_c, "c")]
                
        return opciones_rects

    return []



def dibujar_rectangulo(text, color, font, screen, x, y, tamaño_x, tamaño_y):
    """
    Toma un rectángulo que representa el área del botón, el texto a mostrar en el botón, el color del botón, la fuente del texto y la pantalla en la que se dibujará el botón. Dibuja el botón con el texto centrado en el rectángulo y el color especificado.

    Parametros:
    - rect: Un objeto Rect que representa el área del botón.
    - text: El texto que se mostrará en el botón.
    - color: El color del botón.
    - font: La fuente que se utilizará para el texto del botón.
    - screen: La pantalla en la que se dibujará el botón.
    """

    # Dibujar el rectángulo del botón
    pygame.draw.rect(screen, color, (x,y, tamaño_x, tamaño_y), border_radius=10)
    
    # Renderizar el texto del botón
    text_surface = font.render(text, True, NEGRO)
    text_rect = text_surface.get_rect(center=(x + tamaño_x / 2, y + tamaño_y / 2))
    
    # Dibujar el texto en el centro del rectángulo del botón
    screen.blit(text_surface, text_rect)




def comprobar_respuesta(opcion_selecionada, lista_preguntas: list, indice_pregunta_actual: int) -> bool:
    """
    Toma la opción seleccionada por el jugador, la lista de preguntas y el índice de la pregunta actual para determinar si la opción seleccionada coincide con la respuesta correcta en la pregunta actual.

    Parametros:
    - opcion_selecionada: La opción seleccionada por el jugador (por ejemplo, "a", "b", "c").
    - lista_preguntas: Una lista de diccionarios que representa las preguntas del juego.
    - indice_pregunta_actual: El índice de la pregunta actual en la lista de preguntas.

    Retorno:
    - bool: True si la opción seleccionada es la respuesta correcta, False de lo contrario.
    """

    # Obtener la pregunta actual
    respuesta_correcta = lista_preguntas[indice_pregunta_actual]

    print(respuesta_correcta)

    # Comparar la opción seleccionada con la respuesta correcta y devolver el resultado
    return opcion_selecionada == respuesta_correcta

    
def actualizar_puntaje(score:int, font):
    """
    Toma el puntaje actual y la fuente para crear una superficie de texto que muestra el puntaje actualizado. Devuelve la superficie de texto creada.

    Parametros:
    - score: El puntaje actual del jugador.
    - font: La fuente que se utilizará para mostrar el texto del puntaje.

    Retorno:
    - score_surface: La superficie de texto que muestra el puntaje actualizado.
    """

    # Renderizar el texto del puntaje con el puntaje actualizado
    score_surface = font.render("PUNTAJE: " + str(score), True, BLANCO)
    
    return score_surface



def procesar_respuesta(score:int) -> int:
    """
    Aumenta el puntaje del jugador en 10 puntos, desactiva la opción de mostrar las opciones de respuesta y muestra un mensaje indicando que la respuesta fue correcta.

    Parametros:
    - score(int): El puntaje actual del jugador.

    Retorno:
    - score: El puntaje actualizado después de sumar 10 puntos.
    """
    
    # Aumentar el puntaje en 10 puntos
    score += 10

    # Imprimir mensaje indicando que la respuesta fue correcta
    print("Respuesta correcta!")

    return score


def adelantar_personaje(posicion_personaje: list) -> list:
    """
    Simula el avance del personaje en el juego según ciertas condiciones de posición y límites.

    Parameters:
    - posicion_personaje (list): Lista que contiene las coordenadas [x, y] actuales del personaje.

    Returns:
    list: Lista actualizada de coordenadas [x, y] del personaje después del movimiento.
    """
    if posicion_personaje[1] == 280:
        posicion_personaje[0] += 200

    elif posicion_personaje[1] == 380:
        posicion_personaje[0] -= 200

    if posicion_personaje[0] >= 1020:
        posicion_personaje = [1020, 380]

    return posicion_personaje


def retrodecer_personaje(posicion_personaje: list) -> list:
    """
    Simula el retroceso del personaje en el juego según ciertas condiciones de posición.

    Parameters:
    - posicion_personaje (list): Lista que contiene las coordenadas [x, y] actuales del personaje.

    Returns:
    list: Lista actualizada de coordenadas [x, y] del personaje después del movimiento.
    """
    if posicion_personaje[1] == 280:
        posicion_personaje[0] -= 100
    
    elif posicion_personaje[1] == 380:
        posicion_personaje[0] += 100

    if posicion_personaje[0] < 300:
        posicion_personaje = [220, 280]
    
    elif posicion_personaje[0] > 1020:

        posicion_personaje = [1020, 280]

    return posicion_personaje



def caminar_casilla_especial(posicion_personaje: list) -> list:
    """
    Simula el movimiento del personaje en casillas especiales según ciertas condiciones de posición.

    Parameters:
    - posicion_personaje (list): Lista que contiene las coordenadas [x, y] actuales del personaje.

    Returns:
    list: Lista actualizada de coordenadas [x, y] del personaje después del movimiento.
    """
    # Si el personaje cae en avanzar 1
    if 800 < posicion_personaje[0] < 880 and posicion_personaje[1] == 280:
        posicion_personaje[0] += 100

        print("Avanza 1")
    
    # Si el personaje cae en retroceder 1
    elif 600 < posicion_personaje[0] < 680 and posicion_personaje[1] == 380:
        posicion_personaje[0] += 100

        print("Retrocede 1")


    return posicion_personaje



def pedir_nombre(font, screen, rect_nombre_usuario, texto_usuario:str):
    """
    Muestra en pantalla una interfaz para que el usuario ingrese su nombre.

    Parameters:
    - font (pygame.font.Font): Objeto de fuente para renderizar el texto.
    - screen (pygame.Surface): Superficie de la pantalla donde se dibujarán los elementos.
    - rect_nombre_usuario (tuple): Rectángulo que define el área de entrada del nombre en la pantalla.
    - texto_usuario (str): Texto actual ingresado por el usuario para el nombre.

    Returns:
    None
    """
    # Mostrar el mensaje "Ingrese su nombre" en la pantalla
    dibujar_texto("Ingrese su nombre", font, BLANCO, screen, (350, 280))

    # Dibujar el rectángulo de entrada del nombre
    pygame.draw.rect(screen, BLANCO, rect_nombre_usuario, 2)

    # Renderizar el texto actual ingresado por el usuario
    texto_surface = font.render(texto_usuario, True, NEGRO)
    screen.blit(texto_surface, (315 , 315))

    # Mostrar el mensaje "Presione ENTER para continuar" en la pantalla
    dibujar_texto("Presione ENTER para continuar", font, BLANCO, screen, (300, 350))



def cargar_puntajes():
    """
    Carga los puntajes almacenados en un archivo JSON y los devuelve como una lista de diccionarios.
    
    Returns:
    list: Lista de diccionarios que contienen los puntajes almacenados. Cada diccionario tiene las claves 'nombre' y 'puntaje'.
    """
    try:
        # Intenta abrir el archivo 'archivo_puntajes' en modo lectura ('r')
        with open(archivo_puntajes, 'r') as archivo:
            # Carga los puntajes desde el archivo JSON
            puntajes = json.load(archivo)
    except FileNotFoundError:
        # Si el archivo no existe, inicializa 'puntajes' como una lista vacía
        puntajes = []

    # Devuelve la lista de puntajes cargados desde el archivo JSON
    return puntajes




def guardar_puntaje(nombre:str, puntaje:int):
    """
    Guarda un nuevo puntaje (nombre y puntaje) en un archivo JSON que contiene una lista de puntajes.
    
    Parameters:
    - nombre (str): Nombre del jugador cuyo puntaje se va a guardar.
    - puntaje (int): Puntaje obtenido por el jugador.

    Returns:
    None
    """
    try:
        # Intenta abrir el archivo 'archivo_puntajes' en modo lectura ('r')
        with open(archivo_puntajes, 'r') as archivo:
            # Carga los puntajes existentes desde el archivo JSON
            puntajes = json.load(archivo)
    except FileNotFoundError:
        # Si el archivo no existe, inicializa 'puntajes' como una lista vacía
        puntajes = []

    # Agrega el nuevo puntaje (nombre y puntaje) a la lista 'puntajes'
    puntajes.append({'nombre': nombre, 'puntaje': puntaje})

    # Ordena los puntajes en orden descendente según el puntaje y toma los primeros 10
    puntajes = sorted(puntajes, key=lambda x: x['puntaje'], reverse=True)[:10]

    # Abre el archivo 'archivo_puntajes' en modo escritura ('w')
    with open(archivo_puntajes, 'w') as archivo:
        # Escribe la lista de puntajes ordenados en el archivo JSON con formato indentado
        json.dump(puntajes, archivo, indent=4)



def mostrar_puntajes(font, screen, img_personajes):
    """
    Muestra los puntajes almacenados en el archivo JSON en la pantalla.

    Parameters:
    - font (pygame.font.Font): Objeto de fuente para renderizar el texto.
    - screen (pygame.Surface): Superficie de la pantalla donde se dibujarán los elementos.
    - img_personajes (pygame.Surface): Imagen del personaje que se muestra en la pantalla.

    Returns:
    None
    """
    # Cargar los puntajes desde el archivo JSON
    puntajes = cargar_puntajes()

    # Configurar la posición inicial de dibujo vertical
    y_offset = 150

    # Dibujar el título "PUNTAJES" en la pantalla
    dibujar_texto("PUNTAJES", font, BLANCO, screen, (650, 100))

    # Escalar y dibujar la imagen del personaje en la pantalla
    picture_personaje = pygame.transform.scale(img_personajes, [100, 200])
    posicion_personaje = [300, 300]
    screen.blit(picture_personaje, posicion_personaje)

    # Iterar sobre los puntajes y dibujar cada uno en la pantalla
    for i, puntaje in enumerate(puntajes):
        puntaje_texto = f"{i + 1}. {puntaje['nombre']} - {puntaje['puntaje']}"
        puntaje_surface = font.render(puntaje_texto, True, BLANCO)

        # Dibujar el texto del puntaje en la pantalla con un desplazamiento vertical
        screen.blit(puntaje_surface, (650, y_offset))

        # Incrementar el desplazamiento vertical para la siguiente línea de texto
        y_offset += 50
