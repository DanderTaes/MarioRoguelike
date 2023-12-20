import config
import pyxel

class Character: # propiedades de movimiento de TODOS los personajes
    def __init__(self, x, y, sprite, vidas):
        self.is_grounded = False # tocando el suelo?
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.dir = 1 # 1 positive dx, -1 negative 
        
        # El sprite es una lista [u, v, w, h]
        self.sprite = sprite 

        # gravedad máxima para cada personaje
        self.gravedad_max = 1

        # primer frame donde el personaje es invulnerable
        self.invincibility_frame = 0
        # estado de invulnerabilidad
        self.invincibility = False

        # es el personaje mario?
        self.player = False
        self.max_vidas = vidas
        self.vidas = vidas # en mario son vidas (se resetea el nivel cuando mueres, en los enemigos será cuantas veces hasta stunearlos)
        self.alive = True
        self.tilemap = 0 # cual tilemap elegir (para colisiones)

        # primera frame cuando mueren (para animación de muerte)
        self.death_frame = 0
        # reproduciendo animacion de muerte
        self.dying = False

    ########################################################################
    # COLISIONES

    def collision(self, other): # COLISION ENTRE DOS PERSONAJES (NO TILES)
        # Verificar colision en el eje X
        colision_x = self.x < other.x + abs(other.sprite[2]) and self.x + abs(self.sprite[2]) > other.x
        # Verificar colisión en el eje Y
        colision_y = self.y < other.y + abs(other.sprite[3]) and self.y + abs(self.sprite[3]) > other.y
        # Si hay colisión en ambos ejes, entonces hay colisión
        if colision_x and colision_y:
            return True
        else:
            return False
        
    def collision_character(self, other, frame): # Manejar colisiones entre self (este mismo objeto), y other, otro objeto de esta misma clase
        # si no se está muriendo y han pasasdo 1,5 segs de invincibilidad resetear invincibilidad
        if frame - self.invincibility_frame >= 45 and self.invincibility and self.dying == False:
            self.invincibility = False 

        # Si hay una colision entre dos personajes y niguno tiene invicibilidad
        if self.collision(other) and self.invincibility == False and other.invincibility == False:
            # Si el que detecta colision es el player (mario)
            if self.player:
                # Si el otro personaje no está stunneado (vidas > 0)
                if other.vidas > 0 and other.max_vidas > 0: # max vidas aquí para que no le haga daño la moneda
                    self.vidas -=1
                    # Manejar invinicibilidad
                    self.invincibility = True
                    self.invincibility_frame = frame

                    # cambiar la direccion del otro personaje para evitar dobles colisiones
                    other.last_dx *= -1
                else:
                    # Si el enemigo no está stuneado:
                    if other.max_vidas == 0: # en monedas dejo que se encarge move de cambiar todo (max_vidas == 0 es siempre la moneda)
                        # reproducir sonido de moneda
                        pyxel.play(2, 5, 3, False)
                        other.vidas = 0
                    else:
                        # Matar enemigo (con animación de muerte)
                        other.slow_death_enemy(frame)

            # voltear enemigos de mismo tipo que se encuentran (sólo funciona con enemigos que tengan el type definido, para evitar que pase con bolas de fuego y otros)
            elif self.type != "" and other.type != "": 
                # si son del mismo tipo y no se han encontrado con otro del mismo tipo en 1 seg (para que no se queden atrapados dos colisionando)
                if self.type == other.type and frame - self.turnaround_frame > 30 and self.dx != 0 and other.dx != 0: # solo si se están moviendo
                    if (self.dx/abs(self.dx) != other.dx/abs(other.dx)): # si van en direcciones opuestas
                        self.turnaround_frame = frame # resetear el frame para evitar que vuelvan a darse la vuelta hasta dentro de 30 frames
                        other.last_dx *= -1
                        self.last_dx *= -1

    def detect_collision_tile(self, x, y): # para cualquier personaje con un tile
        # el // 8 es para ajustarse a las coordenadas del tilemap (que una coordenada son 8 pixeles)
        # cogemos las dos esquinas del sprite personaje (x, y) y (x + w, y + h) se le resta uno para cuadrar mejor
        # el abs(w) en la x2 es porque el width puede ser negativo si esta mirando para el otro lado
        x1 = x // 8
        y1 = y // 8
        x2 = (x + abs(self.sprite[2]) - 1) // 8
        y2 = (y + self.sprite[3] - 1) // 8

        # recorremos cada uno de los tiles en los que está este sprite
        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                # vemos que tile hay en cada uno de las coords en las que está el sprite
                tile = pyxel.tilemaps[self.tilemap].pget(xi, yi)
                pow = False
                if self.player:
                    # detectamos si el sprite es el pow y es el jugador el que le da
                    if tile[0] >= 20 and tile[1] >= 2: # estos valores 20 t 2 están cogidos de la .pyxres para que sólo detecte el POW (todos los estados)
                        pow = True
                
                # si el tile no es (0,0) el que hemos considerado como espacio vacío, y no está en el apartado de bloques (v < 7), entonces hay colision con un tile
                if tile != (0,0) and tile[1]<7:
                    # devolvemos True de que hay colision, las coords de la colision (del tilemap) y si es o no el pow el que ha colisionado
                    return True, (xi, yi), pow
                
                # si el tile está entre los sprites de las tuberias y la colision no la hace el player, entonces hacemos que el enemigo vuelva a aparecer por arriba
                # y > 64 para que sólo afecte a las tuberias de abajo
                elif tile in config.PIPES and self.player == False and self.y > 64: 
                    if self.stuneable: # solo algunos enemigos pueden volver a aparecer (los que se pueden matar)
                        self.volver_a_salir()

        return False, (), False
    

    
    ########################################################################
    # Animacion de muerte
    
    def slow_death_enemy(self, frame):
        # en el primer frame de la muerte:
        if self.dying == False:
            pyxel.play(2, 4, 30, False)
            self.death_frame = frame # contamos los frames para la muerte
            self.dying = True
            self.invincibility = True
            self.is_grounded = False # quitamos la colision con el suelo para que caiga como en el original
        else:
            # la animación dura 1 seg
            if frame - self.death_frame > 30:
                self.alive = False

    ########################################################################
    # MOVIMIENTO

    # Esta funcion es la que maneja la transformación de velocidades (dx, dy) a posiciones (x, y) de cada personaje
    def update_pos(self):
        last_y = self.y # ver como cambia la y para saber si está cayendo

        if self.dx == 0 and self.player:
            self.moving = False

        # Caminar infinitamente:
        if int(self.x + self.sprite[3]/2) > config.WIDTH: 
            self.x = -4
        elif int(self.x) < -4: 
            self.x = int(config.WIDTH - self.sprite[3]/2)

        # gravedad
        if self.is_grounded == False:
            self.dy += self.gravedad_max
            if self.dy >= 10: # maxima velocidad
                self.dy = 10

        # actualizar x e y:
        
        abs_dx = abs(self.dx)
        abs_dy = abs(self.dy)
        sign = 1 if self.dx > 0 else -1 # ver si la dx es positiva o negativa

        # actualizar la x pixel a pixel hasta que pase todo dx o haya una colision
        count = 0
        while (count < abs_dx and not self.detect_collision_tile(self.x + sign, self.y)[0]):
            self.x += sign
            count += 1
        else: # un else en un while sólo se ejecuta una vez se ha roto el while (si nunca pasa el while no se ejecuta)
            # si un enemigo choca horizontalmente con un bloque, que cambie su dirección de movimiento
            if self.detect_collision_tile(self.x + sign, self.y)[0] and self.player == False:
                self.last_dx *= -1
                self.dir *= -1
    
        # lo mismo pero con la dy
        sign = 1 if self.dy > 0 else -1
        # COLLISION SUELO (si está cayendo el personaje cuando hay colisión)
        if self.dy > 0: 
            count = 0
            # si hay una colisión para a no ser que se esté muriendo (en ese caso queremos que caiga infinitamente)
            while (count < abs_dy and not self.detect_collision_tile(self.x, self.y + sign)[0]) or (count < abs_dy and self.dying):
                self.y += sign
                count += 1
            else:
                # ya que no hay pow en el suelo, solo usamos la colision True or False
                collision, bloque, pow = self.detect_collision_tile(self.x, self.y + sign)
                if collision:
                    self.is_grounded = True

        # COLISION TECHO (si se está moviendo hacia arriba el personaje)
        elif self.dy < 0:
            count = 0
            while (count < abs_dy and not self.detect_collision_tile(self.x, self.y + sign)[0]):
                self.y += sign
                count += 1
            else:
                collision, bloque, pow = self.detect_collision_tile(self.x, self.y + sign)
                if collision and self.player: # si es el mario el que colisiona con el techo
                    # activar POW
                    if pow:
                        self.pow_activated = True
                    # Cambiar bloques de encima de mario para que se doblen
                    else:
                        self.tile_change(bloque)
                        # Reducir dy ya que ha colisionado con el techo
                        self.dy = int(self.dy*0.3)
        
        # detectar si está en el suelo        
        if self.y < last_y: # si ha bajado en este frame (no está en el suelo)
            self.is_grounded = False
        elif self.y > last_y and self.is_grounded: # si ha subido y estaba en el suelo
            self.is_grounded = False

    
    
    
