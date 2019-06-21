from enum import Enum
import pygame
import random
import rockpaper.hands
import rockpaper.life
from rockpaper.resrc import find_resource
import rockpaper.scene
from rockpaper import sacred_events

class Turn(Enum):
    player = 1
    computer = 2

class Winners(Enum):
    player = 1
    computer = 2
    nobody = 3

class MainScene(rockpaper.scene.Scene):
    def __init__(self, *args, **kwargs):
        rockpaper.scene.Scene.__init__(self,'Main')
        self.turn  = Turn.player
        self.playerhand = None
        self.comphand = None
        self.winner = None
        self.hands = None
        self.lifemeter = rockpaper.life.Life(3)
        self.font  = None
        self.hand_text = "Nothing Selected."
        self.win_text = ""
        self.load()

    def load(self):
        self.hands = rockpaper.hands.Hands()
        self.font  = pygame.font.Font(rockpaper.resrc.find_resource('font', name='militech.ttf'),
            32)
        return

    def draw(self):
        if not self.changing:
            primary = pygame.display.get_surface()
            primary.fill((0,0,0)) # # # OH WOW, I FORGOT THIS
                                  # this makes sense lol

            if self.lifemeter.is_dead() is True:
                string = "You have died."
                string2 = "Press SPACE to continue..."
                deadtext = self.font.render(string, False, (255,0,0))
                deadtext2 = self.font.render(string2, False, (255,0,0))
                primary.blit(deadtext, (400-len(string)//2,300))
                primary.blit(deadtext2, (400-len(string2)//2, 348))
                return pygame.display.flip()

            # DRAW THE HANDS!
            self.hands.draw_hands(primary)
            # CLEAR THE AREA(s) WE DRAW TEXT TO
            blankie = pygame.Surface((800,32))
            blankie.fill((0,0,0))
            primary.blit(blankie, (0,568))
            # DRAW SELECTION TEXT
            seltext = self.font.render(self.hand_text, False, (255,0,0))
            primary.blit(seltext, (400-len(self.hand_text),568))

            # DRAW COMPUTER'S CHOICE
            if self.comphand is not None:
                self.hands.draw_enemy_hand(primary, self.comphand)

            # DRAW HEALTH
            self.lifemeter.draw_hearts(primary, pygame.Rect(600,48,48,48))

            # WHO WON? (yet?)
            if self.winner is not None:
                blankie2 = pygame.Surface((800,32))
                blankie2.fill((0,0,0))
                primary.blit(blankie2, (0,16))

                wintext = None
                if self.winner is Winners.player or self.winner is Winners.nobody:
                    wintext = self.font.render(self.win_text, False, (0,255,0))
                else:
                    wintext = self.font.render(self.win_text, False, (255,0,0))

                primary.blit(wintext, (400-len(self.win_text)*2,16))

            return pygame.display.flip()

    def on_change(self):
        print("Changing scene...")

        # reset state
        self.lifemeter = rockpaper.life.Life(3)

        primary = pygame.display.get_surface()
        primary.fill((0,0,0))
        pygame.display.flip()

        self.changing = False
        return

    def run(self, events):
        if not self.changing:
            dead = False

            if self.lifemeter.is_dead() is True:
                dead = True
            if self.turn == Turn.computer:
                self.winner = self.calculate_victory(self.playerhand)
                if self.winner != Winners.player and self.winner != Winners.nobody:
                    self.lifemeter - 1
                self.turn = Turn.player
                self.set_winner_text(self.winner)

            self.draw()

            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    tf, hand = self.hands.within_hand(event.pos[0],event.pos[1])
                    if tf is True:
                        if hand == rockpaper.hands.ROCK:
                            self.hands.rock_highlighted = True
                            self.hands.paper_highlighted = False
                            self.hands.scissors_highlighted = False
                            self.hand_text = "ROCK!"
                        elif hand == rockpaper.hands.PAPER:
                            self.hands.rock_highlighted = False
                            self.hands.paper_highlighted = True
                            self.hands.scissors_highlighted = False
                            self.hand_text = "PAPER!"
                        elif hand == rockpaper.hands.SCISSORS:
                            self.hands.rock_highlighted = False
                            self.hands.paper_highlighted = False
                            self.hands.scissors_highlighted = True
                            self.hand_text = "SCISSORS!"
                    else:
                        self.hand_text = "..."
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tf, hand = self.hands.within_hand(event.pos[0],event.pos[1])
                    if tf is True:
                        self.turn = Turn.computer
                        self.playerhand = hand
                if dead:
                    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            dead = False
                            self.lifemeter.reset_health()

                # never process events in main handler
                if event.type in sacred_events:
                    self.repost_events(event)

        return

    def calculate_victory(self, player_choice):
        hands = [rockpaper.hands.ROCK,rockpaper.hands.PAPER,rockpaper.hands.SCISSORS]
        random.shuffle(hands)
        computer_choice = random.choice(hands)
        self.comphand = computer_choice

        if computer_choice == rockpaper.hands.ROCK and player_choice == rockpaper.hands.ROCK:
            return Winners.nobody
        elif computer_choice == rockpaper.hands.ROCK and player_choice == rockpaper.hands.PAPER:
            return Winners.player
        elif computer_choice == rockpaper.hands.ROCK and player_choice == rockpaper.hands.SCISSORS:
            return Winners.computer
        elif computer_choice == rockpaper.hands.PAPER and player_choice == rockpaper.hands.ROCK:
            return Winners.computer
        elif computer_choice == rockpaper.hands.PAPER and player_choice == rockpaper.hands.PAPER:
            return Winners.nobody
        elif computer_choice == rockpaper.hands.PAPER and player_choice == rockpaper.hands.SCISSORS:
            return Winners.player
        elif computer_choice == rockpaper.hands.SCISSORS and player_choice == rockpaper.hands.ROCK:
            return Winners.player
        elif computer_choice == rockpaper.hands.SCISSORS and player_choice == rockpaper.hands.PAPER:
            return Winners.computer
        elif computer_choice == rockpaper.hands.SCISSORS and player_choice == rockpaper.hands.SCISSORS:
            return Winners.nobody

        return Winners.nobody

    def set_winner_text(self, the_winner):
        if the_winner is Winners.player:
            self.win_text = "YOU WON!"
        elif the_winner is Winners.computer:
            self.win_text = "YOU LOST!"
        else:
            self.win_text = "IT'S A DRAW!"
