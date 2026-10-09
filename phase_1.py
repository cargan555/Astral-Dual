import Utils
from Utils import *
from player import *
import pygame

class Phase_1:
    def __init__(self, game, display):
        ''' Phase 1:
        This class is in charge of handling all events that take place during the first phase of the game, drawing and updating sprites
        Scrap class:
            The scrap class handles the rendering of the scraps dropped by meteorites, their rarity and their destruction.
        Box class:
            This class is in charge of handling the rendering of the deposit area 
        missile class:
            This class is in charge of rendering meteorites and spawning scraps and assigning them a rarity 
        Warning class:
            This class is in charge or rendering the warning shadow and spawning in meteors
        '''
        
        # essentials
        ''' all of the game parameters in classes bellow exlucing this one are actualy just the phase_1 class'''
        self.game = game
        self.display = display
        self.width = 1280
        self.height = 720
        self.font = game.font
        #Musicplay("underground")

        self.players = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.scraps = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()

        # assets
        self.background = Assets(self.display, "Moon",(0,0,0), self.display.get_size())

        self.player_sprite_1 = Assets(self.display, "Pinkastro", None, (90,90))
        self.player_sprite_2 = Assets(self.display, "Blueastro", None, (90,90))

        # make warning shadow into a sprite sheet
        self.target = Assets(self.display, "Cible", None, (80,36))
        # animated sprites
        self.player_1_animation = Animation(self.display, "Pinkastro spritesheet", 100, (48, 48), (90, 90))
        self.player_2_animation = Animation(self.display, "Blueastro spritesheet", 100, (48, 48), (90, 90))
        self.missile = Animation(self.display, "Missiles spritesheet", 100, (20, 64), (20*3, 64*3))
        self.explosion = Animation(self.display, "Explosion spritesheet", 125, (96, 128), (96*3, 128*3))

        self.scrap_metal_common = Assets(self.display, "Scrap_metal_common", None, (100,100))
        self.scrap_metal_rare = Assets(self.display, "Scrap_metal_rare", None, (100,100))
        self.scrap_metal_legendary = Assets(self.display, "Scrap_metal_legendary", None, (100,100))
      
        self.pinkcam = Assets(self.display, "Pinkcam", None, (237*1.5, 127*1.5))
        self.bluecam = Assets(self.display, "Bluecam", None, (237*1.5, 127*1.5))

        # objects
        self.player_1 = Player_1(self, self.display, 80, 350, "arrow")
        self.player_2 = Player_1(self, self.display, 80, 430, "wasd")
 
        self.boxes.add(Box(self, display, [140,300], "arrow", self.font))
        self.boxes.add(Box(self, display, [140,600], "wasd", self.font))

        self.scoreboard = Scoreboard(self, self.display, self.font, [self.player_1,self.player_2])

        # variables
        self.timer = 60
        self.time_last = 0
        self.active = True
        self.time_last_projectile = 0

    def update(self,  Left, Right, Up, Down, A, D, W, S, keys):
        if self.timer <= 0:
            self.game.p1_to_p2()

        self.time = pygame.time.get_ticks()

        # spawn projectile
        if self.time >= self.time_last_projectile + 1000:
            self.time_last_projectile = self.time
            self.projectiles.add(Projectiles(self, self.display))

        # scraps collection and deletion
        for scrap in self.scraps:
            for box in self.boxes:
                if pygame.sprite.collide_rect(box, scrap) and scrap.picked_up == True and box.target_player == scrap.target_player.key_set:
                    box.collect_material(scrap)
                    scrap.target_player.holding = False
                    scrap.kill()

        self.scoreboard.update([self.player_1,self.player_2])
        self.scraps.update()
        self.projectiles.update(self.time)
        self.players.update(Left, Right, Up, Down, A, D, W, S, keys)
        self.draw()

    def draw(self):
        self.background.render((0,0))
        self.scoreboard.draw()

        for box in self.boxes:
            box.draw()
        for scrap in self.scraps:
            scrap.draw()
        for player in self.players:
            player.draw()
        for projectile in self.projectiles:
            projectile.draw()

        if self.time >= self.time_last + 1000:
            self.time_last = self.time
            self.timer -= 1
        Text_render(f'{self.timer}', self.font, self.display, self.display.get_width()/2, 20)

class Box(pygame.sprite.Sprite):
    def __init__(self, game, display, pos, target, font):
        self.groups = game.boxes
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.font = font
        self.display = display

        self.target_player = target

        if target == "arrow":
            self.sprite = game.pinkcam
        if target == "wasd":
            self.sprite = game.bluecam
        
        self.image = self.sprite.get_sprite()
        self.hitbox = pygame.surface.Surface((self.image.get_size()))
        self.hitbox.fill("blue")
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
        self.gain = 0
        self.time = None

    def collect_material(self, scrap, ):
        self.time = pygame.time.get_ticks()
        if scrap.rarity == "common":
            scrap.target_player.money += 2
            self.gain = 2
        elif scrap.rarity == "rare":
            scrap.target_player.money += 5
            self.gain = 5
        elif scrap.rarity == "legendary":
            scrap.target_player.money += 10
            self.gain = 10
      
    def draw(self):
        if Utils.debug:
            self.display.blit(self.hitbox, self.rect)
        self.sprite.render(self.rect)
        if self.time:
            if pygame.time.get_ticks() <= self.time + 2000:
                Utils.Text_render(f'+{self.gain}', self.font, self.display, self.pos[0], self.pos[1])

class Scraps(pygame.sprite.Sprite):
    def __init__(self, game, display, pos, rarity):  
        self.groups = game.scraps
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.display = display

        # assets
        if rarity == "common":
            self.sprite = game.scrap_metal_common
        elif rarity == "rare":
            self.sprite = game.scrap_metal_rare
        elif rarity == "legendary":
            self.sprite = game.scrap_metal_legendary
        self.image = self.sprite.get_sprite()

        # variables
        self.rarity = rarity
        self.hitbox = pygame.surface.Surface((self.image.get_size()))
        self.hitbox.fill("purple")
        self.pos = pos
        self.rect = self.hitbox.get_rect()
        self.rect.center = self.pos

        self.picked_up = False
        self.target_player = None

    def update(self):
        for player in self.game.players:
            if pygame.sprite.collide_rect(self, player) and player.holding == False and self.picked_up == False:
                self.picked_up = True
                self.target_player = player
                self.hitbox.fill("purple")
        for projectile in self.game.projectiles:
            if projectile.explosion_active and self.picked_up == False:
                if pygame.Rect.colliderect(self.rect, projectile.rect_explosion):
                    self.kill()

        if self.picked_up and self.target_player.alive:
            self.pos = [self.target_player.rect.center[0], self.target_player.rect.center[1]-self.hitbox.get_height()/2]
            self.rect.center = self.pos
            self.target_player.holding = True
        else:
            self.picked_up = False
         
    def draw(self):
        if Utils.debug:
            self.display.blit(self.hitbox, self.rect)
        self.sprite.render(self.rect)

class Projectiles(pygame.sprite.Sprite):
    def __init__(self, game, display):
        self.groups = game.projectiles
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.display = display

        # assets 
        self.sprite_target = game.target
        self.sprite_missile = game.missile
        self.sprite_explosion = game.explosion

        self.image_target = self.sprite_target.get_sprite()
        self.image_missile = self.sprite_missile.get_sprite()
        self.image_explosion = self.sprite_explosion.get_sprite()
       
        # variables
        self.toggle_hitbox = False

        self.pos_target = None
        self.pos_missile = None
        self.pos_explosion = None

        self.hitbox_target = None
        self.hitbox_missile = None
        self.hitbox_explosion = None

        self.rect_target = None
        self.rect_missile = None
        self.rect_explosion = None

        self.target_active = False
        self.missile_active = False
        self.explosion_active = False

        self.spawn_target()

    def spawn_target(self):
        self.pos_target = (randint(400, self.display.get_width()-100), randint(244, self.display.get_height()-50))
        self.hitbox_target = pygame.surface.Surface((self.image_target.get_size()))
        self.hitbox_target.fill("orange")
        self.rect_target = self.hitbox_target.get_rect()
        self.rect_target.center = self.pos_target
        
        self.start_time_target = pygame.time.get_ticks()
        self.blink_time = pygame.time.get_ticks()

        self.state = "warning"
        self.target_active = True

    def spawn_missile(self):
        self.pos_missile = [self.rect_target.center[0], 0-self.image_missile.get_height()] # fix this so its centered
        self.hitbox_missile = pygame.surface.Surface((self.image_missile.get_size()))
        self.hitbox_missile.fill("orange")
        self.rect_missile = self.hitbox_missile.get_rect()
        self.rect_missile.center = self.pos_missile
     
        self.missile_active = True

    def spawn_explosion(self):
        self.hitbox_explosion = pygame.surface.Surface((self.image_explosion.get_width(), self.image_explosion.get_height()/2))
        self.hitbox_explosion.fill("orange")
        self.pos_explosion = self.pos_missile
        self.rect_explosion = self.hitbox_explosion.get_rect()
        self.rect_explosion.center = self.pos_explosion

        self.start_time_explosion = pygame.time.get_ticks()
        self.explosion_active = True
        self.toggle_hitbox = True

    def update(self, time):
        if self.state == "warning":
            if time >= self.blink_time + 100:
                self.blink_time = time

                self.image_target = pygame.transform.scale_by(self.image_target,1.1)
                self.rect_target = self.image_target.get_rect(center=self.rect_target.center)
                self.pos_target = [self.rect_target[0], self.rect_target[1]]
                self.hitbox_target =  pygame.surface.Surface((self.image_target.get_size()))
                self.hitbox_target.fill("orange")
            
            if time >= self.start_time_target + 1000:
                self.spawn_missile()
                self.state = "waiting"
                self.target_active = True
              

        if self.missile_active:
            self.sprite_missile.animate(time)
          
            if self.pos_missile[1] >= self.pos_target[1] or self.pos_missile[1] + 20 -self.pos_missile[1] <= 0: # fix this later
                self.spawn_explosion()
                self.missile_active = False
                Soundplay("explosion")
            else:
                self.pos_missile = [self.pos_missile[0], self.pos_missile[1] + 20]
                self.rect_missile.center = self.pos_missile

        if self.explosion_active:
            self.target_active = False
            self.missile_active = False
            if time >= self.start_time_explosion + 800:
                self.explosion_active = False
                self.state = "grounded"
            self.sprite_explosion.animate(time)
        
        if self.state == "grounded":
            self.spawn_odds = randint(0,100)
            if self.spawn_odds <= 85:
                self.rarity = "common"
                if self.spawn_odds <= 25:
                    self.rarity  = "rare"
                if self.spawn_odds <= 5:
                    self.rarity  = "legendary"
                self.game.scraps.add(Scraps(self.game, self.display, self.pos_explosion, self.rarity))
            self.kill()
        
        if self.toggle_hitbox:   
            for player in self.game.players:
                if pygame.Rect.colliderect(self.rect_target, player.rect) and player.alive and player.invincibility == False:
                    player.death()

    def draw(self):
        if Utils.debug:
            if self.hitbox_target:
                self.display.blit(self.hitbox_target, self.rect_target)
            if self.hitbox_missile:
                self.display.blit(self.hitbox_missile, self.rect_missile)
            if self.hitbox_explosion:
                self.display.blit(self.hitbox_explosion, [self.pos_explosion[0]-self.image_explosion.get_width()/2, self.rect_missile.midtop[1]])
                
        if self.target_active:
            self.sprite_target.render(self.rect_target, self.image_target)
        if self.missile_active:
            self.sprite_missile.render(self.rect_missile)
        if self.explosion_active:
            self.sprite_explosion.render([self.rect_explosion[0], self.rect_explosion[1]-self.hitbox_explosion.get_height()])


class Scoreboard:
    def __init__(self, game, display, font, players):
        self.game = game
        self.display = display
        self.players = players

        self.font = font

        # player 1
        self.p1_score = str(self.players[0].money)
        self.p1_score_box = font.render(self.p1_score, False, ("#ffe17d"))
        self.p1_shadow = font.render(self.p1_score, False, ("#a33729"))

        # player 1
        self.p2_score = str(self.players[1].money)
        self.p2_score_box = font.render(self.p2_score, False, ("#ffe17d"))
        self.p2_shadow = font.render(self.p2_score, False, ("#a33729"))

    def update(self, players):
        self.players = players

        self.p1_score = str(self.players[0].money)
        self.p1_score_box = self.font.render(self.p1_score, False, ("#ffa9c9"))
        self.p1_shadow = self.font.render(self.p1_score, False, ("#ff317e"))

        # player 1
        self.p2_score = str(self.players[1].money)
        self.p2_score_box = self.font.render(self.p2_score, False, ("#c7efee"))
        self.p2_shadow = self.font.render(self.p2_score, False, ("#37aab5"))


    def draw(self):
        # player 1
        self.display.blit(self.p1_shadow, (20+4, 20+4))  
        self.display.blit(self.p1_score_box, (20,20))
        # player 2
        self.display.blit(self.p2_shadow, (self.display.get_width()-self.p2_score_box.get_width()-20+4, 20+4))  
        self.display.blit(self.p2_score_box, (self.display.get_width()-self.p2_score_box.get_width()-20,20))
                





            
