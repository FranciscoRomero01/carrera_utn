import pygame
import sys
import time

from biblioteca_datos import *
from data import *

# Inicializar pygame
pygame.init()

# Definir dimensiones de la ventana
WIDTH, HEIGHT = 1200, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Preguntas y Puntaje")

# Definir fuente
font = pygame.font.SysFont(None, 30)
font_2 = pygame.font.SysFont("Arial", 15)
font_3 = pygame.font.SysFont(None, 40)

# Definir botones como rectángulos
boton_comenzar = pygame.Rect(300, 587, 160, 80)
boton_terminar = pygame.Rect(600, 587, 160, 80)

lista_preguntas = []  # Lista para almacenar las sub-listas de preguntas
lista_opcion_a = []  # Lista para almacenar las sub-listas de opciones
lista_opcion_b = []  # Lista para almacenar las sub-listas de opciones
lista_opcion_c = []  # Lista para almacenar las sub-listas de opciones
lista_temas = []  # Lista para almacenar las sub-listas de temas
lista_respuestas = []  # Lista para almacenar las sub-listas de respuestas correctas


# Procesar preguntas
lista_preguntas = procesar_pregunta(lista, [], "pregunta")
lista_opcion_a = procesar_pregunta(lista, [], "a")
lista_opcion_b = procesar_pregunta(lista, [], "b")
lista_opcion_c = procesar_pregunta(lista, [], "c")
lista_temas = procesar_pregunta(lista, [], "tema")
lista_respuestas = procesar_pregunta(lista, [], "correcta")


 # Añadir información a las listas
print(f"Preguntas: {lista_preguntas}")
print(f"Opciones: {lista_opcion_a}")
print(f"Opciones: {lista_opcion_b}")
print(f"Opciones: {lista_opcion_c}")
print(f"Temas: {lista_temas}")
print(f"Respuestas: {lista_respuestas}")

# Variable para el índice de la pregunta actual
indice_pregunta_actual = 0

# Inicializar puntaje
score = 0

# Variables para rastrear la visibilidad de las opciones
mostrar_opciones = False

# Variable para almacenar los rectángulos de las opciones
opciones_rects = []

# Crear una superficie de texto para el puntaje una sola vez
score_surface = actualizar_puntaje(score, font_3)


# Definir la imagen
img = pygame.image.load("Logo.png")
picture = pygame.transform.scale(img, [300, 200])

# Definir la imagen
img_personajes = pygame.image.load("Personaje.png")
picture_personaje = pygame.transform.scale(img_personajes, [40, 80])

# Definir la imagen
img_flecha = pygame.image.load("Flecha.png")
picture_flecha = pygame.transform.scale(img_flecha, [100, 40])

# Definir la imagen
img_flecha_abajo = pygame.image.load("Flecha_abajo.png")
picture_flecha_abajo = pygame.transform.scale(img_flecha_abajo, [80, 100])

img_utn = pygame.image.load("UTN.png")
picture_utn = pygame.transform.scale(img_utn, [140, 80])


posicion_personaje = [1000, 1000]

# Variable para rastrear mensajes temporales
mensaje_temporal = ""
mensaje_temporal_pos = (0, 0)

# Timer 1 segundos
timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos, 1000)

segundos = "0"

fin_tiempo = False

# Timer 2 segundos

timer_2_segundos = pygame.USEREVENT + 1
pygame.time.set_timer(timer_2_segundos, 2000)

mostrar_todo = True

rect_nombre_usuario = pygame.Rect(300, 300, 300, 50)
texto_usuario = ''
texto_mostrado = ''

flag_mostrar_puntajes = False

posicion_puntajes = [500, 100]


# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.USEREVENT:
            if event.type == timer_segundos:

                if fin_tiempo:
                    segundos = int(segundos) - 1

                    if int(segundos) == -1:

                        segundos = "5"

                        # Avanzar al siguiente índice de pregunta
                        indice_pregunta_actual = (indice_pregunta_actual + 1)


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:

                print(score)

                guardar_puntaje(texto_usuario, score)
                texto_usuario = ''

                flag_mostrar_puntajes = True

            elif event.key == pygame.K_BACKSPACE:
                texto_usuario = texto_usuario[:-1]

            else:
                texto_usuario += event.unicode



        # Manejo del evento de clic del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:


            # Botón para avanzar a la siguiente pregunta
            if boton_comenzar.collidepoint(event.pos):

                # Mostrar las opciones nuevamente y restablecer los intentos y el mensaje temporal
                mostrar_opciones = True
                intentos = 0
                posicion_personaje = [220, 280]
                segundos = "5"
                mostrar_todo = True
                fin_tiempo = True
                flag_mostrar_puntajes = False

                indice_pregunta_actual = 0
                score = 0
                score_surface = actualizar_puntaje(score, font)


            # Botón para terminar el juego
            if boton_terminar.collidepoint(event.pos):

                # Reiniciar el puntaje, el índice de pregunta actual y el mensaje temporal
                indice_pregunta_actual = 0
                mostrar_opciones = True
                intentos = 0
                mostrar_todo = False

                score_surface = actualizar_puntaje(score, font)

            # Verificar si se están mostrando las opciones y si hay opciones disponibles
            if mostrar_opciones and opciones_rects:
                for i, (rect, opcion) in enumerate(opciones_rects):

                    # Verificar si el clic del mouse ocurrió dentro de un rectángulo de opción
                    if rect.collidepoint(event.pos):

                        print(f"Opción '{opcion}' seleccionada")

                        # Comprobar si la opción seleccionada es correcta
                        respuesta = comprobar_respuesta(opcion, lista_respuestas, indice_pregunta_actual)

                        # Avanzar al siguiente índice de pregunta
                        indice_pregunta_actual = (indice_pregunta_actual + 1)

                        segundos = "5"

                        if respuesta:

                            # Procesar la respuesta correcta
                            score = procesar_respuesta(score)
                            score_surface = actualizar_puntaje(score, font)


                            posicion_personaje = adelantar_personaje(posicion_personaje)

                        else:

                            posicion_personaje = retrodecer_personaje(posicion_personaje)




    # Limpiar la pantalla
    screen.fill(AZUL_FONDO)

    # Mostrar el mensaje temporal
    dibujar_texto(mensaje_temporal, font, BLANCO, screen, mensaje_temporal_pos)

    print(posicion_personaje)

    posicion_personaje = caminar_casilla_especial(posicion_personaje)


    # si llega a la meta

    if posicion_personaje[0] <= 300 and posicion_personaje[1] == 380:

        mostrar_todo = False



    # Mostrar la pregunta y las opciones si el índice de pregunta actual es válido
    if indice_pregunta_actual < len(lista_preguntas) and mostrar_todo == True:

        dibujar_rectangulo("", VERDE_OSCURO, font, screen, 350, 10, 500, 250)

        mostrar_pregunta(screen, font_2, lista_preguntas, indice_pregunta_actual, mostrar_opciones)

        opciones_rects = mostrar_respuestas(screen, font_2, lista_opcion_a, lista_opcion_b, lista_opcion_c,
                                             indice_pregunta_actual, mostrar_opciones)
        
        
        screen.blit(score_surface, (1000, 200))  # Mostrar el puntaje


        # Mostrar rectangulos de casillas
        for color in colores_niveles:

            if len(color) == 3:
                dibujar_rectangulo("", color[0], font_2, screen, color[1], color[2], 80, 50)
                dibujar_rectangulo("", color[0], font, screen, color[1], (color[2] + 100), 80, 50)
            else:
                dibujar_rectangulo(color[3], color[0], font_2, screen, color[1], color[2], 80, 50)



        # Dibujar imagenes
        screen.blit(picture_flecha, [200, 350])
        screen.blit(picture_flecha_abajo, [1090, 350])
        screen.blit(picture_utn, [150, 400])
        screen.blit(picture_personaje, posicion_personaje)



        dibujar_texto("Salida", font_2, NEGRO, screen, (210, 360))

        dibujar_texto("Llegada", font_2, NEGRO, screen, (190, 480))


        segundos_texto = font_3.render(f"TIEMPO: {str(segundos)}", True, (255,255,255))
        screen.blit(segundos_texto, (1000,100))

    else:

        dibujar_texto(f"FIN DEL JUEGO! ", font, BLANCO, screen, (400, 20))


        # Si se pide el nombre o no
        if flag_mostrar_puntajes == False:
            pedir_nombre(font, screen, rect_nombre_usuario, texto_usuario)

        else:
            mostrar_puntajes(font, screen, img_personajes)



    # Dibujar los botones
    dibujar_rectangulo("Comenzar", AZUL_CLARO, font, screen, 300, 587, 160, 80)
    dibujar_rectangulo("Terminar", AZUL_CLARO, font, screen, 600, 587, 160, 80)


    # Mostrar la imagen
    screen.blit(picture, [30, 30])


    pygame.display.flip()  # Actualizar la pantalla


pygame.quit()