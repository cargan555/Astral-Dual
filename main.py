print("ASTRAL DUAL MAIN.PY STARTED")
import asyncio
import pygame
import Utils
from Utils import *
import starting_page
from phase_1 import Phase_1
from phase_2 import Phase_2
from phase_3 import Phase_3
from phase_4 import Phase_4
from testing import Testing
print("ALL IMPORTS COMPLETED")

''' Requirements
- python 3.14.7
- pygame-ce
https://opengameart.org/content/explosion-0
https://opengameart.org/content/space-theme
https://opengameart.org/content/lunar-echo
https://opengameart.org/content/100-victories
'''
'''Things that could be changed
- stop using rect and hitbox and use 1 thing

'''

class IntroScene:
    def __init__(self, display_dims, display):
        self.display_dims = display_dims
        self.display = display
        
        starting_page.init()
        pygame.mouse.set_visible(False)
        
        Musicplay("spacetheme")
        print("music start")
        music_volume = 0.5
        pygame.mixer.music.set_volume(music_volume)
    
        self.state = 'intro'

    def draw(self):
        mouse_btn_state = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_btn_state = True

        if self.state == 'intro':
            click = starting_page.starting_screen(self.display, *self.display_dims, mouse_btn_state)
            if click == 'jouer':
                self.state = 'jouer'
            elif click == 'controls':
                self.state = 'controls'
            elif click == 'about':
                starting_page.y_scroll = 0
                self.state = 'about'

        elif self.state == 'jouer':
            starting_page.loading_screen(self.display, *self.display_dims)
            return False

        elif self.state == 'controls':
            click = starting_page.controls_screen(self.display, *self.display_dims, mouse_btn_state)
            if click == 'retour':
                self.state = 'intro'

        elif self.state == 'about':
            click = starting_page.credits_screen(self.display, *self.display_dims, mouse_btn_state)
            if click == 'retour':
                self.state = 'intro'

        return True

class GameScene:
    def __init__(self, display, display_dims, clock):

        self.screen = display
        self.display = pygame.Surface(display_dims)
        self.display_dims = display_dims
        self.clock = clock
        self.font = pygame.font.Font('PressStart2P.ttf', 50)
    
        self.score = None
    
        # Variables + Loop
        self.movement = [False, False, False, False]
        
        self.start_p1()

    def start_p1(self):
        pygame.mixer.stop()
        pygame.mixer.music.unload()
        self.phase = 1
        self.display = pygame.Surface((1280, 720))
        self.phase_1 = Phase_1(self, self.display)

    def p1_to_p2(self):
        pygame.mixer.stop()
        pygame.mixer.music.unload()
        self.phase = 2
        self.display = pygame.Surface((1280, 720))
        self.phase_2 = Phase_2(self, self.display, self.phase_1.players)

    def p2_to_p3(self):
        pygame.mixer.stop()
        pygame.mixer.music.unload()

        stats_1 = [item.current * item.value for item in self.phase_2.upgrade_menu_1.items[:-1]]
        stats_2 = [item.current * item.value for item in self.phase_2.upgrade_menu_2.items[:-1]]

        self.phase = 3
        self.display = pygame.Surface((1280, 720))
        self.phase_3 = Phase_3(self, self.display, stats_1, stats_2)       

    def victory(self):
        pygame.mixer.stop()
        pygame.mixer.music.unload()

        if self.phase_3.player_1.score > self.phase_3.player_2.score:
            victor = self.phase_3.player_1.key_set
        elif self.phase_3.player_2.score > self.phase_3.player_1.score:
            victor = self.phase_3.player_2.key_set
        else:
            victor = "tied"
         
        self.phase = 4
        self.display = pygame.Surface((1280, 720))
        self.phase_4 = Phase_4(self, self.display, victor)       


    def testing(self):
        self.phase = "testing" 
        self.display = pygame.Surface((1280,720))
        self.testing = Testing(self)

    def draw(self):
        self.display.fill((0,0,0))

        # Key input handler
        '''  not used for now'''
        mouse_btn_state = False
        keys = pygame.key.get_pressed() 
        key_events = {
            'h': False,
            'left': False,
            'd': False,
            'right': False,
            'a': False,
            'up': False,
            'w': False,
            'down': False,
            's': False,
        }

        # Event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.phase  = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_btn_state = True
            # single keypress, does nothing for now to be used in the future
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_events["left"] = True
                if event.key == pygame.K_RIGHT:
                    key_events["right"] = True
                if event.key == pygame.K_UP:
                    key_events["up"] = True
                if event.key == pygame.K_DOWN:
                    key_events["down"] = True
                if event.key == pygame.K_a:
                    key_events["a"] = True
                if event.key == pygame.K_d:
                    key_events["d"] = True
                if event.key == pygame.K_w:
                    key_events["w"] = True
                if event.key == pygame.K_s:
                    key_events["s"] = True
                        
        # updating 
        if self.phase == 1:
            self.phase_1.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN], 
                                keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s], key_events)
        if self.phase == 2:
            self.phase_2.update(key_events)
        
        if self.phase == 3:
            self.phase_3.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN], 
                                keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s], key_events)

        if self.phase == 4:
            self.phase_4.update()
    
        # drawing 
        if Utils.debug:
            Text_render(f'fps:{self.clock}', self.font, self.display, 0, 0)            

        if self.phase == 1:
            self.screen.blit(self.display, (0,0))
        if self.phase == 2:
            self.screen.blit(self.display, (0,0))
        if self.phase == 3:
            self.screen.blit(self.display, (0 ,0))
        if self.phase == 4:
            self.screen.blit(self.display, (0,0))

        if self.phase == "testing":
            self.testing.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN], 
                                keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s], key_events, mouse_btn_state)
            self.screen.blit(self.display, (0,0))

        return bool(self.phase)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # game window + essentials
        self.width = 1280
        self.height = 720

        self.screen = pygame.display.set_mode((self.width, self.height),)
        self.display = pygame.Surface((1280, 720))
        self.clock = pygame.time.Clock()

    def create_intro(self):
        self.intro_scene = IntroScene((1280,720), self.display)

    def create_game(self):
        self.game_scene = GameScene(self.display, (self.width, self.height), self.clock)

    def Menu(self):
        self.running = self.intro_scene.draw()
        self.screen.blit(self.display, (0,0))
        pygame.display.flip()
        self.clock.tick(60)
        return True

    def Play(self):
        self.running = self.game_scene.draw()
        # self.display.blit(pygame.transform.scale(self.display, (self.width, self.height)), (0,0))
        self.screen.blit(self.display, (0,0))
        pygame.display.flip()
        self.clock.tick(60)
print("MAIN FILE STARTED")

async def main():
    print("MAIN FUNCTION STARTED")

    game = Game()
    print("GAME CREATED")


    game.create_intro()

    game.running = True
    while game.running:
        game.Menu()
        await asyncio.sleep(0)

    print("MENU FINISHED")

    game.create_game()

    game.running = True
    while game.running:
        game.Play()
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())