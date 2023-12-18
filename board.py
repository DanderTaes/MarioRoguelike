import pyxel
import config
from pantallas.end import End
from pantallas.game import Game
from pantallas.titlescreen import Title_screen



class Board:
    def __init__(self):
        pyxel.init(config.WIDTH, config.HEIGHT, title="MARIO NES")
        self.titlescreen = Title_screen()
        self.game = None
        self.screen = self.titlescreen
        self.ended = False
        pyxel.playm(0, 30, True)
        pyxel.run(self.update, self.draw)
      
    def update(self):
        self.__screen_change()
        self.screen.update()

    def draw(self):
        self.screen.draw()
        

    def __screen_change(self):

        # Comenzar a jugar cuando el jugador esta en la pantalla de inicio (Titlescreen()) y presiona el espacio
        if self.screen == self.titlescreen and self.titlescreen.play:
            # Cambiar la pantalla actual a la del juego (Game())
            self.game = Game(self.titlescreen.selected)
            self.screen = self.game
            self.titlescreen.play = False
        
        # Mario ha muerto
        elif self.screen == self.game and (self.game.player.alive == False):
            # Abre el archivo "topscores.txt" con el modo append y guarda la puntuación del jugador actual
            topscores = open("topscores.txt", "a")
            topscores.write(f"\n{self.game.score}")
            topscores.close()

            # Eviar a la pantalla final (End()) el mensaje de victoria/derrota dependiendo del resulado de la partida
            self.ended = True
            self.screen = End(self.game.score)

        
        
        # Reiniciar partida tras haber sido derrotado
        elif self.ended and pyxel.btn(pyxel.KEY_R):
            # Cambiar la pantalla a la pantalla de juego (Title screen)
            self.ended = False
            self.game = None
            self.screen = self.titlescreen
            
        # # Cerrar el juego tras haber sido derrotado
        elif self.ended and pyxel.btn(pyxel.KEY_Q):
            quit()