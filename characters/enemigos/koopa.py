import config
from characters.enemigo import Enemigo


class Koopa(Enemigo):
    def __init__(self, x, y, mode=0):
        super().__init__(x, y, [16, 72, 12, 16], vidas=1)
        if self.x > config.WIDTH/2:
            self.dx = -1
        else:
            self.dx = 1
        self.last_dx = self.dx
        self.point_value = config.VAL_KOOPA # cuantos puntos por matarla
        if mode == 1:
            signo = 1 if self.last_dx > 0 else -1
            self.last_dx = 2 * signo
            self.point_value = config.VAL_KOOPA * 4 # cuantos puntos por matarla
            self.enfado = 1
        
        self.type = "k"

    def move(self, frame):

        if self.dying == False:
            if self.vidas == 0:
                if not self.downed:
                    # primer frame del stunneo
                    self.frame_stun = frame
                    self.downed = True          
                    self.last_dx = self.dx
        
                self.dx = 0
                if frame - self.frame_stun > 150: # 5 segundos de delay
                    self.enfado = 1
                    self.downed = False
                    self.dx = self.last_dx
            
                    self.vidas = self.max_vidas
            else:
                sign = 1 if self.last_dx > 0 else -1
                self.last_dx = (self.enfado+1) * sign
                self.dx = self.last_dx
        
        self.update_pos()
       

    def animate(self, frame):
        if self.enfado != 0:
            self.sprite[1] = 88
        else:
            self.sprite[1] = 72
        self.sprite[0] = 16 # koopa parado
        if not self.downed:
            self.sprite[0] = (((frame//2)%3))*16
        else:
            self.sprite[0] = ((frame//2)%2 + 3)*16
                
        if self.dx <= 0:  
            self.sprite[2] = 16 # invertir sprite
        else: 
            self.sprite[2] = -16
    