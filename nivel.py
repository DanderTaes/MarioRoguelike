import config
from characters.enemigos.koopa import Koopa
from characters.enemigos.cangrejo import Cangrejo
from characters.enemigos.mosca import Mosca
from characters.enemigos.bola_fuego import Bola_fuego
from characters.enemigos.moneda import Moneda
import random



class Nivel:
    def __init__(self, nivel: int, frame, modo=0):
        # Hay enemigos que spawnear o matar?
        self.gaming = True
        # nivel de dificultad
        self.nivel = nivel
        # qué mapa se usa para el nivel (0 default)
        self.tilemap = 0
        # cada vez que nivel es ejecutado se coge el frame en el que estaba como incial y se esperan 2 segundos para empezar a spawnear enemigos
        self.start_frame = frame + 60 
        
        self.modo = modo # 0 es la demo, 1 es aleatorio
        if modo == 0:
            self.nivel_spawns = self.level_preset()
        else:
            self.nivel_spawns = self.level_randomizer()

        # si no hay más que spawnear devuelve None (entonces gaming es Falso)
        if self.nivel_spawns == None:
            self.gaming = False
        else:
            # si sí hay personajes que spawnear se coge el último frame en el que se va a spawnear como limite superior del nivel
            self.last_frame = list(self.nivel_spawns.keys())[-1] + self.start_frame
        
        

    def spawn(self, frame_global):
        # frame es el frame local suponiendo que se empieza en el "start_frame"
        frame = frame_global - self.start_frame

        enemies = []
        # se itera por cada uno de los frames del diccionario
        for time in self.nivel_spawns.keys(): # Koopa: "k", cangrejo: "c", Mosca: "m", Bola fuego: "b", hielo cosa: "h"
            if time == frame:
                # solo los enemigos que tienen "enfado" cuenta como input el self.nivel_spawns[time][2]
                if self.nivel_spawns[time][0] == "k":
                    enemigo = Koopa(*self.nivel_spawns[time][1], self.nivel_spawns[time][2])
                    enemies.append(enemigo)

                elif self.nivel_spawns[time][0] == "c":
                    enemigo = Cangrejo(*self.nivel_spawns[time][1], self.nivel_spawns[time][2])
                    enemies.append(enemigo)

                elif self.nivel_spawns[time][0] == "m":
                    enemigo = Mosca(*self.nivel_spawns[time][1], self.nivel_spawns[time][2])
                    enemies.append(enemigo)

                elif self.nivel_spawns[time][0] == "b1":
                    enemigo = Bola_fuego(*self.nivel_spawns[time][1])
                    enemies.append(enemigo)

                elif self.nivel_spawns[time][0] == "b2":
                    enemigo = Bola_fuego(*self.nivel_spawns[time][1], 1)
                    enemies.append(enemigo)

                elif self.nivel_spawns[time][0] == "$":
                    enemigo = Moneda(*self.nivel_spawns[time][1], self.nivel_spawns[time][2])
                    enemies.append(enemigo)
        return enemies

    def level_preset(self):
        # niveles por defecto
        if self.nivel == 1:
            self.tilemap = 0
            return config.NIVEL_1 
        elif self.nivel == 2: 
            self.tilemap = 1
            return config.NIVEL_2
        elif self.nivel == 3: 
            self.tilemap = 2
            return config.NIVEL_3
        elif self.nivel == 4:
            self.tilemap = 0
            return config.NIVEL_4
        elif self.nivel == 5: 
            self.tilemap = 3
            return config.NIVEL_5
        else:
            return None

    def level_randomizer(self):

        # Este randomizer está bastante inspirado en la lógica del juego Risk of Rain 2.
        """
        A cada enemigo se le asigna un coste (que podemos editar en el archivo config), y al randomizer se le da unos créditos para spawnear cosas cada nivel,
        en este caso está hecho para que cada nivel tenga 500 creditos más que el anterior (se puede cambiar).
        El que cada nivel tenga un numero de créditos específicos hace que la puntuación máxima de cada nivel sea igual, así que llegar al nivel 5 dará la misma puntuación
        da igual que enemigos te spawneen. (No coger monedas puede hacer que la puntuación baje, pero la máxima es la misma).
        
        En spawnables_total se crea una lista de todos los enemigos ordenados por dificultad (separando enfado de enemigos), y cada nivel se va ampliando el
        rango de spawnear de esa lista, (puse que cada nivel va dejando 2 enemigos más dificiles pero se podría cambiar para poder hacerlo más facil al principio).
        
        Una vez tiene los enemigos que puede spawnear se hace un bucle hasta que se quede sin creditos, cada iteración intenta spawnear un enemigo random de la lista
        anterior, pero siempre teniendo en cuenta los créditos que cuesta cada enemigo (o moneda).

        Una vez tiene los enemigos en una lista (spawning_enemies), crea otra lista de en qué frames saldrán esos enemigos, con un numero aleatorio de tiempo entre ellos
        entre min_frames_between_enemies y max_frames_between_enemies.

        Con esas dos listas crea el diccionario que interpreta la función spawn()
        
        
        """

        enemies = ["k", "c", "m", "b1", "b2", "$"]
        values = [config.VAL_KOOPA, config.VAL_CANGREJO, config.VAL_MOSCA, config.VAL_B1, config.VAL_B2, config.VAL_MONEDA]
        frame = 0
        spawnables_total = [("k", 0), ("$", 0), ("m", 0), ("c", 0), ("k", 1), ("b1", 0), ("m", 1), ("c", 1),  ("b2", 0), ("c", 2)]
        spawnables = spawnables_total[:1]
        spawning_frames = []
        spawning_enemies = [] # tupla con tipo y enfado
        credits = self.nivel * 500
        min_frames_between_enemies = 30
        max_frames_between_enemies = 60

        if self.nivel > 1:
            self.tilemap = random.randint(0,3)

        # choose enemies
        if self.nivel < 2:
            spawnables = spawnables_total[:4]
        elif self.nivel < 3:
            spawnables = spawnables_total[:6]
        elif self.nivel < 4:
            spawnables = spawnables_total[:8]
        else:
            spawnables = spawnables_total
        
        while credits > 0:
            enem = random.choice(spawnables)
            enem_pos = enemies.index(enem[0])
            enem_value = values[enem_pos]
            if enem[1] != 0:
                enem_value = values[enem_pos] * (enem[1] * 4)

            if enem_value <= credits:
                credits -= enem_value
                spawning_enemies.append(enem)

        for _ in range(len(spawning_enemies)):
            ran_frame = random.randint(min_frames_between_enemies, max_frames_between_enemies)
            spawning_frames.append(frame + ran_frame)
            frame += ran_frame
    
        
        final_dict = dict.fromkeys(spawning_frames)

        for i, frames in enumerate(spawning_frames):
            pos = random.choice([(27*8, 2*8), (4*8, 2*8)])
            final_dict[frames] = [spawning_enemies[i][0], pos, spawning_enemies[i][1]]

        return final_dict


    # texto introductivo de cada nivel
    def text(self, frame):
        if frame - self.start_frame <0: # DOS SEGUNDOS DE INTRO
            return f"NIVEL {self.nivel}"
        return ""
