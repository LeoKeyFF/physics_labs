import math


class Ballistics:
    g = 9.8
    @staticmethod
    def calc_velocity(v0, alpha, t):
        g = Ballistics.g
        return v0 * math.sin(math.pi * alpha / 180) - t * g

    @staticmethod
    def calc_max_aim_y(x, v_max):
        g = Ballistics.g
        y = ((v_max * v_max) / (2 * g)) - ((g * x * x) / (2 * v_max * v_max))
        return y

    @staticmethod
    def calc_cords(t, v0, alpha):
        g = Ballistics.g
        x = v0 * (math.cos(math.pi * alpha / 180)) * t
        y = v0 * (math.sin(math.pi * alpha / 180)) * t - ((g * t * t) / 2)
        return x,y
