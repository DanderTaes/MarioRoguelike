import pyxel
import config
from pantallas.end import End
from pantallas.game import Game
from pantallas.titlescreen import Title_screen



class Board:
    def __init__(self):
        # Se inicializan el juego como tal y se pone la pantalla como title_screen()
        pyxel.init(config.WIDTH, config.HEIGHT, title="MARIO NES")
        self.titlescreen = Title_screen()
        self.screen = self.titlescreen

        # Al principio no hay juego como tal, esperamos a elegir modo de juego
        self.game = None

        # Variable para detectar cuando morimos o ha terminado el juego en si
        self.ended = False

        # Reproducimos música creada en el .pyxres e iniciamos el run (el loop principal)
        pyxel.playm(0, 30, True)
        pyxel.run(self.update, self.draw)
      
    def update(self):
        # detectamos si se ha cambiado la pantalla
        self.__screen_change()

        # hacemos update en la pantalla que está activa
        self.screen.update()

    def draw(self):
        # hacemos draw en la pantalla que está activa
        self.screen.draw()
        

    def __screen_change(self):

        # Comenzar a jugar cuando el jugador esta en la pantalla de inicio (Titlescreen()) y presiona el espacio
        if self.screen == self.titlescreen and self.titlescreen.play:
            # Cambiar la pantalla actual a la del juego (Game()) y e juega el modo de juego seleccionados
            self.game = Game(self.titlescreen.selected)

            # cambiamos la pantalla a la del juego y quitamos la activación del juego por si volvemos a poner la titlescreen más tarde
            self.screen = self.game
            self.titlescreen.play = False
        

        # Mario ha muerto
        elif self.screen == self.game and (self.game.player.alive == False):
            # Abre el archivo "topscores.txt" con el modo append y guarda la puntuación del jugador actual
            topscores = open("topscores.txt", "a")
            topscores.write(f"\n{self.game.score}")
            topscores.close()

            # Envia a la pantalla final (End()) con el score actual 
            self.ended = True
            self.screen = End(self.game.score)

        
        
        # Reiniciar partida tras haber sido derrotado
        elif self.ended and pyxel.btn(pyxel.KEY_R):
            # Cambiar la pantalla a la pantalla de inicial (Title screen) y reiniciamos todas las variables del board
            self.ended = False
            self.game = None
            self.screen = self.titlescreen
            
        # Cerrar el juego tras haber sido derrotado
        elif self.ended and pyxel.btn(pyxel.KEY_Q):
            quit()