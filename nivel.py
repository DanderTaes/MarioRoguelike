import config
from characters.enemigos.koopa import Koopa
from characters.enemigos.cangrejo import Cangrejo
from characters.enemigos.mosca import Mosca
from characters.enemigos.bola_fuego import Bola_fuego
from characters.enemigos.moneda import Moneda
import random
# tener arrays con los frames cuando los enemigos spawneán y cambiar tiles cada 5 o así



class Nivel:
    def __init__(self, nivel: int, frame, modo=0):
        self.gaming = True
        self.modo = modo # 0 es niveles preparados, 1 es aleatorio
        self.nivel = nivel
        self.tilemap = 0
        self.start_frame = frame + 60# cambiar para siguientes niveles y eso (2 segundos de delay)
        if modo == 0:
            self.nivel_spawns = self.level_preset()
        else:
            self.nivel_spawns = self.level_randomizer()

        if self.nivel_spawns == None:
            self.gaming = False
        else:
            self.last_frame = list(self.nivel_spawns.keys())[-1] + self.start_frame
        
        

    def spawn(self, frame_global):
        frame = frame_global - self.start_frame

        enemies = []
        for time in self.nivel_spawns.keys(): # Koopa: "k", cangrejo: "c", Mosca: "m", Bola fuego: "b", hielo cosa: "h"
            if time == frame:
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
        if self.nivel == 1: # añadir más niveles
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



    def text(self, frame):
        if frame - self.start_frame <0: # DOS SEGUNDOS DE INTRO
            return f"NIVEL {self.nivel}"
        return ""
