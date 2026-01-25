import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
clock = pygame.time.Clock()

G = 6.67430e-11  # Gravitational constant
SCALE = 6e-11
ZOOM_SCALE = 1e-9
daytime = 86400

zoomed = False


class Body:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        super().__init__()
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
                    f = G * self.mass * other.mass / (r * r)
                    fx += f * dx / r
                    fy += f * dy / r

        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * daytime
        self.vy += ay * daytime
        self.x += self.vx * daytime
        self.y += self.vy * daytime

        current_scale = ZOOM_SCALE if zoomed else SCALE

        self.trail.append((int(self.x * current_scale + WIDTH // 2), int(self.y * current_scale + HEIGHT // 2)))
        if len(self.trail) > 200:
            self.trail.pop(0)

    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, (50, 50, 50), False, self.trail, 1)

        current_scale = ZOOM_SCALE if zoomed else SCALE

        screen_x = int(self.x * current_scale + WIDTH // 2)
        screen_y = int(self.y * current_scale + HEIGHT // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


bodies = [
    Body(0, 0, 0, 0, 1.989e30, 8, (255, 255, 0)),
    # Sun  (1.989e30 kg, 8 pixel radius (not used in calculations, just visual))
    Body(5.79e11, 0, 0, 20000, 3.301e30, 2, (169, 169, 169)),  # Mercury
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            for body in bodies:
                body.trail = []

    screen.fill((0, 0, 0))

    for body in bodies:
        body.update_position(bodies)
        body.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


