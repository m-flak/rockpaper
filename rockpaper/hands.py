import math
import pygame
from rockpaper.resrc import find_resource

ROCK = 0
PAPER = 1
SCISSORS = 2

class Hands(object):
    def __init__(self,*args,**kwargs):
        self._highlighted = [False, False, False]
        self.rockhand = pygame.image.load(find_resource('image', name='rock.png'))
        self.rockhand = self.rockhand.convert_alpha()
        self.rockhand_orig = self.subsurf_hand(self.rockhand).convert_alpha()
        self.paperhand = pygame.image.load(find_resource('image', name='paper.png'))
        self.paperhand = self.paperhand.convert_alpha()
        self.paperhand_orig = self.subsurf_hand(self.paperhand).convert_alpha()
        self.scissorshand = pygame.image.load(find_resource('image', name='scissors.png'))
        self.scissorshand = self.scissorshand.convert_alpha()
        self.scissorshand_orig = self.subsurf_hand(self.scissorshand).convert_alpha()

    @staticmethod
    def subsurf_hand(hand):
        # these coords are arguably the middle of the hand images
        return hand.subsurface(pygame.Rect(31,32,61,62))

    @property
    def rock_highlighted(self):
        return self._highlighted[0]

    @rock_highlighted.setter
    def rock_highlighted(self, value):
        if not isinstance(value, bool):
            return
        self._highlighted[0] = value

    @property
    def paper_highlighted(self):
        return self._highlighted[1]

    @paper_highlighted.setter
    def paper_highlighted(self, value):
        if not isinstance(value, bool):
            return
        self._highlighted[1] = value

    @property
    def scissors_highlighted(self):
        return self._highlighted[2]

    @scissors_highlighted.setter
    def scissors_highlighted(self, value):
        if not isinstance(value, bool):
            return
        self._highlighted[2] = value

    # when calling elsewhere, ofc use hands.ROCK, etc. instead of integers
    # that's what this returns, a tuple of a boolean and the hand
    # RECURSIVE
    def within_hand(self, x, y, hand=0):
        # Woah, man, there's only three options
        if hand > 2:
            return False, -1
        # these coords are position & WxH
        hand_coords = [pygame.Rect(128,400,128,128),
                        pygame.Rect(320,400,128,128),
                        pygame.Rect(512,400,128,128)]
        if x >= hand_coords[hand].left and x <= hand_coords[hand].left+hand_coords[hand].width:
            if y >= hand_coords[hand].top and y <= hand_coords[hand].top+hand_coords[hand].height:
                return True, hand
        return self.within_hand(x,y,hand+1)

    def draw_hands(self, draw_surface):
        #euclidian distance
        def distance(p1,p2) -> int:
            d1 = pow(p1[1]-p1[0],2)
            d2 = pow(p2[0]-p2[1],2)
            return int(math.sqrt(d1+d2))

        # 'hands' are 128x128
        # with a spacing of 64px
        draw_surface.blit(self.rockhand,pygame.Rect(128,400,0,0))
        # handle highlighting via mouse cursor
        # rock
        if self.rock_highlighted is True:
            self.rockhand.lock()
            pygame.draw.circle(self.rockhand, pygame.Color(255,0,0,64), (64,64),
                distance((61,0),(0,62))//8)
            self.rockhand.unlock()
        else:
            self.rockhand.blit(self.rockhand_orig,(31,32))

        draw_surface.blit(self.paperhand,pygame.Rect(320,400,0,0))
        # paper
        if self.paper_highlighted is True:
            self.paperhand.lock()
            pygame.draw.circle(self.paperhand, pygame.Color(255,0,0,64), (64,64),
                distance((61,0),(0,62))//8)
            self.paperhand.unlock()
        else:
            self.paperhand.blit(self.paperhand_orig,(31,32))

        draw_surface.blit(self.scissorshand,pygame.Rect(512,400,0,0))
        # scissors
        if self.scissors_highlighted is True:
            self.scissorshand.lock()
            pygame.draw.circle(self.scissorshand, pygame.Color(255,0,0), (64,64),
                distance((61,0),(0,62))//8)
            self.scissorshand.unlock()
        else:
            self.scissorshand.blit(self.scissorshand_orig,(31,32))

    def draw_enemy_hand(self, draw_surface, hand):
        enemy_hand = None

        if hand is None:
            return
        elif hand == ROCK:
            enemy_hand = pygame.transform.flip(self.rockhand.copy(), True, True)
        elif hand == PAPER:
            enemy_hand = pygame.transform.flip(self.paperhand.copy(), True, True)
        elif hand == SCISSORS:
            enemy_hand = pygame.transform.flip(self.scissorshand.copy(), True, True)

        blankie = pygame.Surface((128,128))
        blankie.fill((0,0,0))
        draw_surface.blit(blankie, pygame.Rect(350,128,0,0))
        draw_surface.blit(enemy_hand, pygame.Rect(350, 128, 0, 0))
