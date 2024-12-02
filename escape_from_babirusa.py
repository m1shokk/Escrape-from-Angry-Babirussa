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
background_image = pygame.image.load("images/bg/test/999.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Цвета
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

# Шрифт
title_font = pygame.font.Font(None, 80)  # Для заголовка
button_font = pygame.font.Font(None, 50)  # Для кнопок

# Текст заголовка
title_text = title_font.render("Escape from Angry Babirussa", True, WHITE)

# Кнопки
buttons = {
    "Play": pygame.Rect(screen_width // 2 - 100, screen_height - 200, 200, 50),
    "Settings": pygame.Rect(screen_width // 2 - 100, screen_height - 130, 200, 50),
    "Exit": pygame.Rect(screen_width // 2 - 100, screen_height - 60, 200, 50),
}

def draw_menu():
    # Отображение фона
    screen.blit(background_image, (0, 0))
    
    # Отображение заголовка
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
    
    # Отображение кнопок
    for button_text, button_rect in buttons.items():
        pygame.draw.rect(screen, GRAY, button_rect)  # Рисуем кнопку
        text_surface = button_font.render(button_text, True, WHITE)
        screen.blit(text_surface, (button_rect.x + button_rect.width // 2 - text_surface.get_width() // 2,
                                   button_rect.y + button_rect.height // 2 - text_surface.get_height() // 2))


#Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # Позиция мыши
            if buttons["Play"].collidepoint(mouse_pos):
                print("Play button clicked!")  # Здесь можно будет запустить игру
            elif buttons["Settings"].collidepoint(mouse_pos):
                print("Settings button clicked!")  # Здесь можно будет открыть настройки
            elif buttons["Exit"].collidepoint(mouse_pos):
                print("Exit button clicked!")
                running = False  # Закрываем игру
    
    draw_menu()  # Отрисовка меню
    pygame.display.flip()  # Обновление экрана

pygame.quit()
sys.exit()
