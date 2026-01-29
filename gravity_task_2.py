import pygame
import math
import random

# from grvt01 import velocity

MassBig1 = 1e32 # Это вводят!!!!!!!!! формула правильного MassBig1 это [4*pi**2*Radius**3/(G*T**2)]

res = 0 # Переменная res - показывает результат, она используется в самом низу и перед классом тел для демонстрации результата юзеру

# Используем: период(T) от 2.8e8*pi до 2.2e9*pi
#             радиус(Radius) от 1.1e12 до 4.4e12
#             Рассчитываем массу большого тела(MassBig) по формуле MassBig=4*pi**2*Radius**3/(G*T**2)
# В условие пишем: Спутник на орбите радиуса Radius делает полный оборот за период T. Найти массу MassBig1 тела вокруг которого летает спутник
# Чуть ниже будет всё связанное со всеми опрерируемыми значениями
#
# Красное тело в классе Body1 это тело которое симулируется исходя из введённого значения массы
# Синее тело в классе Body это тело которое должно получится
#
# Проверку можно прикрутить самому, я предлагаю на полный бал - погрешность меньше 0.5%, неполный бал - погрешность не больше 3-5%

pygame.init()
WIDTH, HEIGHT = 800, 600
telo_size = 25

win = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity task №2")
clock = pygame.time.Clock()

G = 6.67430e-11  # Vonyuchaya constanta
SCALE = 6e-11
DT = 2000000
pi = 3.141592653589793

BG = pygame.transform.scale(pygame.image.load("images/Night_sky1_grid1_wip.jpg").convert(), (WIDTH, HEIGHT))
telo = pygame.transform.scale(pygame.image.load("images/Planet_base_n1.png"), (telo_size * 2, telo_size * 2))
kruto = pygame.transform.scale(pygame.image.load("images/OK800x600.png"), (WIDTH, HEIGHT) )
nekruto = pygame.transform.scale(pygame.image.load("images/FALSE800x600.png"), (WIDTH, HEIGHT))


zoomed = False

show_overlay_image = False


# =============================#
T = random.uniform(2.8e8*pi, 2.2e9*pi)
Radius = random.uniform(1.1e12, 4.4e12)
MassSmall = 1.024e26
velocity = 2*pi*Radius/T

MassBig = 4*pi**2*Radius**3/(G*T**2)

Radius1 = Radius
MassSmall1 = MassSmall
velocity1 = velocity #*math.sqrt(MassBig1/MassBig)
# =============================#


def showres():
    if res == 0:
        win.blit(nekruto, (0, 0))
    elif res == 1:
        win.blit(kruto, (0, 0))
    elif res == 2:
        win.blit(kruto, (0, 0))


class Body:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail = []

    def update_position(self, bodies):
        fx = fy = 0
        for other in bodies:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                r = math.sqrt(dx * dx + dy * dy)
                if r > 0:
                    # Formula: F = G * (m1 * m2) / r^2
                    f = G * self.mass * other.mass / (r * r)
                    fx += f * dx / r
                    fy += f * dy / r

        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * DT
        self.vy += ay * DT
        self.x += self.vx * DT
        self.y += self.vy * DT

        current_scale = SCALE

        self.trail.append((int(self.x * current_scale + WIDTH // 2), int(self.y * current_scale + HEIGHT // 2)))
        if len(self.trail) > 200:
            self.trail.pop(0)

    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, (50, 50, 50), False, self.trail, 1)

        current_scale = SCALE

        screen_x = int(self.x * current_scale + WIDTH // 2)
        screen_y = int(self.y * current_scale + HEIGHT // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


bodies = [
    Body(-8e10, 0, 0, 0, MassBig, 1, (153, 255, 153)),  # Telo
    # Body(7.786e11-8e10, 0, 0, 13070, 1.898e27, 6, (200, 150, 100)),  # Sputnik min
    # Body(1.1e12-8e10, 0, 0, 13070, 1.2e27, 2, (00, 150, 200)),  # Спутник ровно
    Body(Radius, 0, 0, velocity, MassSmall, 6, (0, 0, 255)),  # Sputnik max
]


# -----------------------------------------------------------------------------------------------------------------#

class Body1:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail = []

    def update_position(self, bodies1):
        fx = fy = 0
        for other in bodies1:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                r = math.sqrt(dx * dx + dy * dy)
                if r > 0:
                    # Formula: F = G * (m1 * m2) / r^2
                    f = G * self.mass * other.mass / (r * r)
                    fx += f * dx / r
                    fy += f * dy / r

        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * DT
        self.vy += ay * DT
        self.x += self.vx * DT
        self.y += self.vy * DT

        current_scale = SCALE

        screen_x = int(self.x * current_scale + WIDTH // 2)
        screen_y = int(self.y * current_scale + HEIGHT // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


bodies1 = [
    Body1(-8e10, 0, 0, 0, MassBig1, 1, (153, 255, 153)),  # Telo
    # Body1(7.786e11-8e10, 0, 0, 13070, 1.898e27, 6, (200, 150, 100)),  # Sputnik min
    # Body(1.1e12-8e10, 0, 0, 13070, 1.2e27, 2, (00, 150, 200)),  # Спутник ровно
    Body1(Radius1, 0, 0, velocity1, MassSmall1, 6, (255, 0, 0)),  # Sputnik max
]

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            for body in bodies:
                body.trail = []

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                show_overlay_image = True
    win.blit(BG, (0, 0))
    win.blit(telo, (369, 276))

    for body in bodies:
        body.update_position(bodies)
        body.draw(screen)

    for body1 in bodies1:
        body1.update_position(bodies1)

    if show_overlay_image:
        showres()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()