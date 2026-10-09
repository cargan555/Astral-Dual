import Utils
import pygame

class Player_1(pygame.sprite.Sprite):
    def __init__(self, game, display, x, y, key_set):
        # game window + essentials
        self.groups = game.players
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.display = display
        self.width = self.display.get_width()
        self.height = self.display.get_height()
        self.pos = [x,y]
        self.og_pos = self.pos.copy()
        self.key_set = key_set

        if self.key_set == "arrow":
            self.sprite = game.player_1_animation
        elif self.key_set == "wasd":
            self.sprite = game.player_2_animation
        self.image = self.sprite.get_sprite()
        
        self.hitbox = pygame.Surface((self.image.get_size()))
        self.hitbox.fill("green")
        self.rect = self.hitbox.get_rect()
        #self.rect.center = self.pos

        # variables
        self.money = 0
        self.orientation = "Right"
        self.alive = True
        self.holding = False
        self.speed = 8
        self.death_timer = 0
        self.og_image = self.image
        self.animation = 0
        self.invincibility = False
        self.i_frame = 0
        self.blink =  True

    def death(self):
        self.alive = False
        self.holding = False
        self.death_timer = pygame.time.get_ticks()


    def respawn(self):
        '''resets player variables'''
        self.pos = self.og_pos.copy()
        self.rect.center = self.pos
        self.alive = True
        self.speed = 8
        self.orientation = "Right"
        
        self.invincibility = True
        self.i_frame = pygame.time.get_ticks()

      
    def update(self, Left, Right, Up, Down, A, D, W, S, keys):
        self.time = pygame.time.get_ticks()

        # speed handling
        if self.holding:
            self.speed = 4
        else:
            self.speed = 6

        # death and respawning:
        if self.alive == False:
            if self.time >= self.death_timer  + 1000 :
                self.respawn()

        # movement
        if self.key_set == "arrow":
            if Left:
                self.sprite.animate(self.time)
                self.orientation = "Left"
            elif Right:
                self.orientation = "Right"
                self.sprite.animate(self.time)
        if self.key_set == "wasd":
            if A:
               self.orientation = "Left" 
               self.sprite.animate(self.time)
            elif D:
                self.orientation = "Right"
                self.sprite.animate(self.time)
    
        if self.alive == True:

            if self.invincibility:
                if self.time >= self.i_frame + 1500:
                    self.invincibility = False
                self.blink = not self.blink
            else:
                self.blink = True

            self.rect.topleft = self.pos

            if self.key_set == "arrow":
                if Left and self.pos[0] >= 0:
                    self.pos[0] -= 1*self.speed
                if Right and self.pos[0] <= self.width - self.image.get_width():
                    self.pos[0] += 1*self.speed
                if Up and self.pos[1] >= 224:
                    self.pos[1] -= 1*self.speed
                if Down and self.pos[1] <= self.height - self.image.get_height(): 
                    self.pos[1] += 1*self.speed
            elif self.key_set == "wasd":
                if A and self.pos[0] >= 0:
                    self.pos[0] -= 1*self.speed
                if D and self.pos[0] <= self.width - self.image.get_width():
                    self.pos[0] += 1*self.speed
                if W and self.pos[1] >= 224:
                    self.pos[1] -= 1*self.speed
                if S  and self.pos[1] <= self.height  - self.image.get_height(): 
                    self.pos[1] += 1*self.speed

    def draw(self):
       if Utils.debug:
            self.display.blit(self.hitbox, self.rect)
       if self.alive and self.blink:
            ''' we dont use the render method of the Assets class because i dont want to deal with flipping the sprite'''
            if self.orientation == "Right":
                self.sprite.render(self.rect)
            elif self.orientation == "Left":
                self.sprite.render(self.rect, pygame.transform.flip(self.sprite.assets[self.sprite.frame], True, False))


class Player_2(pygame.sprite.Sprite):
    def __init__(self, game, key_set, money):
        # game window + essentials
        self.groups = game.players
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.key_set = key_set

        # variables
        self.money = money

       
class Player_3(pygame.sprite.Sprite):
    def __init__(self, game, display, x, y, stats, key_set):
        # game window + essentials
        self.groups = game.players
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.display = display
        self.width = self.display.get_width()
        self.height = self.display.get_height()
        self.pos = [x,y]
        self.key_set = key_set

        if self.key_set == "arrow":
            self.sprite = self.game.player_sprite_1
        elif self.key_set == "wasd":
            self.sprite = self.game.player_sprite_2
        self.image = self.sprite.get_sprite()
            
        self.hitbox = pygame.Surface((self.image.get_size()))
        self.hitbox.fill("green")
        self.rect = self.hitbox.get_rect()
        self.rect.center = self.pos
    
        # variables<
        self.lives = 3 + stats[0]
        self.score = 0
        self.alive = True
        self.speed = 8 + stats[1]
        self.death_timer = 0
        self.hitpoints = 1
        self.spawn_rate = 0
        self.fire_rate = 5 + stats[2]
        self.damage = 1
        self.invincibility = False
        self.i_frame = 0
        self.blink =  True
    
    def respawn(self):
        '''resets player variables'''
        if self.key_set == "arrow":
            self.pos = [100, 200]
        if self.key_set == "wasd":
            self.pos = [100, 400]
        self.rect.center = self.pos
        self.alive = True
        self.speed = 8
        self.death_timer = 0
        self.hitpoints = 1

        self.invincibility = True
        self.i_frame = pygame.time.get_ticks()

    def death(self):
        self.lives -= 1
        self.alive = False
        self.hitpoints = 1
        self.death_timer = pygame.time.get_ticks()
        
    def update(self, Left, Right, Up, Down, A, D, W, S, keys):
        self.time = pygame.time.get_ticks()

        if self.lives > 0:
            #death:
            if self.hitpoints <= 0:
                self.death()

            # respawning:
            if self.alive == False:
                if self.time >= self.death_timer  + 2000 :
                    self.respawn()

            # movement
            if self.alive == True:

                if self.invincibility:
                    if self.time >= self.i_frame + 1500:
                        self.invincibility = False
                        self.blink = not self.blink
                    else:
                        self.blink = True

                self.rect.center = self.pos
                if self.key_set == "arrow":
                    if Left and self.pos[0] >= 0:
                        self.pos[0] -= 1*self.speed
                    if Right and self.pos[0] <= self.width:
                        self.pos[0] += 1*self.speed
                    if Up and self.pos[1] >= 0:
                        self.pos[1] -= 1*self.speed
                    if Down and self.pos[1] <= self.height: 
                        self.pos[1] += 1*self.speed
                elif self.key_set == "wasd":
                    if A and self.pos[0] >= 0:
                        self.pos[0] -= 1*self.speed
                    if D and self.pos[0] <= self.width:
                        self.pos[0] += 1*self.speed
                    if W and self.pos[1] >= 0:
                        self.pos[1] -= 1*self.speed
                    if S  and self.pos[1] <= self.height: 
                        self.pos[1] += 1*self.speed
            else:
                self.alive = False
                    
    def draw(self):
        if Utils.debug:
            self.display.blit(self.hitbox, self.rect)
        if self.alive:
            self.display.blit(self.image, self.rect)
