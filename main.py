import os
import sys
import enum
import pygame
pygame.font.init()


# Screen Variables
HEIGHT, WIDTH = 450, 450
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60


# Color Variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Text Variables
MAIN_FONT = pygame.font.SysFont('arial', 50)
GAME_FONT = pygame.font.SysFont('arial', 40)
GAME_FONT.set_bold(True)
BIG_FONT = pygame.font.SysFont('arial', 120)
BIG_FONT.set_bold(True)
mm_play_text_W = MAIN_FONT.render("PLAY", 1, WHITE)
mm_play_text_B = MAIN_FONT.render("PLAY", 1, BLACK)
mm_exit_text_W = MAIN_FONT.render("EXIT", 1, WHITE)
mm_exit_text_B = MAIN_FONT.render("EXIT", 1, BLACK)
mm_x_text_W = BIG_FONT.render("X", 1, WHITE)
mm_o_text_W = BIG_FONT.render("O", 1, WHITE)
mm_game_text_B = GAME_FONT.render("GAME", 1, BLACK)


class MenuButtons(enum.Enum):
    start_button = 0
    exit_button = 1


class TileType(enum.Enum):
    tile_none = 0
    tile_x = 1
    tile_o = 2


class Tile():
    def __init__(self, x_pos, y_pos):
        self.tile_rect = pygame.Rect((x_pos, y_pos), (150, 150))
        self.owner = TileType.tile_none
        


def set_mm_button(mouse_pos):
    # Play Text ----------------------------------------
    if mouse_pos[0] >= 50 and mouse_pos[0] <= 175:
        if mouse_pos[1] >= 250 and  mouse_pos[1] <= 300:
            return MenuButtons.start_button
    # Exit Text ----------------------------------------
    if mouse_pos[0] >= 50 and mouse_pos[0] <= 175:
        if mouse_pos[1] > 300 and  mouse_pos[1] <= 349:
            return MenuButtons.exit_button


def handle_player_input(keys_pressed, mouse_pressed):
    pass


# Update the Main Menu screen
def update_display0(mouse_pos, play_rect, exit_rect, game_rect):
    # Always at the top --------------------------------
    SCREEN.fill(BLACK)

    # XOX Logo -----------------------------------------
    SCREEN.blit(mm_x_text_W, (50, 50))
    SCREEN.blit(mm_o_text_W, (120, 50))
    SCREEN.blit(mm_x_text_W, (203, 50))
    pygame.draw.rect(SCREEN, WHITE, game_rect)
    SCREEN.blit(mm_game_text_B, (155, 157.5))

    # Play Text ----------------------------------------
    if mouse_pos[0] >= 50 and mouse_pos[0] <= 175:
        if mouse_pos[1] >= 250 and  mouse_pos[1] <= 300:
            pygame.draw.rect(SCREEN, WHITE, play_rect)
            SCREEN.blit(mm_play_text_B,(50, 250))
        else:
            pygame.draw.rect(SCREEN, BLACK, play_rect)
            SCREEN.blit(mm_play_text_W,(50, 250))
    else:
        pygame.draw.rect(SCREEN, BLACK, play_rect)
        SCREEN.blit(mm_play_text_W,(50, 250))
    # Exit Text ----------------------------------------
    if mouse_pos[0] >= 50 and mouse_pos[0] <= 175:
        if mouse_pos[1] > 300 and  mouse_pos[1] <= 350:
            pygame.draw.rect(SCREEN, WHITE, exit_rect)
            SCREEN.blit(mm_exit_text_B,(50, 300))
        else:
            pygame.draw.rect(SCREEN, BLACK, exit_rect)
            SCREEN.blit(mm_exit_text_W,(50, 300))
    else:
        pygame.draw.rect(SCREEN, BLACK, exit_rect)
        SCREEN.blit(mm_exit_text_W,(50, 300))


    # Always at the bottom -----------------------------
    pygame.display.update()


# Update the Game screen
def update_display1(tiles, mouse_pos):
    # Always at the top --------------------------------
    SCREEN.fill(BLACK)

    # Tiles
    for tile in tiles:
        if mouse_pos[0] > tile.tile_rect.x and mouse_pos[0] < tile.tile_rect.x + tile.tile_rect.width:
            if mouse_pos[1] > tile.tile_rect.y and mouse_pos[1] < tile.tile_rect.y + tile.tile_rect.height:
                pygame.draw.rect(SCREEN, RED, tile.tile_rect)
            else:
                pygame.draw.rect(SCREEN, GREEN, tile.tile_rect)
        else:
            pygame.draw.rect(SCREEN, GREEN, tile.tile_rect)

    # Horizontal Lines
    pygame.draw.line(SCREEN, WHITE, (0, 3), (450, 3) ,5)
    pygame.draw.line(SCREEN, WHITE, (0, 150), (450, 150) ,5)
    pygame.draw.line(SCREEN, WHITE, (0, 300), (450, 300) ,5)
    pygame.draw.line(SCREEN, WHITE, (0, 446), (450, 446) ,5)
    # Vertical Lines
    pygame.draw.line(SCREEN, WHITE, (2, 3), (2, 446) ,5)
    pygame.draw.line(SCREEN, WHITE, (150, 3), (150, 446) ,5)
    pygame.draw.line(SCREEN, WHITE, (300, 3), (300, 446) ,5)
    pygame.draw.line(SCREEN, WHITE, (447, 3), (447, 446) ,5)

    # Always at the bottom -----------------------------
    pygame.display.update()


def main():

    # Main menu buttons
    play_rect = pygame.Rect((50, 250), (125, 50))
    exit_rect = pygame.Rect((50, 300), (125, 50))
    game_rect = pygame.Rect((149,159), (145, 40))
    mm_button_in_focus = None
    
    # Cursor
    hide_cursor = False

    # Initialize Tiles
    tile0 = Tile(0, 0)
    tile1 = Tile(150, 0)
    tile2 = Tile(300, 0)
    tile3 = Tile(0, 150)
    tile4 = Tile(150, 150)
    tile5 = Tile(300, 150)
    tile6 = Tile(0, 300)
    tile7 = Tile(150, 300)
    tile8 = Tile(300, 300)
    tiles = [tile0, tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8]
    
    clock = pygame.time.Clock()
    
    run = True
    play = False
    
    while run:
        
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        # To get input from player
        keys_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # To handle player input
        handle_player_input(keys_pressed, mouse_pressed)
        
        # To change scene
        if not play:
            if hide_cursor  == False:
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)
            mm_button_in_focus = set_mm_button(mouse_pos)
            update_display0(mouse_pos, play_rect, exit_rect, game_rect)
            # Start button
            if mm_button_in_focus == MenuButtons.start_button:
                if mouse_pressed == (1,0,0):
                    play = True
            # Exit button
            if mm_button_in_focus == MenuButtons.exit_button:
                if mouse_pressed == (1,0,0):
                    run = False
                    pygame.quit()
                    sys.exit()
            #print(mm_button_in_focus)
        else:
            update_display1(tiles, mouse_pos)
            
    main()




if __name__ == "__main__":
    main()



