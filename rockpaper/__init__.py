import pygame
from pygame import USEREVENT

MODULE_NAME = 'rockpaper'

SCENE_CHANGE = 1+USEREVENT

# Events we only want handled in main event loop
## put pygame items prior to rockpaper items in this list
sacred_events = [pygame.QUIT, SCENE_CHANGE]
