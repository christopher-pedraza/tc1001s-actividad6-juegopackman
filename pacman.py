"""
Actividad 6: Juego del Packman

Equipo 9:
Christopher Gabriel Pedraza Pohlenz A01177767
Kevin Susej Garza Aragón A00833985
Eugenia Ruiz Velasco Olvera A01177887
"""


# Se importan las librerías de random, turtle y freegames
from random import *
from turtle import *
from freegames import floor, vector

# Declara la puntuación inical
state = {'score': 0}
# Crea dos instancias de turtle en la que la tortuga es invisible
path = Turtle(visible=False)
writer = Turtle(visible=False)
# Vectores de posición y dirección iniciales
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-160, 40), vector(5, 0)],
    [vector(-90, -40), vector(0, 5)],
    [vector(10, 120), vector(0, -5)],
    [vector(0, -120), vector(-5, 0)],
]

# Declara matriz del mapa. 0 = pared, 1 = camino
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]


# Función para dibujar los cuadros del mapa
def square(x, y):
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


# Función para convertir coordenadas en posición de matriz
def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


# Función para verificar si la posición recibida es válida en el tablero
def valid(point):
    # Obtener posición en matriz
    index = offset(point)
    
    # Checar si es pared o camino
    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


# Función para crear el tablero
def world():
    # Declarar colores
    bgcolor('black')
    path.color('blue')

    # Recorrer matriz dibujando tablero
    for index in range(len(tiles)):
        tile = tiles[index]

        # Crear cuadro azul 
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            
            # Agregar comida
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


# Función para mover pacman y fantasmas
def move():
    # Puntaje
    writer.undo()
    writer.write(state['score'])

    # Elimina los dibujos en la pantalla
    clear()

    # Checa si se puede mover pacman
    if valid(pacman + aim):
        pacman.move(aim)

    # Obtener posición en matriz
    index = offset(pacman)

    # Checar si hay camino y comida
    if tiles[index] == 1:
        # Declarar espacio sin comida
        tiles[index] = 2
        # Aumenta el puntaje
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    # Dejar de pintar
    up()
    # Mover pacman a esta posición
    goto(pacman.x + 10, pacman.y + 10)
    # Hacer un círculo relleno
    dot(20, 'yellow')

    # Ciclo para mover a los fantasmas
    for point, course in ghosts:
        # Si la posición es válida se mueven
        if valid(point + course):
            point.move(course)
        # Cambiar posición
        else:
            MIN = 3
            MAX = 10
            options = [
                # Elegir velocidad aleatoria
                vector(randint(MIN, MAX), 0),
                vector(-randint(MIN, MAX), 0),
                vector(0, randint(MIN, MAX)),
                vector(0, -randint(MIN, MAX)),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y
            
        # Dejar de dibujar
        up()
        # Mover fantasma a esta posición
        goto(point.x + 10, point.y + 10)
        # Hacer un círculo relleno
        dot(20, 'red')


    update()

    # Si colisiona pacman con fantasma, se termina juego
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    # Llamar función cada 20 milisegundos
    ontimer(move, 20)


# Cambiar direcciónd e pacman si es válida
def change(x, y):
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


# Establecer el ancho, largo, y posición inicial en x y y
setup(420, 420, 370, 0)
# Esconder el cursor, la tortuga
hideturtle()
# Elimina la animación de la tortuga
tracer(False)
# Configuración del puntaje
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
# Empieza a "escuchar" las teclas que se presionan
listen()
# onkey(func, key) une una función a una tecla, para que se llame a esta cuando se presiona la tecla
# Cambia el vector de dirección del pacman
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
# Crea el tablero
world()
# Llama a la función move
move()
# Comienza el ciclo de eventos
done()

