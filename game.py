import pygame
import os
import sys
from pygame.locals import *

pygame.init()

#Ouverture de la fenêtre Pygame
screen = pygame.display.set_mode((800, 600))

#Chargement et collage du fond
image_folder = "images/bg"
image_path = os.path.join(image_folder, "top.jpg")
background_image = pygame.image.load(image_path)

#Chargement et collage du personnage
perso_folder = "images/animations/player"
perso = os.path.join(perso_folder, "Run_1.png")
perso_image = pygame.image.load(perso)

#Rafraîchissement de l'écran
screen.blit(background_image, (0, 0))

#BOUCLE INFINIE
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
