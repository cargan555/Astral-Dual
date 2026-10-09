import Utils
from Utils import *
from player import Player_2
import pygame

class Phase_2:
    def __init__(self, game, display, players): 
        # essentials
        ''' all of the game parameters in classes exlucing this one are actualy just the phase_1 class'''
        self.game = game
        self.display = display
        self.font = game.font

        Musicplay("lunar_echo")
        print("music start")
        music_volume = 0.5
        pygame.mixer.music.set_volume(music_volume)

        self.players = pygame.sprite.Group()

        self.balance = []
        for player in players:
            self.balance.append(player.money)

        self.player_1 = Player_2(self, "arrow", self.balance[0])
        self.player_2 = Player_2(self, "wasd", self.balance[1])
        
        # assets
        self.shop = Assets(self.display, "Shopselect", None, (1280, 720))
        self.planet = Assets(self.display, "Shopfond", None, (1280, 720))
        self.alien_girl =  Assets(self.display, "Alien girl", None, (256*2, 256*2))  
        
        # objects
        self.upgrade_menu_1 = Upgrade_Menu(self, self.display, [730,430], self.player_1)
        self.upgrade_menu_2 = Upgrade_Menu(self, self.display, [1020,430], self.player_2)
       
        # variables
        self.time = 0
      
    def update(self, key_events):
        self.display.fill((0,0,0))
        self.time = pygame.time.get_ticks()

        if self.upgrade_menu_1.items[-1].state and self.upgrade_menu_2.items[-1].state:
            self.game.p2_to_p3()

        # update
        self.upgrade_menu_1.update(key_events)
        self.upgrade_menu_2.update(key_events)

        # drawing
        self.draw()

    def draw(self):
        self.planet.render((0,0))
        self.shop.render((0,0))
        self.alien_girl.render((0,self.display.get_height() - 256*2))

        self.upgrade_menu_1.draw()
        self.upgrade_menu_2.draw()

class Upgrade_Menu:
    def __init__(self, game, display, pos, player):
        self.game = game
        self.display = display
        self.pos = pos
        self.player = player

        self.upgrades = ["health", "speed", "fire_rate"]
        self.items = []
        self.cursor = Assets(self.display, "Pointer", None, (16*3,16*3))
        self.rect = self.cursor.get_sprite().get_rect()
        self.pos_cursor = [pos[0]+180, pos[1]]
        self.rect.center = self.pos

        self.values = [1, 0.4, -0.6]
        for x in range(3):
            self.items.append(Item(self, self.display, [pos[0], pos[1]+80*x], self.values[x], self.player, 2, self.upgrades[x]))
        self.items.append(Switch(self, self.display, [pos[0]+80, pos[1]+80*3], self.player.key_set))

        self.current = 0

    def update(self, key_events):

        if self.player.key_set == "arrow":
            if key_events['up']:
                if self.current > 0:
                    self.current -= 1
            elif key_events["down"]:
                if self.current < len(self.items)-1:
                    self.current += 1
        elif self.player.key_set == "wasd":
            if key_events['w']:
                if self.current > 0:
                    self.current -= 1
            elif key_events["s"]:
                if self.current < len(self.items)-1:
                    self.current += 1

        self.items[self.current].update(key_events)
        self.rect.center = [self.pos_cursor[0], self.items[self.current].pos[1]]
        
        
    def draw(self):
        Utils.Text_render(f'{self.player.money}$', self.game.font, self.display, self.pos[0], self.pos[1]-80)
        self.cursor.render(self.rect)
        for item in self.items:
            item.draw()
                
class Switch:
    def __init__(self, game, display, pos, target):
        self.game = game
        self.display = display
     
        self.state = False
        self.target = target

        self.not_ready = Assets(self.display, "Not_ready", None, (32*3,32*3))
        self.ready = Assets(self.display, "Ready", None, (32*3,32*3))

        self.image = self.not_ready.get_sprite()
        
        # variables
        self.hitbox = pygame.surface.Surface((self.image.get_size()))
        self.hitbox.fill("purple")
        self.pos = pos
        self.rect = self.hitbox.get_rect()
        self.rect.center = self.pos

    def update(self, key_events):

        if self.target == "arrow":
            if key_events["left"] or key_events["right"]:
                self.state = not self.state
        elif self.target == "wasd":
            if key_events["a"] or key_events["d"]:
              self.state = not self.state

        if self.state:
            self.image = self.ready.get_sprite()
        if self.state == False:
            self.image = self.not_ready.get_sprite()

    def draw(self):
        if self.state:
            self.ready.render(self.rect)
        elif not self.state:
            self.not_ready.render(self.rect)

class Item:
    def __init__(self, game, display, pos, item_value, target_player, price, effect):

        self.game = game
        self.display = display
        self.pos = pos
        self.max = 5
        self.min = 0
        self.value = item_value
        self.player = target_player
        self.price = price
        self.effect = effect

        self.current = 0

        if self.effect == "health":
            self.icon = Assets(self.display, "Health_upgrade", None, (32*2,32*2))
        elif self.effect == "speed":
            self.icon = Assets(self.display, "Speed_upgrade", None, (32*2,32*2))
        elif self.effect == "fire_rate":
            self.icon = Assets(self.display, "Fire_rate_upgrade", None, (32*2,32*2))
        self.image_icon = self.icon.get_sprite()
        self.rect_icon = self.image_icon.get_rect()
        self.rect_icon.center = self.pos

        self.sprites = []
        for x in range(0,6):
            self.sprites.append(Assets(self.display, f"Upgrade_{x}", None, (21*5, 8*5)))

        self.sprite = self.sprites[self.current]
        self.image = self.sprite.get_sprite()
        self.hitbox = pygame.Surface((self.image.get_size()))
        self.hitbox.fill("green")
        self.rect = self.hitbox.get_rect()
        self.rect.center = [self.pos[0] + self.image_icon.get_width()*1.5, self.pos[1]]
        
    def update(self, keys_events):

        if self.player.key_set == "arrow":
            if keys_events["left"]:
                if self.current > self.min:
                    self.current -= 1
                    self.price -= 1
                    self.player.money += self.price + 1
            elif keys_events["right"]:
                if self.player.money > self.price:
                    if self.current < self.max:
                        self.current += 1
                        self.price += 1
                        self.player.money -= self.price
        elif self.player.key_set == "wasd":
            if keys_events["a"]:
                if self.current > self.min:
                    self.current -= 1
                    self.price -= 1
                    self.player.money += self.price + 1
            elif keys_events["d"]:
                if self.player.money > self.price:
                    if self.current < self.max:
                        self.current += 1
                        self.price += 1
                        self.player.money -= self.price

        self.sprite = self.sprites[self.current]
        self.image = self.sprite.get_sprite()

    def draw(self):
        self.icon.render(self.rect_icon)
        self.sprite.render(self.rect)
