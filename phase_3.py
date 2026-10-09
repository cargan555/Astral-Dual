import Utils
from Utils import *
from player import Player_3
from aliens import Speed_alien
from waves import *
import pygame

class Phase_3:
    def __init__(self, game, display, player_1_stats, player_2_stats): 
        # essentials
        ''' all of the game parameters in classes exlucing this one are actualy just the phase_1 class'''
        self.game = game
        self.display = display
        self.font = pygame.font.Font('PressStart2P.ttf', 30)

        self.players = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bullets_players = pygame.sprite.Group()
        self.bullets_aliens = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group() # delete me later
        
        # assets
        self.background = Background(self, self.display)
        self.player_sprite_1 = Assets(self.display, "Pink_ship", None, (64, 64))
        self.player_sprite_2 = Assets(self.display, "Blue_ship", None, (64,64))

        self.basic_alien = Assets(self.display, "Basic alien", None, (16*4, 16*4))
        self.speed_alien = Assets(self.display, "Speed_alien", None, (32*3, 16*3))

        self.b_bullet = Assets(self.display, "Blue_bullet", None, (32, 4*4))
        self.p_bullet = Assets(self.display, "Pink_bullet", None, (32, 4*4))
        self.basic_bullet = Assets(self.display, "Basic_bullet", None, (32, 4*4))

        # objects
        self.player_1 = Player_3(self, self.display, 100,300, player_1_stats, "arrow")
        self.player_2 = Player_3(self, self.display, 100,600, player_2_stats, "wasd")
        self.ui = Scoreboard(self.game, self.display, self.font, [self.player_1, self.player_2])
       
        # variables
        self.time = 0

        self.wave_1()

        self.start_wave_2 = pygame.time.get_ticks() + 24000
        self.end_wave = pygame.time.get_ticks() + 28000

    def update(self, Left, Right, Up, Down, A, D, W, S, keys):
        self.display.fill((0,0,0))
        self.time = pygame.time.get_ticks()

        if self.time >= self.start_wave_2:
            self.wave_2()
            self.start_wave_2 = 1000000000

        if self.time >= self.end_wave:
            self.game.victory()
            self.end_wave = 1000000000

        if self.player_1.lives <= 0 and self.player_2.lives <= 0:
            self.game.victory()

        for player in self.players:
            if player.alive:
                if self.time >= player.spawn_rate + player.fire_rate*100:
                    player.spawn_rate = self.time
                    self.bullets_players.add(Bullet_player(self, self.display, player.pos[0], player.pos[1], player.key_set))

        # update
        self.background.update()
        self.players.update(Left, Right, Up, Down, A, D, W, S, keys)
        self.bullets_players.update(self.time)
        self.bullets_aliens.update(self.time)
        self.aliens.update()
        self.ui.update()
        
        # drawing
        self.draw()

    def draw(self):
        self.background.draw()
        for bullet in self.bullets_aliens:
            bullet.draw()
        for bullet in self.bullets_players:
            bullet.draw()
        for alien in self.aliens:
            alien.draw()
        for player in self.players:
            player.draw()
        self.ui.draw()

    def wave_1(self):
        self.spawn_time = pygame.time.get_ticks()

        Up_diagonal(self, self.display, 1280, 670, "basic")
        Down_diagonal(self, self.display, 1280, 50, "basic")

        Vertical(self, self.display, 2080, 720/2-50*2, "basic")

        for x in range(3):
            Square(self, self.display, 2800+200*x, 470-100*x, "basic")

        for x in range(10):
            Single(self, self.display, randint(0,400)*2 + 3800, randint(50, 670), "basic")

        Vertical(self, self.display, 4400, 720/2-50*2, "basic")

    def wave_2(self):
        Speed_alien(self, self.display, [1280, 320], "R_L",)
        Speed_alien(self, self.display, [1280, 620], "R_L",)
        
        Square(self, self.display, 1500, 400, "speed")
              

class Bullet_player(pygame.sprite.Sprite):
    def __init__(self, game, display, x, y, key_set):
        # essentials
        self.groups = game.bullets_players
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.display = display

        self.key_set = key_set
        # assets
        if key_set == "arrow":
            self.sprite = self.game.p_bullet
        if key_set == "wasd":
            self.sprite = self.game.b_bullet
        self.image = self.sprite.get_sprite()

        self.hitbox = pygame.Surface(self.image.get_size())
        self.hitbox.fill("yellow")

        self.rect = self.hitbox.get_rect()
        self.pos = [x,y]
        self.rect.center = self.pos

        #  varriables
        self.bullet_speed = 10
        self.bullet_time = 0

    def update(self, time):
        self.bullet_time = time
        if self.pos[0] <= self.display.get_width():
            self.pos[0] += 1*self.bullet_speed
        else:
            self.kill()
        self.rect.center = self.pos

    def draw(self):
        if Utils.debug:
            self.sprite.render(self.rect)
        self.display.blit(self.image, self.rect)


class Background():
    def __init__(self, game, display):
        self.game = game
        self.display = display

        self.sprite = Assets(self.display, "Pixelart_starfield", None, (1280,720))
        self.image = self.sprite.get_sprite()

        self.pos_1 = [0,0]
        self.pos_2 = [1280,0]

        self.scroll_speed = 2

    def update(self):
        self.pos_1[0] -= self.scroll_speed
        if self.pos_1[0] <= -1280:
            self.pos_1[0] = 1280

        self.pos_2[0] -= self.scroll_speed
        if self.pos_2[0] <= -1280:
            self.pos_2[0] = 1280

    def draw(self):
        self.sprite.render(self.pos_1)
        self.sprite.render(self.pos_2)

   
class Scoreboard:
    def __init__(self, game, display, font, players):
        self.game = game
        self.display = display
        self.players = players

        self.font = font

        self.hearts_1 = []
        self.hearts_2 = []

        for x in range(players[0].lives):
            self.hearts_1.append(Heart(self.display, [20+40*x, 20], self.players[0])) 
        self.hearts_1.append(Score_counter(self.display, self.font, [0+40*(self.players[0].lives), 20-15], self.players[0]))

        for x in range(players[1].lives):
            self.hearts_2.append(Heart(self.display, [20+40*x, 60], self.players[1]))   
        self.hearts_2.append(Score_counter(self.display, self.font, [0+40*(self.players[1].lives), 60-15], self.players[1]))
    
    def update(self,):

        self.hearts_1 = []
        self.hearts_2 = []

        for x in range(self.players[0].lives):
            self.hearts_1.append(Heart(self.display, [20+40*x, 20], self.players[0])) 
        self.hearts_1.append(Score_counter(self.display, self.font, [10+40*(self.players[0].lives), 20-15], self.players[0]))

        for x in range(self.players[1].lives):
            self.hearts_2.append(Heart(self.display, [20+40*x, 60], self.players[1]))   
        self.hearts_2.append(Score_counter(self.display, self.font, [10+40*(self.players[1].lives), 60-15], self.players[1]))
            
    def draw(self):
        for heart in self.hearts_1:
            heart.draw()
        for heart in self.hearts_2:
            heart.draw()

class Heart:
    def __init__(self, display, pos, player):
        self.display = display

        if player.key_set == "wasd":
            self.sprite = Assets(self.display, "Blue_health", None, (16*2,16*2))
        elif player.key_set == "arrow":
            self.sprite = Assets(self.display, "Pink_health", None, (16*2, 16*2))
        self.image = self.sprite.get_sprite()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos

    def draw(self):
        self.sprite.render(self.rect)

class Score_counter:
    def __init__(self, display, font, pos, player):
        self.display = display
        self.font = font

        self.player = player
        self.pos = pos

        if self.player.key_set == "arrow":
            self.score = str(self.player.score)
            self.score_box = self.font.render(self.score, False, ("#ffa9c9"))
            self.shadow = self.font.render(self.score, False, ("#ff317e"))
        if self.player.key_set == "wasd":
            self.score = str(self.player.score)
            self.score_box = self.font.render(self.score, False, ("#c7efee"))
            self.shadow = self.font.render(self.score, False, ("#37aab5"))

    def update(self):
        if self.player.key_set == "arrow":
            self.score = str(self.player.score)
            self.score_box = self.font.render(self.score, False, ("#ffa9c9"))
            self.shadow = self.font.render(self.score, False, ("#ff317e"))
        if self.player.key_set == "wasd":
            self.score = str(self.player.score)
            self.score_box = self.font.render(self.score, False, ("#c7efee"))
            self.shadow = self.font.render(self.score, False, ("#37aab5"))

    def draw(self):
        self.display.blit(self.shadow, [self.pos[0]+4, self.pos[1]+4])  
        self.display.blit(self.score_box, self.pos)
        

# add other aliens
# add enemi ship explode
# ajouter animatinos joueur