import pygame
from rockpaper.resrc import find_resource

class Life(object):
    def __init__(self, health):
        self.health = health
        self.max_health = health
        self.hearts = []
        self.h_img = pygame.image.load(find_resource('image', name='heart.png'))
        for i in range(0, health):
            self.hearts.insert(i, pygame.Surface((48,48)))

    def __sub__(self, other):
        self.health -= 1

    def __rsub__(self, other):
        self.health -= 1

    def is_dead(self):
        if self.health == 0:
            return True
        return False

    # draw from right to left, rectWhere is rightmost coordinates
    # hearts are 48x48
    def draw_hearts(self, draw_surface, rectWhere):
        rW = rectWhere
        for surf in self.hearts:
            surf.fill((0,0,0))
            rW.left -= rectWhere.width
            draw_surface.blit(surf, rW)
        rW = rectWhere
        for i in range (0, self.health):
            self.hearts[i].blit(self.h_img.copy(),(0,0))
            rW.left -= rectWhere.width
            draw_surface.blit(self.hearts[i], rW)

        return
