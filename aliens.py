import pygame
import Utils
from random import randint

class Bullet_aliens(pygame.sprite.Sprite):
    def __init__(self, game, display, x, y):
        # essentials
        self.groups = game.bullets_aliens
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.display = display

        # assets
        self.sprite = self.game.basic_bullet
        self.image = self.sprite.get_sprite()

        self.hitbox = pygame.Surface(self.image.get_size())
        self.hitbox.fill("yellow")

        self.rect = self.hitbox.get_rect()
        self.pos = [x,y]
        self.rect.center = self.pos

        #  varriables
        self.bullet_speed = 5
        self.bullet_time = 0

    def update(self, time):
        self.bullet_time = time
        if self.pos[0] >= 0:
            self.pos[0] -= 1*self.bullet_speed
        else:
            self.kill()
        self.rect.center = self.pos
        for player in self.game.players:
            if pygame.sprite.collide_rect(self, player):
                player.hitpoints -= 1
                self.kill()

    def draw(self):
        if Utils.debug:
            self.sprite.render(self.rect)
        self.display.blit(self.image, self.rect)

class Basic_alien(pygame.sprite.Sprite):
    def __init__(self, game, display, pos, direction):
        # essentials
        self.groups = game.aliens
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.display = display

        # assets
        self.sprite = game.basic_alien
        self.image = self.sprite.get_sprite()

        self.hitbox = pygame.surface.Surface((self.image.get_size()))
        self.hitbox.fill("yellow")
        self.rect = self.hitbox.get_rect()

        self.pos = pos
        self.rect.center = self.pos
        self.dir = direction

        # variables
        self.hitpoints = 1
        self.last_time = 0
        self.spawn_rate = 0
        self.fire_rate = 30
        if self.dir == "L_R":
            self.move_speed = 3
        if self.dir == "R_L":
            self.move_speed = -3
      

    def update(self):
      
        self.time = pygame.time.get_ticks()

        screen_rect = pygame.Rect(0, 0, self.display.get_width(), self.display.get_height())
        if self.time >= self.spawn_rate + self.fire_rate*100 and pygame.Rect.colliderect(self.rect, screen_rect):
            self.spawn_rate = self.time
            if randint(0,100) > 50:
                self.game.bullets_aliens.add(Bullet_aliens(self.game, self.display, self.pos[0], self.pos[1]))

        if self.dir == "R_L":
            if self.pos[0] <= 0:
                self.kill()
        elif self.dir == "L_R":
            if self.pos[0] >= self.display.get_width():
                self.kill()
        self.pos[0] += self.move_speed

        self.rect.center = self.pos

        if self.hitpoints <= 0:
            if self.killer == "arrow":
                self.game.player_1.score += 10
            if self.killer == "wasd":
                self.game.player_2.score += 10
            self.kill()

        for bullet in self.game.bullets_players:
            if pygame.sprite.collide_rect(self, bullet):
                self.hitpoints -= 1
                self.killer = bullet.key_set
                bullet.kill()

    def draw(self):
        if Utils.debug:
            self.display.blit(self.hitbox, self.rect)
        self.sprite.render(self.rect)


class Speed_alien(pygame.sprite.Sprite):
    def __init__(self, game, display, pos, direction):
        # essentials
        self.groups = game.aliens
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.display = display

        # assets
        self.sprite = game.speed_alien
        self.image = self.sprite.get_sprite()

        self.hitbox = pygame.surface.Surface((self.image.get_size()))
        self.hitbox.fill("yellow")
        self.rect = self.hitbox.get_rect()

        self.pos = pos
        self.rect.center = self.pos
        self.dir = direction

        # variables
        self.hitpoints = 2
        self.last_time = 0
        if self.dir == "L_R":
            self.move_speed = 9
        if self.dir == "R_L":
            self.move_speed = -9
      

    def update(self):
      
        self.time = pygame.time.get_ticks()

        if self.dir == "R_L":
            if self.pos[0] <= 0:
                self.kill()
        elif self.dir == "L_R":
            if self.pos[0] >= self.display.get_width():
                self.kill()
        self.pos[0] += self.move_speed

        self.rect.center = self.pos

        if self.hitpoints <= 0:
            if self.killer == "arrow":
                self.game.player_1.score += 15
            if self.killer == "wasd":
                self.game.player_2.score += 15
            self.kill()

        for bullet in self.game.bullets_players:
            if pygame.sprite.collide_rect(self, bullet):
                self.hitpoints -= 1
                self.killer = bullet.key_set
                bullet.kill()

    def draw(self):
        if Utils.debug:
            self.display.blit(self.hitbox, self.rect)
        self.sprite.render(self.rect)
