import Utils
from Utils import *
from player import Player_2
import pygame

class Phase_4:
    def __init__(self, game, display, winner): 
        # essentials
        ''' all of the game parameters in classes exlucing this one are actualy just the phase_1 class'''
        self.game = game
        self.display = display
        self.font = game.font

        Musicplay("100_victories")
        print("music start")
        music_volume = 0.5
        pygame.mixer.music.set_volume(music_volume)

        self.players = pygame.sprite.Group()

        self.winner = winner
        
        # assets
        if self.winner == "arrow":
            self.victory_screen = Assets(self.display, "Pink_win", None, (1280,720))
            self.winner = 1
        if self.winner == "wasd":
            self.victory_screen = Assets(self.display, "Blue_win", None, (1280,720))
            self.winner = 2
        if self.winner == "tied":
            self.victory_screen = Assets(self.display, "Both_win", None, (1280,720))
      
    def update(self):
        self.display.fill((0,0,0))
        self.draw()
      
    def draw(self):
        self.victory_screen.render((0,0))
        if self.winner == "tied":
            Utils.Text_render(f'Both Player won', self.font, self.display, 350, 580)
        else:
            Utils.Text_render(f'Player {self.winner} won', self.font, self.display, 350, 580)