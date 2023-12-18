import pyxel 
import config 

def filetolist(file):
    """
    Dado un archivo, devuelve una lista con las líneas de este.
    """
    f = open(file, "r")

    list1 = []

    for line in f:
        line = line.strip("\n")
        if line != "":
            list1.append(int(line))

    return list1

class End:
    def __init__(self, score):
        self.scores = sorted(filetolist("topscores.txt"), reverse=True)  # Lista con todos los resultado en topscores.txt
        self.score = score

    # Creo que aqui tendriamos que poner las imagenes y asociarlas


    def update(self):
        pass
        # creo que no hay que poner anda pero la pongo por si acaso


    def draw(self):
        # Cambia el fondo a color negro e imprime el mensaje (VICTORY / DEFEAT)
        pyxel.cls(0)
        #pyxel.blt - aquitambienirianlasimagenescreo

        # Imprime todo el texto de la pantalla centrado en la pantalla, excepto los TOP SCORES, que se imprimen más abajo
        texts = ("YOUR SCORE: ", str(self.score), "TOP SCORES:", "Press 'R' to play again", "Press 'Q' to quit game")
        ypositions = (config.HEIGHT * 1 / 2 - 55, config.HEIGHT * 1 / 2 - 43, config.HEIGHT * 3 / 5 - 50, config.HEIGHT * 7 / 8 - 35,
                    config.HEIGHT * 7 / 8 - 25)
        for text, yposition in zip(texts, ypositions):
            color = lambda text: pyxel.frame_count % 15 + 1 if (text == str(
                self.score)) else 10  # Si lo que se imprime es la puntación del usuario, hacer que cambie de color entre todos los colores menos el negro
            pyxel.text(config.WIDTH / 2 - len(str(text)) * 4 / 2, yposition, text, color(text))

        # Imprime los TOP SCORES
        x = 0
        for i in range(min(5, len(self.scores))):
            text = f"{i + 1}. {self.scores[i]}"
            pyxel.text(config.WIDTH / 2 - len(text) * 4 / 2, config.HEIGHT * 3 / 5 - 40 + x, text, 10)
            x += 10

