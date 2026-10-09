import pygame
import os
from random import randint


global debug
debug = False

def load_image(name):
    return pygame.image.load(os.path.join('assets', f'{name}.png')).convert_alpha()

class Assets():
    def __init__(self, display, name, bg_color=None, size=None):
        # asset fetch
        self.display = display
        self.asset = pygame.image.load(os.path.join('assets', f'{name}.png')).convert_alpha()
        if bg_color:
            self.asset.set_colorkey(bg_color)
        if size:
            self.asset = pygame.transform.scale(self.asset, size)

    def render(self, rect, new_image=None):
        if new_image:
            self.display.blit(new_image, rect)
        else:
            self.display.blit(self.asset, rect)

    def get_sprite(self):
        return self.asset

class Animation():
    def __init__(self, display, name, delay, size, scale=None):
        self.display = display
        self.frame = 0
        self.last_frame = 0
        self.delay = delay
        self.assets = []
        self.spritesheet = pygame.image.load(os.path.join('assets', f'{name}.png')).convert_alpha()
        for x in range(self.spritesheet.get_width()//size[0]):
            for y in range(self.spritesheet.get_height()//size[1]):
                image = pygame.Surface(size)
                image.blit(self.spritesheet, (0,0), (x*size[0], y*size[1], size[0], size[1]))
                image.set_colorkey((0,0,0))
                if scale:
                    image = pygame.transform.scale(image, scale)
                self.assets.append(image)

    def animate(self, time):
       
        if time >= self.last_frame + self.delay:
            self.last_frame = time
            self.frame += 1
        if self.frame >= len(self.assets):
            self.frame = 0
        return self.assets[self.frame]

    def render(self, rect, new_image=None):
        if new_image:
            self.display.blit(new_image, rect)
        else:
            self.display.blit(self.assets[self.frame], rect)

    def get_sprite(self):
        return self.assets[self.frame]

    

def Text_render(text, font, display, x, y):
       text = str(text)
       text_box = font.render(text, False, ("#ffffff"))
       shadow = font.render(text, False, ("#a33729"))
       display.blit(shadow, (x+4,y+4))
       display.blit(text_box, (x,y))
    
def Soundplay(name):
    sfx = pygame.mixer.Sound(os.path.join('audio', f'{name}.ogg'))
    sfx.play()
    sfx.set_volume(0.2)

def Musicplay(name):
    pygame.mixer.music.load(os.path.join('audio', f'{name}.ogg'))
    pygame.mixer.music.play(-1)