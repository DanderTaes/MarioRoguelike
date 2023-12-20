from character import Character
import random
import config
import pyxel


class Enemigo(Character):
    def __init__(self, x, y, sprite, vidas):
        super().__init__(x, y, sprite, vidas)
        self.stuneable = True # en general si se puede stunear al enemigo o no
        self.last_frame = 0 # ultima vez stuneado (para evitar doble stunneo a la vez del mismo personaje)
        self.frame_stun = None # en qué frame ha sido stuneado (contador para despertar)
        self.downed = False # está stuneado (comprueba si el anterior frame estaba stuneado)
        self.enfado = 0 # cambia velocidad y eso
        self.loopeable = False # vuelve a salir por arriba si entra en tubería?
        self.type = "" # tipo de personaje
        self.turnaround_frame = 0 # frame en el que se encuentra a otro enemigo del mismo tipo

        self.point_value = 0 # cuanto vale al matarlo
    

    # volver a spawnear arriba si entran en las tuberías
    def volver_a_salir(self):
        if self.dying == False:
            new_pos = random.choice([(27*8, 2*8), (4*8, 2*8)])
            self.x, self.y = new_pos
            if self.dx > 0 and self.x > config.WIDTH/2:
                self.last_dx *= -1
            elif self.dx < 0 and self.x < config.WIDTH/2:
                self.last_dx *= -1

    def stun_detect(self, bloque, frame, pow = False):
        if frame-self.last_frame > 15: # delay de 0.5s (30fps)
            if self.stuneable:
                if pow and self.is_grounded: # si le han dado al pow y estaba en el suelo

                    # ajustar saltito cuando los stunneas
                    if self.gravedad_max == 0.2:
                        self.dy = -2
                    else:
                        self.dy = -5
                    if self.vidas > 0:
                        self.vidas = 0
                else:
                    for tile in bloque:
                        dist_x = abs(self.x - (tile[0][0])*8)
                        dist_y = abs(self.y+self.sprite[3] - tile[0][1]*8)
                        # colisión con los bloques levantados
                        if (dist_x < 10 and dist_y < 1):
                            if self.gravedad_max == 0.2:
                                self.dy = -2
                            else:
                                self.dy = -5
                            if self.vidas > 0:
                                # sonido de stunneo
                                pyxel.play(3, 4, 30, False)
                                self.vidas -= 1
                            else:
                                self.downed = False
                                self.vidas = self.max_vidas
            self.last_frame = frame
        elif self.last_frame == 0:
            self.last_frame = frame

