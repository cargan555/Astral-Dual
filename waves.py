from aliens import Basic_alien, Speed_alien

def Single(game, display, x_pos, y_pos, alien_type):
    if alien_type == "basic":
        Basic_alien(game, display, [x_pos+48, y_pos], "R_L")
    elif alien_type == "speed":
        Speed_alien(game, display, [x_pos+48, y_pos], "R_L")

def Vertical(game, display, x_pos, y_pos, alien_type):
    for x in range(0,4):
        if alien_type == "basic":
            Basic_alien(game, display, [x_pos+48, y_pos + 70*x], "R_L")
        elif alien_type == "speed":
            Speed_alien(game, display, [x_pos+48, y_pos + 70*x], "R_L")

def Down_diagonal(game, display, x_pos, y_pos, alien_type):
    for x in range(1,5):
        if alien_type == "basic":
            Basic_alien(game, display, [x_pos+48*x,y_pos+50*x], "R_L")
        elif alien_type == "speed":
            Speed_alien(game, display, [x_pos+48*x,y_pos+50*x], "R_L")

def Up_diagonal(game, display, x_pos, y_pos, alien_type):
    for x in range(1,5):
        if alien_type == "basic":
            Basic_alien(game, display, [x_pos+48*x, y_pos-50*x], "R_L")
        elif alien_type == "speed":
            Speed_alien(game, display, [x_pos+48*x, y_pos-50*x], "R_L")
        
def Square(game, display, x_pos, y_pos, alien_type):
    if alien_type == "basic":    
        Basic_alien(game, display, [x_pos+48, y_pos], "R_L")
        Basic_alien(game, display, [x_pos+48*3,y_pos], "R_L")
        Basic_alien(game, display, [x_pos+48,y_pos + 60], "R_L")
        Basic_alien(game, display, [x_pos+48*3,y_pos + 60], "R_L")
    elif alien_type == "speed":
        Speed_alien(game, display, [x_pos+48, y_pos], "R_L")
        Speed_alien(game, display, [x_pos+48*3,y_pos], "R_L")
        Speed_alien(game, display, [x_pos+48,y_pos + 60], "R_L")
        Speed_alien(game, display, [x_pos+48*3,y_pos + 60], "R_L")
