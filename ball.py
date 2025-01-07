import math
from PIL import Image, ImageTk

class Ball:
    def __init__(self,x0, y0, canvas):
        pass
        self.x = x0
        self.y = y0
        self.canvas = canvas
        self.body = None
        self.alpha = 45
        self.x0 = x0
        self.y0 = y0
        self.img = None

        self.V0 = 20
        self.Vmax = 25
        self.size = 20

    def draw(self):
        if self.body:
            self.canvas.delete(self.body)
        x, y = self.x, self.y
        self.img = ImageTk.PhotoImage(Image.open('images/желез_шар20x20.png'))
        self.body = self.canvas.create_image(x + 10, y - 10, image=self.img)


    def move(self, x, y):
        self.x = x
        self.y = y
        self.draw()

    def calc_cords(self, t):
        g = 9.8
        x = self.V0 * (math.cos(math.pi * self.alpha / 180)) * t
        y = self.V0 * (math.sin(math.pi * self.alpha / 180)) * t - ((g * t * t) / 2)
        return x,y