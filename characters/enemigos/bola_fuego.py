import config
from characters.enemigo import Enemigo


class Bola_fuego(Enemigo):
    def __init__(self, x, y, mode=0): # mode 0 --> roja, mode 1 --> verde
        super().__init__(x, y, [96, 184, 8, 8], vidas=1)
        # que caiga mas lento
        self.gravedad_max = 0.2
        # cuanto tiempo antes de volver a "saltar"
        self.jump_wait = 10
        self.point_value = config.VAL_B1
        self.first_frame = 0
        self.spawned = False # detecta simplemente la primera vez que aparece para el timer

        # cambiar cosas dependiendo de qué tipo es
        max_vel = 0.2
        if mode == 0:
            self.sprite[1] = 192
        elif mode == 1:
            self.point_value = config.VAL_B2
            self.enfado = 1
            max_vel = 4
            self.jump_wait = 0
            self.gravedad_max = 1
            self.sprite[1] = 184

        # hacer que tenga una velocidad incial hacia el centro del tablero
        if self.x > config.WIDTH / 2:
            self.dx = -max_vel
        else:
            self.dx = max_vel
        
        # no se puede matar, hay que esperar hasta que desaparezca
        self.stuneable = False
        self.last_dx = self.dx
        self.last_jump_frame = 0
    

    def slow_death_enemy(self, frame): # 120, 184 --> 120, 192
        # sobreescribir la función de muerte para hacer animacion customizada
        if self.dying == False:
            self.death_frame = frame
            self.dying = True
            self.dy = -1
            self.invincibility = True
            self.gravedad_max = 0
            self.sprite = [120, 192, 8, 8]
            if self.enfado != 0:
                self.sprite = [120, 184, 8, 8]
            self.y -= 5
            self.dx = 0
        else:
            if frame - self.death_frame < 15:
                if (frame - self.death_frame) % 3 == 0:
                    self.sprite[0] += 8
            else:
                self.alive = False

    def move(self, frame):
        if self.vidas == 0:
            if self.dying == False:
                self.slow_death_enemy(frame)

        if self.spawned == False:
            # coger el primer frame cuando spawnea para contar el tiempo antes de morir (ya que frame no lo tenemos en el init)
            self.first_frame = frame
            self.spawned = True

        if self.is_grounded:
            if frame - self.last_jump_frame >= self.jump_wait: # salta cada 0,333 segs (la roja)
                self.dy = -3
                if self.jump_wait == 0:
                    self.dy = -10
                self.last_jump_frame = frame
            self.dx = 0
        else:
            self.dx = self.last_dx

        if frame - self.first_frame >= 1/(self.enfado + 1) * 450: # que dure más la roja que la verde
            self.vidas = 0
        self.update_pos()

    def animate(self, frame):
        if self.dying == False:
            self.sprite[0] = (((frame // 2) % 3)+12)* 8

        if self.dx < 0:
            self.sprite[2] = 8
        else:
            self.sprite[2] = -8