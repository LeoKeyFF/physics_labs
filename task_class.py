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
    def __init__(self, number,  name, text, velocity):
        super().__init__()

        self.number = number
        self.name = name
        self.text = text
        self.velocity = velocity
