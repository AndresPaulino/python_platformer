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

# PLAYER
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    def __init__(self, x, y, width, height):
        # Set player rect to the given x, y, width, and height
        self.rect = pygame.Rect(x, y, width, height)
        # Set player x and y velocity to 0 (not moving)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        
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

# DRAW
def draw(window, background, bg_image):
    for tile in background: 
        window.blit(bg_image, tile)
    
    pygame.display.update()

# MAIN GAME LOOP
def main(window):
    run = True
    clock = pygame.time.Clock()
    bacground, bg_image = get_background("Blue.png")

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        draw(window, bacground, bg_image)

    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main(window)