import math
import random

import pygame.sprite

from costants import *


class Boid(pygame.sprite.DirtySprite):

    def __init__(self, x, y, cohesion_weight, alignment_weight, separation_weight, field_of_view):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.image.load("images/boid.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.fieldOfView = field_of_view
        self.cohesionWeight = cohesion_weight
        self.alignmentWeight = alignment_weight
        self.separationWeight = separation_weight

        self.rect.x = x
        self.rect.y = y

        self.velocityX = random.randint(1, 10) / 10
        self.velocityY = random.randint(1, 10) / 10

    def distance(self, otherBoid):
        if not otherBoid:
            return -1
        return math.sqrt((self.rect.x - otherBoid.rect.x) ** 2 + (self.rect.y - otherBoid.rect.y) ** 2)

    def cohesion(self, otherBoids):
        if len(otherBoids) == 0:
            return

        center = self.find_center_of_mass(otherBoids)
        cohesion_velocity_change = (center[0] - self.rect.x, center[1] - self.rect.y)

        # set our velocity towards the others
        self.velocityX += (cohesion_velocity_change[0] / self.cohesionWeight)
        self.velocityY += (cohesion_velocity_change[1] / self.cohesionWeight)

    def alignment(self, boid_list):
        if len(boid_list) == 0:
            return

        # calculate the average velocities of the other prey_list
        average_velocity = [0, 0]

        for boid in boid_list:
            average_velocity[0] += boid.velocityX
            average_velocity[1] += boid.velocityY

        average_velocity[0] /= len(boid_list)
        average_velocity[1] /= len(boid_list)

        # set our velocity towards the others
        self.velocityX += (average_velocity[0] / self.alignmentWeight)
        self.velocityY += (average_velocity[1] / self.alignmentWeight)

    def separation(self, boid_list, min_distance):
        if len(boid_list) == 0:
            return

        separation_velocity_change = [0, 0]

        for boid in boid_list:
            if self.distance(boid) < min_distance:
                separation_velocity_change[0] += self.rect.x - boid.rect.x
                separation_velocity_change[1] += self.rect.y - boid.rect.y

        self.velocityX += separation_velocity_change[0] / self.separationWeight
        self.velocityY += separation_velocity_change[1] / self.separationWeight

    def update(self, wrap):
        if wrap:
            # If we leave the screen we reappear on the other side.
            if self.rect.x < 0 and self.velocityX < 0:
                self.rect.x = SCREEN_WIDTH
            if self.rect.x > SCREEN_WIDTH and self.velocityX > 0:
                self.rect.x = 0
            if self.rect.y < 0 and self.velocityY < 0:
                self.rect.y = SCREEN_HEIGHT
            if self.rect.y > SCREEN_HEIGHT and self.velocityY > 0:
                self.rect.y = 0
        # Bounce off the walls to stay on screen. We lose a random amount of velocity along the axis we collided on.
        else:
            if self.rect.x < 0 and self.velocityX < 0:
                self.velocityX = -self.velocityX * random.random()
            if self.rect.x > SCREEN_WIDTH and self.velocityX > 0:
                self.velocityX = -self.velocityX * random.random()
            if self.rect.y < 0 and self.velocityY < 0:
                self.velocityY = -self.velocityY * random.random()
            if self.rect.y > SCREEN_HEIGHT and self.velocityY > 0:
                self.velocityY = -self.velocityY * random.random()

        speed = math.sqrt(self.velocityX ** 2 + self.velocityY ** 2)
        if speed > 10:
            scale_factor = 10 / speed
            self.velocityX *= scale_factor
            self.velocityY *= scale_factor
        elif speed < 1:
            cohesion_velocity_change = ((SCREEN_WIDTH / 2) - self.rect.x, (SCREEN_HEIGHT / 2) - self.rect.y)

            # set our velocity towards the others
            self.velocityX += (cohesion_velocity_change[0] / self.cohesionWeight)
            self.velocityY += (cohesion_velocity_change[1] / self.cohesionWeight)

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        # Since the boids should always be moving, we don't have to worry about whether or not they have a dirty rect
        self.dirty = 1

    def find_center_of_mass(self, boid_list):
        if len(boid_list) == 0:
            return None

        center = [0, 0]
        for boid in boid_list:
            center[0] += boid.rect.x
            center[1] += boid.rect.y
        center[0] /= len(boid_list)
        center[1] /= len(boid_list)

        return center
