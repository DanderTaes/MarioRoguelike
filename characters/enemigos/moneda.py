import config
from characters.enemigo import Enemigo

class Moneda(Enemigo):
    def __init__(self, x, y, mode=0):
        super().__init__(x, y, [0, 184, 8, 11], vidas=1)
        if self.x > config.WIDTH / 2:
            self.dx = -1
        else:
            self.dx = 1
        self.last_dx = self.dx
        if mode == 1:
            self.dx = 0
            self.last_dx = 0
        self.max_vidas = 0 # ESTO ES LO QUE LE INDICA AL RESTO DE CLASES QUE ES UNA MONEDA

        self.point_value = config.VAL_MONEDA # cuantos puntos por matarla
    
    def volver_a_salir(self):
        # reescribir la funcion de las tuberías para que despawnee si llega a una tubería (solo tienes para cogerla un tiempo limitado)
        self.alive = False
    
    def slow_death_enemy(self, frame):
        # sobreescribir la animacion de muerte para hacer la explosioncita
        if self.dying == False:
            self.death_frame = frame
            self.dying = True
            self.dy = -1
            self.invincibility = True
            self.gravedad_max = 0
            self.sprite = [32, 184, 16, 16]
            self.y -= 5
            self.dx = 0
        else:
            if frame - self.death_frame < 12:
                if (frame - self.death_frame) % 3 == 0:
                    self.sprite[0] += 16
            else:
                self.alive = False

    def move(self, frame):
        if self.vidas == 0:
            if self.dying == False:
                self.slow_death_enemy(frame)
        else:
            self.dx = self.last_dx
        self.update_pos()

    def animate(self, frame):
        if self.dying == False:
            self.sprite[0] = (((frame//2)%4))*8