from Utils import *
from player import Player_3
import pygame

class Testing:
    def __init__(self, game): 
        # essentials
        ''' all of the game parameters in classes exlucing this one are actualy just the phase_1 class'''
        self.game = game
        self.display = game.display
        self.font = pygame.font.Font('PressStart2P.ttf', 30)

        self.player_sprite_1 = Assets(self.display, "Pink_ship", (0,0,0), (20*3, 16*3))
        self.player_sprite_2 = Assets(self.display, "Blue_ship", (0,0,0), (64,64))

        self.players = pygame.sprite.Group()
        self.player_1 = Player_3(self, self.display, 400, 400, "arrow")
        self.player_2 = Player_3(self, self.display, 400, 500, "wasd")

       
        
        # variables
        self.time = 0       
      
    def update(self, Left, Right, Up, Down, A, D, W, S, key_events, mouse_btn_state):
        self.display.fill((0,0,0))
        self.time = pygame.time.get_ticks()

        self.players.update(Left, Right, Up, Down, A, D, W, S, key_events)

        self.draw()

    def draw(self):
        pass
 