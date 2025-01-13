import pygame
import sys

#Инициализация PyGame
pygame.init()

#Установка размеров окна
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Escrape from Angry Babirussa") 

#Фон
background_image = pygame.image.load("images/bg/source/999.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
#Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
    #Отображение фона
    screen.blit(background_image, (0, 0))
    #Обновление экрана
    pygame.display.flip()

pygame.quit()
sys.exit()
