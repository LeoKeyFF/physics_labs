from PIL import Image, ImageTk

class Aim:
    def __init__(self,x0, y0, canvas):
        self.x = x0
        self.y = y0
        self.img = None
        self.canvas = canvas

    def draw(self):
        self.img = ImageTk.PhotoImage(Image.open('images/aim.png'))
        self.canvas.create_image(self.x + 10, self.y - 50+25, image=self.img)
