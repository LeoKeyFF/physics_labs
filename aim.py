from PIL import Image, ImageTk

class Aim:
    def __init__(self,x0, y0, canvas):
        self.x = x0
        self.y = y0
        self.img = None
        self.canvas = canvas
        self.width = 20
        self.height = 50

    def draw(self):
        self.img = ImageTk.PhotoImage(Image.open('images/aim.png'))
        self.canvas.create_image(self.x + self.width/2, self.y, image=self.img)
