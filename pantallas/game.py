import pyxel
from characters.player import Player
import config
from nivel import Nivel
import mando


class Game:
    def __init__(self, gamemode=0):
        # cargamos assets
        pyxel.load("assets/mario.pyxres")
        self.gamemode = gamemode
        self.score = 0
        # creamos al player, a la lista de personajes y enemigos
        self.player = Player(30,179)
        self.enemies = []
        self.characters = []
        self.characters.append(self.player)

        self.nivel_num = 5 # en el modo demo empezamos en el nivel 1
        self.nivel = Nivel(self.nivel_num, pyxel.frame_count, self.gamemode)
        # cambiamos el tilemap con respecto al nivel
        self.tilemap = self.nivel.tilemap

        try: # normalmente no usaría try pero en esta librería es necesario (la del mando)
            self.mando = mando.XInput()
        except Exception:
            self.mando = None
            print("mando no conectado")
    

    def update(self):

        # CAMBIAR NIVEL
        # si el frame es mayor que el ultimo frame donde se spawnean enemigos y está todos muertos se pasa de nivel
        if self.nivel.last_frame < pyxel.frame_count and len(self.characters) <= 1:
            self.player.x, self.player.y = (30,179) # resetear al mario
            self.nivel_num +=1
            # cambiar nivel (cada nivel es un nuevo objeto)
            self.nivel = Nivel(self.nivel_num, pyxel.frame_count, self.gamemode)
            # sonido de cambio de nivel 
            pyxel.play(1, 0, 30, False)
            self.tilemap = self.nivel.tilemap
            if self.nivel.gaming == False: # si se han acabado los niveles de la demo, matar al mario para terminar
                self.player.alive = False

        # Detección de mando:
        if self.mando is not None:
            try:
                self.mando.run()
            except Exception as e:
                self.mando = None # si no hay mando, no intentar de nuevo conectarse (evitar lag)
                print(e)
        
        # SPAWN ENEMIES:
        enemies = []
        if self.nivel.gaming:
            enemies = self.nivel.spawn(pyxel.frame_count)
        if len(enemies) > 0:
            # meter a los nuevos enemigos en las listas correspondientes para detecciones
            self.characters.extend(enemies)
            self.enemies.extend(enemies)

        # MARIO:
        # al usar mouvement como una lista aquí nos permite presionar dos teclas a la vez y que funcione (saltar y moverte a la vez)
        mouvement = []
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            mouvement.append('l')
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            mouvement.append('r')            
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_SPACE)):
            mouvement.append('u')
        self.player.move(mouvement, pyxel.frame_count)


        # colisiones
        # Iteramos entre todos los personajes de 2 en 2
        for i, personaje in enumerate(self.characters):
            if personaje.dying: # si está muriendo que baje pa abajo
                personaje.slow_death_enemy(pyxel.frame_count)
            personaje.tilemap = self.tilemap # actualizar tilemap de cada personaje

            for other in self.characters[i + 1 :]: # lista del resto de personajes para hacer colisiones 2 a 2
                personaje.collision_character(other, pyxel.frame_count) # comprobar colisiones entre los 2
                if other.alive == False: # una vez muere un personaje, añadir a la puntuación y quitar enemigo
                    self.score += other.point_value
                    self.characters.remove(other) # quitar colisiones de los muertos


        # UPDATE ENEMIES:
        # comprobar si hay bloques doblados (para stunear)
        bloques_stunned = self.player.get_bloques()
        for enemy in self.enemies:
            # mover a todos los enemigos
            enemy.move(pyxel.frame_count)
            if len(bloques_stunned)>0: # si hay bloques doblados mirar colision de stunnear
                enemy.stun_detect(bloques_stunned, pyxel.frame_count)
            # POW (con delay de 1 seg antes de activarse otra vez)
            elif self.player.pow_activated and (pyxel.frame_count - self.player.pow_cooldown_frame) > 30: 
                enemy.stun_detect((), pyxel.frame_count, pow=True)
        
        # desactivar pow una vez stunnea a enemigos
        if self.player.pow_activated:
            self.player.pow_activated = False
            if (pyxel.frame_count - self.player.pow_cooldown_frame) > 30: 
                self.player.pow_cooldown_frame = pyxel.frame_count
                self.player.pow_level -= 1
        
        # TECLA MÁGICA PARA MATAR A MARIO (para debuggear)
        if pyxel.btn(pyxel.KEY_E): 
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

        # CAMBIO NIVEL (si hay texto que aparezca)
        texto = self.nivel.text(pyxel.frame_count)
        if texto != "":
            pyxel.text(config.WIDTH / 2 - len(texto) * 4 / 2, config.HEIGHT/2+10, texto, 7)

    