import math


class Ballistics:
    g = 9.8
    @staticmethod
    def calc_velocity_y(v0, alpha, t):
        g = Ballistics.g
        return v0 * math.sin(math.pi * alpha / 180) - t * g

    @staticmethod
    def calc_velocity_x(v0, alpha):
        return v0 * math.cos(math.pi * alpha / 180)

    @staticmethod
    def calc_max_aim_y_v0_const(x, v_max, x0, y0):
        g = Ballistics.g
        y = y0 + ((v_max * v_max) / (2 * g)) - ((g * (x - x0) * (x - x0)) / (2 * v_max * v_max))
        return y

    @staticmethod
    def calc_max_aim_y_angle_const(x, v_max, x0, y0, angle):
        g = Ballistics.g
        y = y0 + math.tan(math.pi * angle / 180)*(x - x0) - g*(x-x0)*(x-x0)/(2*math.cos(math.pi * angle / 180)*math.cos(math.pi * angle / 180)*v_max*v_max)
        return y

    @staticmethod
    def calc_cords(t, v0, alpha, x0, y0):
        g = Ballistics.g
        x = x0 +v0 * (math.cos(math.pi * alpha / 180)) * t
        y = y0 +v0 * (math.sin(math.pi * alpha / 180)) * t - ((g * t * t) / 2)
        return x,y
