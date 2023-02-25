import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Platformer")

# BACKGROUND
BG_COLOR = (255, 255, 255)

# CONSTANTS
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

# WINDOW
window = pygame.display.set_mode((WIDTH, HEIGHT))

# MAIN GAME LOOP
def main(window):
    pass
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main(window)