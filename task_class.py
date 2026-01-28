class TaskBall:
    def __init__(self, number,  name, text, velocity, angle, x0, y0, Vmax, meter):
        super().__init__()

        self.number = number
        self.name = name
        self.text = text
        self.velocity = velocity
        self.angle = angle
        self.x0 = x0
        self.y0 = y0
        self.Vmax = Vmax
        self.meter = meter

class TaskGravity:
    def __init__(self, number,  name, text1, text2, text3):
        super().__init__()

        self.number = number
        self.name = name
        self.velocity = None
        self.radius = None
        self.mass_big = None
        self.text1 = text1
        self.text2 = text2
        self.text3 = text3
