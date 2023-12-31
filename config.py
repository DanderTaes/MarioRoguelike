
# Ancho y alto de la Pantalla
WIDTH = 256
HEIGHT = 216

# Posición (u, v) para los 4 bloques "doblados" de cada tipo
AMARILLOS = [(6,3), (7, 3), (6,2), (7, 2)]
AZULES = [(16,3), (17,3), (16, 2), (17, 2)]
LADRILLO_AZUL = [(4, 1), (5, 1), (4, 0), (5, 0)]
PLAT_AMARILLA = [(12, 1), (13, 1), (12, 0), (13, 0)]
LADRILLO_ROJO = [(22, 1), (23, 1), (22, 0), (23, 0)]

# Posición (u, v) para las tuberías en las que los enemigos pueden entrar (para salir por arriba)
PIPES = [(3,7), (4,7), (3,8), (4,8)]


# Koopa: "k", cangrejo: "c", Mosca: "m", Bola fuego: "b1" o "b2", moneda: "$"
# keys del dict --> Frames; valores del dict --> [tipo de enemigo, coordenadas de spawn, nivel de enfado]
# El modo de enfado del enemigo sólo vale en mosca (0,1), koopa (0,1), y cangrejo (0,1,2)

# Niveles prehechos de la demo
NIVEL_1 = {30: ["k", (27*8, 2*8), 0], 60: ["k", (4*8, 2*8), 0], 90: ["m", (27*8, 2*8), 0], 95: ["$", (4*8, 2*8), 0]}

NIVEL_2 = {30: ["k", (27*8, 2*8), 1], 31: ["k", (4*8, 2*8), 0], 45: ["$", (4*8, 2*8), 0], 60: ["c", (4*8, 2*8), 0], 90: ["m", (27*8, 2*8), 0], 95: ["$", (4*8, 2*8), 0]}

NIVEL_3 = {30: ["k", (27*8, 2*8), 1], 31: ["b1", (4*8, 2*8), 0], 60: ["$", (4*8, 2*8), 0], 80: ["c", (4*8, 2*8), 0], 100: ["m", (27*8, 2*8), 0], 120: ["$", (4*8, 2*8), 0], 130: ["m", (27*8, 2*8), 0]}

NIVEL_4 = {30: ["c", (27*8, 2*8), 1], 31: ["m", (4*8, 2*8), 0], 45: ["$", (4*8, 2*8), 0], 60: ["b2", (4*8, 2*8), 0], 90: ["$", (27*8, 2*8), 0], 95: ["$", (4*8, 2*8), 0], 280: ["c", (27*8, 2*8), 2]}

NIVEL_5 = {30: ["$", (27*8, 18*8), 1], 31: ["$", (23*8, 18*8), 1], 32: ["$", (4*8, 18*8), 1], 33: ["$", (8*8, 18*8), 1], 34: ["$", (1*8, 13*8), 1], 35: ["$", (30*8, 13*8), 1], 36: ["$", (15*8, 11*8), 1], 37: ["$", (20*8, 11*8), 1], 38: ["$", (10*8, 11*8), 1], 39: ["$", (23*8, 5*8), 1], 40: ["$", (8*8, 5*8), 1]}

# VALORES DE SCORE: Versiones enfadadas serán 4 veces más creditos (para spawnear)
# Estos valores no sólo son la puntuación que se lo otorga a mario al matarlos sino también lo que le "cuesta" al juego spawnear a esos enemigos en el roguelike.
# Cada nivel el roguelike tendrá X creditos para spawnear enemigos y estos son los costes de cada uno de los enemigos (y monedas)
VAL_MONEDA = 300
VAL_KOOPA = 100
VAL_CANGREJO = 300
VAL_B1 = 400
VAL_B2 = 600
VAL_MOSCA = 200