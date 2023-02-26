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

# SPRITES
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

# Grabs the block image from the terrain.png file. 96, 0 is the x and y position of the block in the sprite sheet
def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
    
    
# PLAYER
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 4
    
    def __init__(self, x, y, width, height):
        super().__init__()
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
            
    # Player loop
    def loop(self, fps):
        # self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        self.fall_count += 1
        self.update_sprite()
        self.update()
        
    # Animate sprites
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "run"
            
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = self.animation_count // self.ANIMATION_DELAY % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
    
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def draw(self, window):
        window.blit(self.sprite, (self.rect.x, self.rect.y))

# Define a class for all objects in the game
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

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
def draw(window, background, bg_image, player, objects):
    for tile in background: 
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window)
    
    player.draw(window)
    
    pygame.display.update()

# MAIN GAME LOOP
def main(window):
    clock = pygame.time.Clock()
    bacground, bg_image = get_background("Blue.png")
    
    block_size = 96
    
    player = Player(100, 100, 50, 50)
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    blocks = [Block(0, HEIGHT - block_size, block_size)]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        player.loop(FPS) 
        handle_move_player(player)   
        draw(window, bacground, bg_image, player, floor)

    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main(window)