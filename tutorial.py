import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Platformer")

# CONSTANTS
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

# WINDOW
window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    
    # Loads every file inside the given directory
    images = [f for f in listdir(path) if isfile(join(path, f))]
    
    all_sprites = {}

    # Loops through every image in the directory
    for image in images: 
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        
        
        # Loops through every sprite in the sprite sheet and adds it to the sprites list (doulbe the size of the sprite)
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
            
        # Handles if the sprite is facing left or right. Replaces .png with _right or _left
        if direction: 
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
            
    return all_sprites
    

# PLAYER
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    
    def __init__(self, x, y, width, height):
        # Set player rect to the given x, y, width, and height
        self.rect = pygame.Rect(x, y, width, height)
        # Set player x and y velocity to 0 (not moving)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        
    def move(self, dx, dy):
        # Move the player in the x and y direction
        self.rect.x += dx
        self.rect.y += dy
        
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
            
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        self.fall_count += 1
        
    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, self.rect)

# BACKGROUND
def get_background(name):
    image =  pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    
    # Loop through the width and height of the screen and add the position of each tile to the tiles list
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

# HANDLE MOVE PLAYER
def handle_move_player(player):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)
    

# DRAW
def draw(window, background, bg_image, player):
    for tile in background: 
        window.blit(bg_image, tile)
    
    player.draw(window)
    
    pygame.display.update()

# MAIN GAME LOOP
def main(window):
    clock = pygame.time.Clock()
    bacground, bg_image = get_background("Blue.png")
    
    player = Player(100, 100, 50, 50)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        player.loop(FPS) 
        handle_move_player(player)   
        draw(window, bacground, bg_image, player)

    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main(window)