import pygame
import rockpaper.resrc
import rockpaper.scene
from rockpaper import sacred_events

class StartScene(rockpaper.scene.Scene):
    def __init__(self, *args, **kwargs):
        rockpaper.scene.Scene.__init__(self,'Start')
        self.title_text = None
        self.psts_text = None

        self.load()

    def load(self):
        font_file = rockpaper.resrc.find_resource('font', name='militech.ttf')
        # T: SUPER ROCK PAPER SCISSORS
        font = pygame.font.Font(font_file, 32)
        self.title_text = font.render("Super Rock Paper Scissors", False,
        (255,0,0))
        # T: PRESS SPACE TO START
        font = pygame.font.Font(font_file, 18)
        self.psts_text = font.render("Press SPACE to start!", False,
        (255,0,0))
        return

    def draw(self):
        if not self.changing:
            primary = pygame.display.get_surface()
            primary.blit(self.title_text,(250,250))
            primary.blit(self.psts_text,(350,300))
            return pygame.display.flip()

    def on_change(self):
        print("Changing scene...")

        primary = pygame.display.get_surface()
        primary.fill((0,0,0))
        pygame.display.flip()

        return

    def run(self, events):
        if not self.changing:
            self.draw()

            for event in events:
                # never process events in main handler
                if event.type in sacred_events:
                    self.repost_events(event)
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.changing = True
                        self.change('Main')

        return
