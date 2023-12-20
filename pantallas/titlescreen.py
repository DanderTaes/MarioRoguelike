import pyxel 
import config 

class Title_screen:
    def __init__(self) -> None:
        pyxel.load("./assets/mario.pyxres")
        # gamemode seleccionado (por defecto el 0) 0 es demo y 1 es roguelike
        self.selected = 0
        self.play = False

    def update(self): # cambiar entre modos y selecionar cuando play sea True
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.selected = 0 if self.selected == 1 else 1
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.selected = 0 if self.selected == 1 else 1
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            self.play = True


    def draw(self):
        pyxel.cls(0)
        # Cambia el fondo de pantalla y muestra el título del juego
        pyxel.blt(config.WIDTH/2 - 100, 30, 2, 0, 0, 200, 72, 1)

        if self.selected == 0:
            if pyxel.frame_count % 15 in (range(int(15 / 2))): # que parpadee el texto
                text = "PLAY DEMO"
                pyxel.text(config.WIDTH / 2 - len(text) * 4 / 2, config.HEIGHT *  9/ 14, text, 7)
            text = "PLAY ROGUELIKE"
            pyxel.text(config.WIDTH / 2 - len(text) * 4 / 2, config.HEIGHT * 11/ 14, text, 13)
        
        else:
            text = "PLAY DEMO"
            pyxel.text(config.WIDTH / 2 - len(text) * 4 / 2, config.HEIGHT *  9/ 14, text, 13)
            if pyxel.frame_count % 15 in (range(int(15 / 2))): # que parpadee el texto
                text = "PLAY ROGUELIKE"
                pyxel.text(config.WIDTH / 2 - len(text) * 4 / 2, config.HEIGHT * 11/ 14, text, 7)
