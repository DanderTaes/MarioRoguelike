import pyxel
from characters.player import Player
import config
from nivel import Nivel
from pantallas.end import End
from pantallas.titlescreen import Title_screen
import mando


class Game:
    def __init__(self, gamemode=0):
        pyxel.load("assets/mario.pyxres")
        self.gamemode = gamemode
        self.score = 0
        self.player = Player(30,179)
        self.enemies = []
        self.characters = []
        self.characters.append(self.player)
        self.tilemap = 0
        self.nivel_num = 1
        self.nivel = Nivel(self.nivel_num, pyxel.frame_count, self.gamemode)
        self.tilemap = self.nivel.tilemap
        try: # normalmente no usaría try pero en esta librería es necesario (la del mando)
            self.mando = mando.XInput()
        except Exception:
            self.mando = None
            print("mando no conectado")
    

    def update(self):

        # CAMBIAR NIVEL
        if self.nivel.last_frame < pyxel.frame_count and len(self.characters) <= 1:
            self.player.x, self.player.y = (30,179) # resetear al mario
            self.nivel_num +=1
            self.nivel = Nivel(self.nivel_num, pyxel.frame_count, self.gamemode)
            pyxel.play(1, 0, 30, False)
            self.tilemap = self.nivel.tilemap
            if self.nivel.gaming == False:
                self.player.alive = False

        # Detección de mando:
        if self.mando is not None:
            try:
                self.mando.run()
            except Exception as e:
                self.mando = None
                print(e)
        
        # SPAWN ENEMIES:
        enemies = []
        if self.nivel.gaming:
            enemies = self.nivel.spawn(pyxel.frame_count)
        if len(enemies) > 0:
            self.characters.extend(enemies)
            self.enemies.extend(enemies)

        # MARIO:
        mouvement = []
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            mouvement.append('l')
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            mouvement.append('r')            
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_SPACE)):
            mouvement.append('u')
        self.player.move(mouvement, pyxel.frame_count)


        # colisiones
        for i, personaje in enumerate(self.characters):
            if personaje.dying: # si está muriendo que baje pa abajo
                personaje.slow_death_enemy(pyxel.frame_count)
            personaje.tilemap = self.tilemap # actualizar tilemap

            for other in self.characters[i + 1 :]:
                personaje.collision_character(other, pyxel.frame_count)
                if other.alive == False:
                    self.score += other.point_value
                    self.characters.remove(other) # quitar colisiones de los muertos


        # UPDATE ENEMIES:
        bloques_stunned = self.player.get_bloques()
        for enemy in self.enemies:
            enemy.move(pyxel.frame_count)
            if len(bloques_stunned)>0:
                enemy.stun_detect(bloques_stunned, pyxel.frame_count)
            # POW
            elif self.player.pow_activated and (pyxel.frame_count - self.player.pow_cooldown_frame) > 30: 
                enemy.stun_detect((), pyxel.frame_count, pow=True)
        if self.player.pow_activated:
            self.player.pow_activated = False
            if (pyxel.frame_count - self.player.pow_cooldown_frame) > 30: 
                self.player.pow_cooldown_frame = pyxel.frame_count
                self.player.pow_level -= 1
        
        if pyxel.btn(pyxel.KEY_E): # DEBUGGER
            self.player.vidas = 0
        
    
    def draw(self):
        pyxel.cls(0)

        # score
        pyxel.text(config.WIDTH/2, 7, f"SCORE: {self.score}", 7)
        vidas = self.player.vidas if self.player.vidas > 0 else 0
        pyxel.text(config.WIDTH/2-30 , 7, f"x{vidas}", 7)
        pyxel.blt(config.WIDTH/2-40 , 7, 0, 112, 2, 8, 6, 8)

        # TILES
        pyxel.bltm(0, 0, self.tilemap, 0, 0, config.WIDTH, config.HEIGHT, 2)

        # Enemigos
        for enemy in self.enemies:
            if enemy.alive == False:
                self.enemies.remove(enemy) # quitar draw de los muertos
                continue
            enemy.animate(pyxel.frame_count)
            pyxel.blt(enemy.x, enemy.y, 0, *enemy.sprite, 8)

        # MARIO
        self.player.animate(pyxel.frame_count)
        pyxel.blt(self.player.x, self.player.y, 0, *self.player.sprite, 8)

        # FASE
        texto = self.nivel.text(pyxel.frame_count)
        if texto != "":
            pyxel.text(config.WIDTH / 2 - len(texto) * 4 / 2, config.HEIGHT/2+10, texto, 7)

    