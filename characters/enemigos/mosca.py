import config
from characters.enemigo import Enemigo

#Solo falta cambiar los sprites y numero de vidas y esas cosas, y meterlo de herencia en las demas files
#Aqui tambien hay que cambair le movimiento
class Mosca(Enemigo):
    def __init__(self, x, y, mode=0):
        super().__init__(x, y, [0, 104, 15, 15], vidas=1)
        if self.x > config.WIDTH / 2:
            self.dx = -0.2
        else:
            self.dx = 0.2
        self.last_dx = self.dx
        self.gravedad_max = 0.2
        self.last_jump_frame = 0
        self.point_value = config.VAL_MOSCA # cuantos puntos por matarla
        if mode == 1:
            sign = 1 if self.last_dx > 0 else -1
            self.last_dx = 2 *(self.enfado+1)* sign
            self.point_value = config.VAL_MOSCA * 4 # cuantos puntos por matarla
            self.enfado = 1
        self.type = ""



    def move(self, frame):
        last_y = self.gravity()
        self.moving = True
        if self.vidas == 0:
            if not self.downed:
                self.frame_stun = frame
                self.downed = True                
            self.moving = False
            self.dx = 0
            if frame - self.frame_stun > 150:  # 5 segundos de delay
                self.enfado = 1
                self.downed = False
                self.dx = self.last_dx
                self.moving = True
                self.vidas = self.max_vidas
        else:
            if self.is_grounded:
                espera = 45
                if self.enfado == 1:
                    espera = 35
                if frame - self.last_jump_frame >= espera: # salta cada 1,5 segs
                    self.dy = -2
                    self.last_jump_frame = frame
                self.dx = 0
            else:
                sign = 1 if self.last_dx > 0 else -1
                self.last_dx = ((self.enfado+1)*0.2) * sign
                self.dx = self.last_dx
                self.moving = True
        self.update_pos(last_y)

    def animate(self, frame):
        self.sprite[0] = 0
        if self.enfado != 0:
            self.sprite[1] = 120
        else:
            self.sprite[1] = 104
        if self.moving:
            self.sprite[0] = (((frame // 2) % 2)+1) * 16
        else:
            self.sprite[0] = 48

        if self.dx < 0:
            self.sprite[2] = 16
        else:
            self.sprite[2] = -16