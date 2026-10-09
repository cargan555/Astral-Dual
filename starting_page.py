
import pygame
import time
import math
from Utils import load_image

text_color = (0,0,0)

def init():
    global cursor_img, font_fin, font_fin_2, y_scroll, background, title, start, start_press, controles, controles_press, credit, credit_press, retour, retour_press

    y_scroll = 0
    
    font_fin = pygame.font.Font('PressStart2P.ttf', 50)
    font_fin_2 = pygame.font.Font('PressStart2P.ttf', 30)
    cursor_img = load_image('Mouse')
    cursor_img = pygame.transform.scale_by(cursor_img, 2)

    background = pygame.image.load("assets/Background.png")

    title = load_image('Logo')
    '''
    title_blue = pygame.image.load("../data/title_blue.png")
    title_green = pygame.image.load("../data/title_green.png")
    title_yellow = pygame.image.load("../data/title_yellow.png")
    title_red = pygame.image.load("../data/title_red.png")
    '''
    start = load_image("Start_button")
    controles = load_image("Controles_button")
    credit = load_image("Credits_button")
    start_press = load_image("Start_pressed")
    controles_press = load_image("Control_pressed")
    credit_press = load_image("Credits_pressed")
    retour = load_image("Retour_button")
    retour_press = load_image("Retour_pressed")
    
    '''
    titles = [title_blue, title_green, title_yellow, title_red]'''
    
def centered_text(screen, text, position, color):
    text = font_fin_2.render(text, True, color)
    pos = (position[0] - text.get_width()//2, position[1] - text.get_height()//2)
    screen.blit(text, pos)

def draw_button(screen, text, position, color):
    text = font_fin_2.render(text, True, (255, 255, 255))
    pos = (position[0] - text.get_width()//2, position[1] - text.get_height()//2)
    rect = pygame.rect.Rect(pos[0]-40, pos[1]-20, text.get_width()+80, text.get_height()+40)
    pygame.draw.rect(screen, color, rect)
    screen.blit(text, pos)

    return rect

def starting_screen(screen, windowWidth, windowHeight, clicked):
    rect = cursor_img.get_rect()
    rect.topleft = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (0,0,0), rect)

    '''
    frame_number = math.floor(time.time()* 3 % 4)
    '''
    
    screen.blit(pygame.transform.scale(background, screen.get_size()), (0,0))

    '''
    screen.blit(pygame.transform.scale(titles[frame_number], (screen.get_size()[0]//2,screen.get_size()[1]//2)), (windowWidth // 4,0))
    '''
    screen.blit(title, (windowWidth // 4,0))

    screen.blit(pygame.transform.scale(start, (windowWidth // 4, windowHeight * 0.4)), (windowWidth //2.7, windowHeight * 0.35))
    screen.blit(pygame.transform.scale(controles, (windowWidth // 4, windowHeight * 0.4)), (windowWidth //2.7, windowHeight * 0.5))
    screen.blit(pygame.transform.scale(credit, (windowWidth // 4, windowHeight * 0.4)), (windowWidth //2.7, windowHeight * 0.65))
    start_rect = (start.get_rect())
    controles_rect = (controles.get_rect())
    credit_rect = (credit.get_rect())
    start_rect[0],start_rect[1],start_rect[2],start_rect[3] = screen.get_size()[0]//2.5, screen.get_size()[1]//2, 67 * 3.5, 50 * 1.5
    controles_rect[0],controles_rect[1],controles_rect[2], controles_rect[3] = screen.get_size()[0]//2.6,screen.get_size()[1]//1.55, 80 * 3.5, 50 * 1.5
    credit_rect[0],credit_rect[1],credit_rect[2], credit_rect[3] = screen.get_size()[0]//2.6,screen.get_size()[1]//1.25, 80 * 3.5, 50 * 1.5
    
    click = None

    if start_rect.collidepoint(rect.topleft):
        screen.blit(pygame.transform.scale(start_press, (windowWidth // 4, windowHeight * 0.4)), (windowWidth //2.7, windowHeight * 0.35))
        if clicked:
            click = 'jouer'

    elif controles_rect.collidepoint(rect.topleft):
        screen.blit(pygame.transform.scale(controles_press, (windowWidth // 4, windowHeight * 0.4)), (windowWidth //2.7, windowHeight * 0.5))
        if clicked:
            click = 'controls'

    elif credit_rect.collidepoint(rect.topleft):
        screen.blit(pygame.transform.scale(credit_press, (windowWidth // 4, windowHeight * 0.4)), (windowWidth //2.7, windowHeight * 0.65))
        if clicked:
            click = 'about'

    screen.blit(cursor_img, rect)
    return click

def controls_screen(screen, windowWidth, windowHeight, clicked):
    rect = cursor_img.get_rect()
    rect.topleft = pygame.mouse.get_pos()

    control = """
QWERTY only!
Player 1: Arrow Keys
Player 2: WASD
""".strip()

    screen.blit(pygame.transform.scale(background, screen.get_size()), (0,0))
    text_y = windowHeight * 0.45
    for line in control.split('\n'):
        centered_text(screen, line, (windowWidth // 2, text_y), (0x2e, 0x22, 0x2f))
        centered_text(screen, line, (windowWidth // 2 - 4, text_y - 4), (255, 255, 255))
        text_y += 48

    screen.blit(pygame.transform.scale(retour, (windowWidth // 4, windowHeight * 0.4)), (windowWidth * 0.74, windowHeight * 0.01))
    retour_rect = (retour.get_rect())
    retour_rect[0],retour_rect[1],retour_rect[2],retour_rect[3] = screen.get_size()[0]//1.3, screen.get_size()[1]//6, 67 * 3.5, 50 * 1.5

    click = None

    if retour_rect.collidepoint(rect.topleft):
        screen.blit(pygame.transform.scale(retour_press, (windowWidth // 4, windowHeight * 0.4)), (windowWidth * 0.74, windowHeight * 0.01))
        if clicked:
            click = 'retour'

    screen.blit(cursor_img, rect)
    return click

def credits_screen(screen, windowWidth, windowHeight, clicked):
    global y_scroll

    rect = cursor_img.get_rect()
    rect.topleft = pygame.mouse.get_pos()

    credit = """
Programing
poof

Art and sprites
se4lly_art
poof

Other assets used
Music - se4lly_art 
Music - OpenGameArt
Police - CodeMan38 (DaFont)

and finaly...
To the Uottawa gamedev club 
for making the game jam

""".strip()

    screen.blit(pygame.transform.scale(background, screen.get_size()), (0,0))
    text_y = windowHeight - 48
    for line in credit.split('\n'):
        centered_text(screen, line, (windowWidth // 2, text_y-y_scroll), (0x2e, 0x22, 0x2f))
        centered_text(screen, line, (windowWidth // 2 - 4, text_y-y_scroll - 4), (255, 255, 255))
        text_y += 48

  
    y_scroll += windowHeight / 500

    screen.blit(pygame.transform.scale(retour, (windowWidth // 4, windowHeight * 0.4)), (windowWidth * 0.74, windowHeight * 0.01))
    retour_rect = (retour.get_rect())
    retour_rect[0],retour_rect[1],retour_rect[2],retour_rect[3] = screen.get_size()[0]//1.3, screen.get_size()[1]//6, 67 * 3.5, 50 * 1.5

    click = None

    if retour_rect.collidepoint(rect.topleft):
        screen.blit(pygame.transform.scale(retour_press, (windowWidth // 4, windowHeight * 0.4)), (windowWidth * 0.74, windowHeight * 0.01))
        if clicked:
            click = 'retour'

    if y_scroll > 48*len(credit.split('\n'))+windowHeight:
        click = 'retour'

    screen.blit(cursor_img, rect)
    return click

def loading_screen(screen, windowWidth, windowHeight):
    screen.fill((0x32, 0x3e, 0x4f))
    centered_text(screen, 'Loading game...', (windowWidth // 2, windowHeight // 2), (255, 255, 255))

