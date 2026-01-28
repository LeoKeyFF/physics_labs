import pygame
import math

#=============================#
MassBig = 1
MassSmall = 2

MassBig1 = 1
MassSmall1 = 2
#=============================#


pygame.init()
WIDTH, HEIGHT = 800, 600
telo_size = 25

win = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity task №1")
clock = pygame.time.Clock()

G = 6.67430e-11  # Vonyuchaya constanta
SCALE = 6e-11
DT = 2000000

BG = pygame.transform.scale(pygame.image.load("images/Night_sky1_grid_wip.png").convert(),(WIDTH, HEIGHT))
telo = pygame.transform.scale(pygame.image.load("images/Planet_base_n1.png"), (telo_size * 2, telo_size * 2))

zoomed = False


class Body:
    def  __init__(self, x, y, vx, vy, mass, radius, color):

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
    Body(0, 1.815e12 - 8e10, 10, -5, 1.024e26, 6, (153, 255, 153)), #Telo
    #Body(7.786e11-8e10, 0, 0, 13070, 1.898e27, 6, (200, 150, 100)),  # Sputnik min
    # Body(1.1e12-8e10, 0, 0, 13070, 1.2e27, 2, (00, 150, 200)),  # Спутник ровно
    Body(1.500e12-8e10, 0, 4, 0, 1.024e26, 6, (0, 0, 255)),  # Sputnik max
    Body(-1.100e12 - 8e10, 0, 0, 9, 1.024e26, 6, (50, 255, 240)),  # Sputnik max
]

#-----------------------------------------------------------------------------------------------------------------#

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

    #     self.trail.append((int(self.x * current_scale + WIDTH // 2), int(self.y * current_scale + HEIGHT // 2)))
    #     if len(self.trail) > 200:
    #         self.trail.pop(0)
    #
    #  def draw(self, screen):
    #      if len(self.trail) > 1:
    #          pygame.draw.lines(screen, (50, 50, 50), False, self.trail, 1)

        current_scale = SCALE

        screen_x = int(self.x * current_scale + WIDTH // 2)
        screen_y = int(self.y * current_scale + HEIGHT // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)

bodies1 = [
    # Body1(-8e10, 0, 0, 0, 1.989e30, 1, (153, 255, 153)), #Telo
    # # Body1(7.786e11-8e10, 0, 0, 13070, 1.898e27, 6, (200, 150, 100)),  # Sputnik min
    # # Body(1.1e12-8e10, 0, 0, 13070, 1.2e27, 2, (00, 150, 200)),  # Спутник ровно
    # Body1(4.515e12-8e10, 0, 0, 5430, 1.024e26, 6, (255, 0, 0)),  # Sputnik max
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            for body in bodies:
                body.trail = []
    win.blit(BG, (0,0))
    # win.blit(telo, (369,276))

    for body in bodies:
        body.update_position(bodies)
        body.draw(screen)

    for body1 in bodies1:
        body1.update_position(bodies1)
    #    body1.draw(screen)

    pygame.display.flip()
    clock.tick(36000)

pygame.quit()


