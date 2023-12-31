import config
from characters.enemigo import Enemigo

class Cangrejo(Enemigo):
    def __init__(self, x, y, mode=0):
        super().__init__(x, y, [0, 136, 16, 16], vidas=2)
        if self.x > config.WIDTH / 2:
            self.dx = -1
        else:
            self.dx = 1
        self.last_dx = self.dx
        
        self.point_value = config.VAL_CANGREJO # cuantos puntos por matarla
        if mode == 1:
            signo = 1 if self.last_dx > 0 else -1
            self.last_dx = 2 * signo
            self.point_value = config.VAL_CANGREJO * 4 # cuantos puntos por matarla y por spawnearla
            self.enfado = 1
        if mode == 2:
            signo = 1 if self.last_dx > 0 else -1
            self.last_dx = 4 * signo
            self.point_value = config.VAL_CANGREJO * 8 # cuantos puntos por matarla y por spawnearla
            self.enfado = 2
        self.type = "c"

    def move(self, frame):
        if self.vidas == 1: # que se haga más rapido una vez le das una vez
            sign = 1 if self.last_dx > 0 else -1
            self.last_dx = 2 *(self.enfado+1)* sign
        elif self.vidas == 2:
            sign = 1 if self.last_dx > 0 else -1
            self.last_dx = (self.enfado+1) * sign

        if self.vidas == 0:
            if not self.downed:
                self.frame_stun = frame
                self.downed = True          
                self.last_dx = self.dx
            self.dx = 0
            
            # esta detección de stunneo se podría meter directamente en la clase enemigo ya que es igual para todos, pero bueno...
            if frame - self.frame_stun > 150:  # 5 segundos de delay
                if self.enfado < 2:
                    self.enfado +=1
                self.downed = False
                self.dx = self.last_dx
                self.vidas = self.max_vidas
        else:
            self.dx = self.last_dx
        self.update_pos()

    def animate(self, frame):
        self.sprite[0] = 0
        if self.enfado == 1:
            self.sprite[1] = 152
        elif self.enfado == 2:
            self.sprite[1] = 168
        if not self.downed:
            if self.vidas == 2:
                self.sprite[0] = (((frame // 4) % 2)+1) * 16
            elif self.vidas == 1:
                self.sprite[0] = (((frame // 3) % 2)+4) * 16
        else:
            self.sprite[0] = ((frame // 2) % 2 + 7) * 16

        if self.dx < 0:
            self.sprite[2] = 16
        else:
            self.sprite[2] = -16