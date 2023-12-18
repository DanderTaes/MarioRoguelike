import pyxel 
import config 

class Title_screen:
    def __init__(self) -> None:
        pyxel.load("./assets/mario.pyxres")
        self.selected = 0
        self.play = False

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.selected = 0 if self.selected == 1 else 1
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.selected = 0 if self.selected == 1 else 1
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            self.play = True


    def draw(self):
        pyxel.cls(0)

        # Cambia el fondo de pantalla y muestra el título del juego
        #pyxel.blt  # aqui vendrian las imagenes
        pyxel.blt(config.WIDTH/2 - 100, 30, 2, 0, 0, 200, 72, 1)

        if self.selected == 0:
            if pyxel.frame_count % 15 in (range(int(15 / 2))):
                text = "PLAY DEMO"
                pyxel.text(config.WIDTH / 2 - len(text) * 4 / 2, config.HEIGHT *  9/ 14, text, 7)
            text = "PLAY ROGUELIKE"
            pyxel.text(config.WIDTH / 2 - len(text) * 4 / 2, config.HEIGHT * 11/ 14, text, 13)
        
        else:
            text = "PLAY DEMO"
            pyxel.text(config.WIDTH / 2 - len(text) * 4 / 2, config.HEIGHT *  9/ 14, text, 13)
            if pyxel.frame_count % 15 in (range(int(15 / 2))):
                text = "PLAY ROGUELIKE"
                pyxel.text(config.WIDTH / 2 - len(text) * 4 / 2, config.HEIGHT * 11/ 14, text, 7)
