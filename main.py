import os
import sys
import time
import enum
import pygame
pygame.font.init()


# Game Variables
game_over = False


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
TILE_FONT = pygame.font.SysFont('arial', 160)
TILE_FONT.set_bold(True)
mm_play_text_W = MAIN_FONT.render("PLAY", 1, WHITE)
mm_play_text_B = MAIN_FONT.render("PLAY", 1, BLACK)
mm_exit_text_W = MAIN_FONT.render("EXIT", 1, WHITE)
mm_exit_text_B = MAIN_FONT.render("EXIT", 1, BLACK)
mm_x_text_W = BIG_FONT.render("X", 1, WHITE)
mm_o_text_W = BIG_FONT.render("O", 1, WHITE)
mm_game_text_B = GAME_FONT.render("GAME", 1, BLACK)


# Button Enum
class MenuButtons(enum.Enum):
    start_button = 0
    exit_button = 1


# Tile Type Enum
class TileType(enum.Enum):
    tile_none = 0
    tile_x = 1
    tile_o = 2


# Tile Object Class
class Tile():
    def __init__(self, x_pos, y_pos, index):
        self.tile_rect = pygame.Rect((x_pos, y_pos), (150, 150))
        self.owner = TileType.tile_none
        self.tile_index = index
        self.tile_text = "None"
        self.text_color = WHITE

    def set_owner(self, new_owner):
        self.owner = new_owner
        if new_owner == TileType.tile_x:
            self.tile_text = "X"
            self.text_color = BLUE
        elif new_owner == TileType.tile_o:
            self.tile_text = "O"
            self.text_color = GREEN

    def return_text(self):
        return TILE_FONT.render(self.tile_text, 1, self.text_color)


# To detect which button is under the mouse
def set_mm_button(mouse_pos):
    # Play Text ----------------------------------------
    if mouse_pos[0] >= 50 and mouse_pos[0] <= 175:
        if mouse_pos[1] >= 250 and  mouse_pos[1] <= 300:
            return MenuButtons.start_button
    # Exit Text ----------------------------------------
    if mouse_pos[0] >= 50 and mouse_pos[0] <= 175:
        if mouse_pos[1] > 300 and  mouse_pos[1] <= 349:
            return MenuButtons.exit_button


# To detect which tile is under the cursor
def get_tile_in_focus(tiles, mouse_pos):
    for tile in tiles:
        if mouse_pos[0] > tile.tile_rect.x and mouse_pos[0] < tile.tile_rect.x + tile.tile_rect.width:
            if mouse_pos[1] > tile.tile_rect.y and mouse_pos[1] < tile.tile_rect.y + tile.tile_rect.height:
                return tile.tile_index


# To place X or O to any tile
def set_tile_type(tiles, tile_in_focus, mouse_pressed):
    if tile_in_focus != None:
        if tiles[tile_in_focus].owner == TileType.tile_none:
            if mouse_pressed == (1,0,0):
                tiles[tile_in_focus].set_owner(TileType.tile_x)
                # To check every time a cell value is changed
                check_nearby_cells(tiles)
            elif mouse_pressed == (0,0,1):
                tiles[tile_in_focus].set_owner(TileType.tile_o)
                # To check every time a cell value is changed
                check_nearby_cells(tiles)
        

# To check the nearby cells to see if they are X or O
def check_nearby_cells(tiles):
    for tile in tiles:
        right,down,down_left,down_right = 0,0,0,0
        search = True
        if tile.owner == TileType.tile_none:
            continue
        while search:
            if right >= 0:
                if right == 3:
                    print(tile.tile_text, "has won the game!")
                    print("Player has won the game with: right")
                    search = False
                    game_over = True
                if tile.tile_index + right <= len(tiles) - 1:
                    if tiles[tile.tile_index + right].owner == tile.owner:
                        right += 1
                    else:
                        right = -1
                else:
                    right = -1
            if down >= 0:
                if down == 3:
                    print(tile.tile_text, "has won the game!")
                    print("Player has won the game with: down")
                    search = False
                    game_over = True
                if tile.tile_index + (down * 3) <= len(tiles) - 1:
                    if tiles[tile.tile_index + (down * 3)].owner == tile.owner:
                        down += 1
                    else:
                        down = -1
                else:
                    down = -1
            if down_right >= 0:
                if down_right == 3:
                    print(tile.tile_text, "has won the game!")
                    print("Player has won the game with: down_right")
                    search = False
                    game_over = True
                if tile.tile_index + (down_right * 4) <= len(tiles) - 1:
                    if tiles[tile.tile_index + (down_right * 4)].owner == tile.owner:
                        down_right += 1
                    else:
                        down_right = -1
                else:
                    down_right = -1
            if down_left >= 0:
                if down_left == 3:
                    print(tile.tile_text, "has won the game!")
                    print("Player has won the game with: down_left")
                    search = False
                    game_over = True
                if tile.tile_index + (down_left * 2) <= len(tiles) - 1:
                    if tiles[tile.tile_index + (down_left * 2)].owner == tile.owner:
                        down_left += 1
                    else:
                        down_left = -1
                else:
                    down_left = -1
            if right == -1 and down == -1 and down_right == -1 and down_left == -1:
                search = False


# Doesn't do anything for now
def handle_player_input(keys_pressed, mouse_pressed, play):
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
                #pygame.draw.rect(SCREEN, RED, tile.tile_rect)
                if tile.owner != TileType.tile_none:
                    SCREEN.blit(tile.return_text(), (tile.tile_rect.x+10, tile.tile_rect.y-10))
            else:
                #pygame.draw.rect(SCREEN, GREEN, tile.tile_rect)
                if tile.owner != TileType.tile_none:
                    SCREEN.blit(tile.return_text(), (tile.tile_rect.x+10, tile.tile_rect.y-10))
        else:
            #pygame.draw.rect(SCREEN, GREEN, tile.tile_rect)
            if tile.owner != TileType.tile_none:
                    SCREEN.blit(tile.return_text(), (tile.tile_rect.x+10, tile.tile_rect.y-10))

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
    tile0 = Tile(0, 0, 0)
    tile1 = Tile(150, 0, 1)
    tile2 = Tile(300, 0, 2)
    tile3 = Tile(0, 150, 3)
    tile4 = Tile(150, 150, 4)
    tile5 = Tile(300, 150, 5)
    tile6 = Tile(0, 300, 6)
    tile7 = Tile(150, 300, 7)
    tile8 = Tile(300, 300, 8)
    tiles = [tile0, tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8]
    tile_in_focus = None
    
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
        handle_player_input(keys_pressed, mouse_pressed, play)
        
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
                    time.sleep(0.5)
            # Exit button
            if mm_button_in_focus == MenuButtons.exit_button:
                if mouse_pressed == (1,0,0):
                    run = False
                    pygame.quit()
                    sys.exit()
            #print(mm_button_in_focus)
        else:
            tile_in_focus = get_tile_in_focus(tiles, mouse_pos)
            if not game_over:
                set_tile_type(tiles, tile_in_focus, mouse_pressed)
            
            update_display1(tiles, mouse_pos)
            #print(tile_in_focus)
            
    main()




if __name__ == "__main__":
    main()



