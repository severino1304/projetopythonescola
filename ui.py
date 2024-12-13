import utils
import globals

class ButtonUI:
    def __init__(self, keyCode, text, x, y):
        self.keyCode = keyCode
        self.text = text
        self.x = x
        self.y = y
        self.pressed = False
        self.on = False
        self.timer = 20
    def update(self, InputStream):
        self.pressed = InputStream.keyboard.isKeyPressed(self.keyCode)
        if self.pressed:
            self.on = True
        if self.on:
            self.timer -= 1
            if self.timer <= 0:
                self.on = False
                self.timer = 20
    def draw(self, screen, alpha=255):
        if self.on:
            cor = globals.VERDE
        else:
            cor = globals.BRANCO
        utils.drawText(screen, self.text, self.x, self.y, cor, 255)