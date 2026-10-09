
import pygame
from random import randint

class Game:
    def __init__(self):
        # essentials
        pygame.display.set_caption('game')
        
        self.width =  640
        self.height = 480
        
        
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE) # window surface
        self.screen = pygame.Surface((self.width, self.height)) # game surface
        
        pygame.init()
        pygame.mixer.init()
        
        self.fullscreen = False
        self.running = True
        self.clock = pygame.time.Clock()
        
        # classes
        self.tet = Text(self)
        
        # var
        self.texts = ["a micheal jackson parody account", "bro thinks he is slick", "4 am is a reasonable time", "among us", "AMONG US", "self proclaimed king of pop", "how do we live with love?, its cutting, when its never enough, im running to a blank horizon"]
        self.index = -1
        self.time = 0
                
    def update(self):
        while self.running:
            self.screen.fill((0,0,0))
            
            # essential variables:
            pygame.draw.rect(self.screen, (255,0,0), (self.width/2, 0, 1, self.height), 0)
            #self.screen.blit(self.test, self.rect)        
    
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_F4:
                        self.window = pygame.display.set_mode(
                            (self.desktop_width, self.desktop_height), pygame.FULLSCREEN
                        )
                    if event.key == pygame.K_ESCAPE:
                        self.window = pygame.display.set_mode(
                            (self.width, self.height), pygame.RESIZABLE
                        )
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_z:
                        if self.tet.done == True:
                            if self.texts != None and self.texts != []:
                                self.tet.write(self.texts[0],0,0)
                                self.texts.pop(0)
                    if event.key == pygame.K_x:
                        self.tet.skip = True

            self.tet.draw()

            self.scaled = pygame.transform.scale(self.screen, self.window.size)
            self.window.blit(self.scaled, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()

class Text:
    def __init__(self, game):
        self.screen = game.screen 
        self.font = pygame.font.Font('PressStart2P.ttf', 16)
        self.text = None
        self.done = False
        self.bubble = []
        self.max = 24
        self.max_max = self.max
        self.index = 0
        self.x = 2
        self.y = 0
        self.surface =pygame.Surface((220, 100)) # text surfaced
        self.surface.fill((0,255,0))
        self.bubble = pygame.Rect(640/2-10, 480/2-10, 220+20, self.y+10+100)
        self.time = 0
        self.speed = 30
        self.skip = False
   
    def write(self, text, x, y):
        self.surface.fill((0,255,0))
        self.text = []
        self.done = False
        self.x = 0
        self.y = 0
        while len(text) >= self.max:
            while text[self.max] != " ":
                self.max -= 1
            self.text.append(text[:self.max+1])
            text = text[self.max+1:]
            self.max = self.max_max
        self.text.append(text)
        print(self.text)
        
    def draw(self):
        if self.text != None and self.text != []:
            self.rendered = self.font.render(str(self.text[0][self.index]), True, (0,0,0), (0,255,0))
            
            if self.skip == True:
                print(str(self.text[0][:self.index]))
                self.rendered = self.font.render(str(self.text[0][:self.index]), True, (0,0,0), (0,255,0))
                self.surface.blit(self.rendered, self.textRect)
                self.x += 8
                #self.index += 1
            
            self.textRect = [self.x,self.y]
            if pygame.time.get_ticks() >= self.time + self.speed: # text scroll speed
                self.surface.blit(self.rendered, self.textRect)
                self.x += 8
                self.index += 1
                if self.index == len(self.text[0]):
                    self.text.pop(0)
                    self.y += 20
                    self.x = 0
                    self.index = 0
                self.time = pygame.time.get_ticks()
        else:
            self.index = 0
            self.done = True
            self.text = None
        pygame.draw.rect(self.screen, (0,255,0), self.bubble, border_radius=10)
        self.screen.blit(self.surface, (640/2,480/2))
        
        
        
        #self.bubble_spike = ((x-randint(250,280),y-randint(120,160)),(x-200,y+20-200+40),(x-200,y-20-200+40))

game = Game()
game.update()