import random
import sys

import pygame

import costants
from Entities.Boid import Boid

pygame.init()
screen = pygame.display.set_mode((costants.SCREEN_WIDTH, costants.SCREEN_HEIGHT))
pygame.display.set_caption('Boids')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

# classica lista di sprite
boidList = pygame.sprite.Group()

# lista di sprite che hanno bisogno di essere aggioranti, i think
allSpritesList = pygame.sprite.LayeredDirty()

for i in range(25):
    boid = Boid(random.randint(0, costants.SCREEN_WIDTH), random.randint(0, costants.SCREEN_HEIGHT), 25, 15, 15,
                costants.FIELD_OF_VIEW)
    boidList.add(boid)
    allSpritesList.add(boid)

clock = pygame.time.Clock()

running = True

allSpritesList.clear(screen, background)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    text = "Boids Simulation: FPS: {0:.2f}".format(clock.get_fps())
    pygame.display.set_caption(text)

    for boid in boidList:
        closeboids = []
        for otherboid in boidList:
            if otherboid == boid:
                continue
            distance = boid.distance(otherboid)
            if distance < boid.fieldOfView:
                closeboids.append(otherboid)

        boid.cohesion(closeboids)
        boid.alignment(closeboids)
        boid.separation(closeboids, 20)
        boid.update(False)

        # Create list of dirty rects
        rects = allSpritesList.draw(screen)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.update(rects)
        clock.tick(1000)

pygame.quit()
sys.exit()
