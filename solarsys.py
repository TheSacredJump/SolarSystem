import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1500, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simlation")

BLACK = (0,0,0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (80, 78, 81)
ORANGE = (255, 165, 0)
BROWN = (150, 75, 0)

BG = pygame.image.load('Solar System/space2.jpg')

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67e-11
    SCALE = 150 / AU #Scale: 1AU = 100px
    TIMESTEP = 3600*24 #1 day time step

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.dist_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y  * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self. y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892e30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, GRAY, 3.30e23)
    mercury.y_vel = -47.4 * 1000
    
    venus = Planet(0.732 * Planet.AU, 0, 14, ORANGE, 4.8685e24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.0742e24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39e20)
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(-4.95 * Planet.AU, 0, 20, BROWN, 1898e24)
    jupiter.y_vel = 13.1 * 1000


    planets = [sun, mercury, venus, earth, mars, jupiter]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        WIN.blit(BG, (0, 0))

        #Quitting the simulation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()