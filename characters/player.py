import config
from character import Character
import pyxel


class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, [0, 0, 16, 21], vidas=3)
        # es el player
        self.player = True
        self.moving = False

        # manager del pow
        self.pow_cooldown_frame = 0
        self.pow_level = 3
        self.pow_activated = False

        # qué tiles están siendo stunneadas (y qué tile eran originalmente)
        self.original_tiles = [] 
    
    ########################################################################
    # DOBLAR TILES:

    def tile_change(self, bloque: list):
        tiles = []
        if len(self.original_tiles) > 0:
            for value in self.original_tiles:
                if bloque == value[0] or bloque[0]+1 == value[0][0]: # evitar dar a un bloque que todavía está doblado
                    return
        
        # tiles es una lista que contiene:
        # tiles[0] --> las coords del bloque donde se ha dado
        # y el resto son los bloque originales que se van a cambiar a doblados
        tiles.append(bloque) 
        tiles.append(pyxel.tilemaps[self.tilemap].pget(bloque[0], bloque[1])) # (bloque[0]+1, bloque[1]) Es la coordenada del bloque que va a hacer daño a los enemigos)
        tiles.append(pyxel.tilemaps[self.tilemap].pget(bloque[0]+1, bloque[1]))
        tiles.append(pyxel.tilemaps[self.tilemap].pget(bloque[0], bloque[1]-1))
        tiles.append(pyxel.tilemaps[self.tilemap].pget(bloque[0]+1, bloque[1]-1))

        # original tiles es una lista por si acaso hay multiples doblados a la vez aunque no debería ocurrir por el delay
        self.original_tiles.append(tiles)

        # usar los bloques correctos doblados para cada bloque normal
        color = config.AMARILLOS # en caso de que no haya versión doblada de algún bloque, el default son los amarillos
        if tiles[1][1] == 2:
            if tiles[1][0] < 10:
                color = config.AMARILLOS
            else:
                color = config.AZULES
        elif tiles[1][1] == 0:
            if tiles[1][0] < 8:
                color = config.LADRILLO_AZUL
            elif tiles[1][0] < 16:
                color = config.PLAT_AMARILLA
            elif 17 < tiles[1][0]:
                color = config.LADRILLO_ROJO
        
        # cambiar los 4 bloques anteriormente mencionados por la versión doblada del mismo tipo
        pyxel.tilemaps[self.tilemap].pset(bloque[0], bloque[1], color[0]) # (bloque[0]+1, bloque[1]) Es la coordenada del bloque que va a hacer daño a los enemigos)
        pyxel.tilemaps[self.tilemap].pset(bloque[0]+1, bloque[1], color[1])
        pyxel.tilemaps[self.tilemap].pset(bloque[0], bloque[1]-1, color[2])
        pyxel.tilemaps[self.tilemap].pset(bloque[0]+1, bloque[1]-1, color[3])
    
    def tile_reset(self):
        # volver a poner los tiles como estaban y vaciar original_tiles
        if len(self.original_tiles) > 0:
            for tiles in self.original_tiles:
                pyxel.tilemaps[self.tilemap].pset(tiles[0][0], tiles[0][1], tiles[1])
                pyxel.tilemaps[self.tilemap].pset(tiles[0][0]+1, tiles[0][1], tiles[2])
                pyxel.tilemaps[self.tilemap].pset(tiles[0][0], tiles[0][1]-1, tiles[3])
                pyxel.tilemaps[self.tilemap].pset(tiles[0][0]+1, tiles[0][1]-1, tiles[4])
                self.original_tiles.remove(tiles)
    
    def get_bloques(self): # getter de los bloques stunneados
        return self.original_tiles


    ########################################################################
    # ENSEÑAR POW:
    
    def show_pow(self, frame):
        pow_pos = [(15,20), (16,20), (15,21), (16, 21)]
        y = ((frame//9 %2)+1) * 2 # alternar color del pow

        fase = (3- self.pow_level) * 2
        if self.pow_level > 0: # cambiar fase del pow
            pyxel.tilemaps[self.tilemap].pset(*pow_pos[0], (20+fase,y))
            pyxel.tilemaps[self.tilemap].pset(*pow_pos[1], (21+fase,y))
            pyxel.tilemaps[self.tilemap].pset(*pow_pos[2], (20+fase,y+1))
            pyxel.tilemaps[self.tilemap].pset(*pow_pos[3], (21+fase,y+1))
        else:
            pyxel.tilemaps[self.tilemap].pset(*pow_pos[0], (0,0))
            pyxel.tilemaps[self.tilemap].pset(*pow_pos[1], (0,0))
            pyxel.tilemaps[self.tilemap].pset(*pow_pos[2], (0,0))
            pyxel.tilemaps[self.tilemap].pset(*pow_pos[3], (0,0))

    ########################################################################
    # MANEJAR MARIO:

    def move(self, inputs: list, frame):
        self.tile_reset() # resetear tiles cada frame
        # manejar inputs
        for input in inputs:
            if input == 'l':
                self.dx = -2
                self.dir = -1
                self.moving = True
            elif input == 'r':
                self.dx = 2
                self.dir = +1
                self.moving = True
            elif input == 'u' and self.is_grounded:
                self.dy = -10
        self.update_pos()
        self.dx = int(self.dx*0.2) # fricción del suelo
        if self.vidas == 0:
            self.slow_death_enemy(frame)
            self.vidas = -1
        

    
    def animate(self, frame):
        self.show_pow(frame)

        if self.dying:
            self.sprite[1] = 48
            self.sprite[0] = 16
        
        # no conseguí alguna forma de hacer más notable la invincibilidad cuando te hacen daño, pero se cambiaría aquí
        elif self.invincibility:
            self.sprite[1] = 48
            self.sprite[0] = 0
        else:
            self.sprite[1] = 0
            self.sprite[0] = 0 # mario parado
            if self.is_grounded == False:
                self.sprite[0] = 64
            elif self.moving:
                self.sprite[0] = (((frame//2)%3 )+1)*16
        if self.dir > 0:  self.sprite[2] = 16 # invertir sprite
        else: self.sprite[2] = -16

    
    