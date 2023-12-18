import config
import pyxel

class Character: # propiedades de movimiento de TODOS los personajes
    def __init__(self, x, y, sprite, vidas):
        self.is_grounded = False
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.dir = 1 # 1 positive dx, -1 negative 
        self.moving = False
        self.sprite = sprite
        self.gravedad_max = 1
        self.invincibility_frame = 0
        self.invincibility = False

        self.player = False
        self.max_vidas = vidas
        self.vidas = vidas # en mario son vidas (se resetea el nivel cuando mueres, en los enemigos será cuantas veces hasta stunearlos)
        self.alive = True
        self.tilemap = 0 # cual tilemap elegir
        self.death_frame = 0
        self.dying = False

    ########################################################################
    # COLISIONES

    def collision(self, other):
        # Este es la funcion madre por decirlo de alguna manera que te dice cunado uno y otro estan en la msima posicion
        colision_x = self.x < other.x + abs(other.sprite[2]) and self.x + abs(self.sprite[2]) > other.x
        # Verificar colisión en el eje Y
        colision_y = self.y < other.y + abs(other.sprite[3]) and self.y + abs(self.sprite[3]) > other.y
        # Si hay colisión en ambos ejes, entonces hay colisión
        if colision_x and colision_y:
            return True
        else:
            return False
        
    def collision_character(self, other, frame):
        # si no se está muriendo resetear invincibilidad
        if frame - self.invincibility_frame >= 45 and self.invincibility and self.dying == False:
            self.invincibility = False 
        if self.collision(other) and self.invincibility == False and other.invincibility == False:
            if self.player:
                if other.vidas > 0 and other.max_vidas > 0: # max vidas aquí para que no le haga daño la moneda
                    self.vidas -=1
                    self.invincibility = True
                    self.invincibility_frame = frame
                    other.last_dx *= -1
                else:
                    if other.max_vidas == 0: # en monedas dejo que se encarge move de cambiar todo
                        pyxel.play(2, 5, 3, False)
                        other.vidas = 0
                    else:
                        other.slow_death_enemy(frame)
            elif self.type != "" and other.type != "": # voltear enemigos de mismo tipo que se encuentran
                if self.type == other.type and frame - self.turnaround_frame > 30 and self.dx != 0 and other.dx != 0: # solo si van en direcciones opuestas
                    if (self.dx/abs(self.dx) != other.dx/abs(other.dx)):
                        self.turnaround_frame = frame
                        other.last_dx *= -1
                        self.last_dx *= -1

    def detect_collision_tile(self, x, y): # para cualquier objeto
        x1 = x // 8
        y1 = y // 8
        x2 = (x + abs(self.sprite[2]) - 1) // 8
        y2 = (y + self.sprite[3] - 1) // 8
        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                tile = pyxel.tilemaps[self.tilemap].pget(xi, yi)
                pow = False
                if self.player:
                    if tile[0] >= 20 and tile[1] >= 2:
                        pow = True
                if tile != (0,0) and tile[1]<7:
                    return True, (xi, yi), pow
                elif tile in config.PIPES and self.player == False and self.y > 64:
                    if self.stuneable:
                        self.volver_a_salir()
        return False, (), False
    

    
    ########################################################################
    # Animaciones
    
    def slow_death_enemy(self, frame):
        if self.dying == False:
            pyxel.play(2, 4, 30, False)
            self.death_frame = frame
            self.dying = True
            self.invincibility = True
            self.is_grounded = False
        else:
            if frame - self.death_frame > 30:
                self.alive = False

    ########################################################################
    # MOVIMIENTO

    def update_pos(self, last_y):
        abs_dx = abs(self.dx)
        abs_dy = abs(self.dy)
        sign = 1 if self.dx > 0 else -1

        count = 0
        while (count < abs_dx and not self.detect_collision_tile(self.x + sign, self.y)[0]):
            self.x += sign
            count += 1
        else:
            if self.detect_collision_tile(self.x + sign, self.y)[0] and self.player == False:
                self.last_dx *= -1
                self.dir *= -1
    
        sign = 1 if self.dy > 0 else -1
        # COLLISION SUELO
        if self.dy > 0:
            count = 0
            while (count < abs_dy and not self.detect_collision_tile(self.x, self.y + sign)[0]) or (count < abs_dy and self.dying):
                self.y += sign
                count += 1
            else:
                collision, bloque, pow = self.detect_collision_tile(self.x, self.y + sign)
                if collision:
                    if self.is_grounded is not None:
                        self.is_grounded = True

        # COLISION TECHO
        elif self.dy < 0:
            count = 0
            while (count < abs_dy and not self.detect_collision_tile(self.x, self.y + sign)[0]):
                collision, bloque, pow = self.detect_collision_tile(self.x, self.y + sign)
                self.y += sign
                count += 1
            else:
                collision, bloque, pow = self.detect_collision_tile(self.x, self.y + sign)
                if collision and self.player:
                    if pow:
                        self.pow_activated = True
                    else:
                        self.tile_change(bloque)
                        self.dy = int(self.dy*0.3)
        
        if self.y < last_y:
            self.is_grounded = False
        elif self.y > last_y and self.is_grounded:
            self.is_grounded = False

    def gravity(self):
        last_y = self.y # ver como cambia la y para saber si está cayendo
        if self.dx == 0:
            self.moving = False

        # Caminar infinitamente:
        if int(self.x + self.sprite[3]/2) > config.WIDTH: 
            self.x = -4
        elif int(self.x) < -4: 
            self.x = int(config.WIDTH - self.sprite[3]/2)


        if self.is_grounded == False:
            self.dy += self.gravedad_max
            if self.dy >= 10: # maxima velocidad
                self.dy = 10
        return last_y


    
    
    
