import pygame
import os
import sys

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape from AB")

# Загрузка изображения фона с относительным путём
image_folder = "images/bg"
image_path = os.path.join(image_folder, "road.jpg")
background_image = pygame.image.load(image_path)

# Цвета
text_color = (0, 0, 0)  # Чёрный цвет текста
button_color = (200, 200, 200)  # Светло-серый цвет кнопок
button_hover_color = (170, 170, 170)  # Цвет кнопки при наведении
button_border_color = (50, 50, 50)  # Цвет рамки кнопки


# Шрифты
font = pygame.font.Font(None, 80)  # Для заголовка
button_font = pygame.font.Font(None, 50)  # Для кнопок

# Заголовок
title_text = font.render("Escape from AB", True, text_color)
title_rect = title_text.get_rect(center=(400, 150))  # По центру экрана

# Кнопки
button_width, button_height = 200, 60
button_spacing = 50
start_x = (800 - (3 * button_width + 2 * button_spacing)) // 2  # Начальная координата X для центрирования

buttons = {
    "Play": pygame.Rect(start_x, 450, button_width, button_height),
    "Settings": pygame.Rect(
        start_x + button_width + button_spacing, 450, button_width, button_height
    ),
    "Exit": pygame.Rect(
        start_x + 2 * (button_width + button_spacing), 450, button_width, button_height
    ),
}

# Текст кнопок
button_texts = {name: button_font.render(name, True, text_color) for name in buttons}

# Функция кнопок
def draw_button(screen, rect, color, border_color, text, hover=False):
    pygame.draw.rect(screen, color, rect, border_radius=15)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=15)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

# Функция запуска другого кода
def start_game():
    game_path = "game.py"
    if os.path.exists(game_path):
        os.system(f"python {game_path}")  # Запуск game.py
    else:
        print("Файл game.py не найден!")

from settings import open_settings

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                mouse_pos = pygame.mouse.get_pos()
                if buttons["Exit"].collidepoint(mouse_pos):
                    running = False  # Завершить игру
                elif buttons["Play"].collidepoint(mouse_pos):
                    start_game()  # Запуск игры
                elif buttons["Settings"].collidepoint(mouse_pos):
                    open_settings()

    # Рисование фона
    screen.blit(background_image, (0, 0))

    # Рисование заголовка
    screen.blit(title_text, title_rect)

    # Рисование кнопок
    for name, rect in buttons.items():
        mouse_pos = pygame.mouse.get_pos()
        color = button_hover_color if rect.collidepoint(mouse_pos) else button_color
        draw_button(screen, rect, color, button_border_color, button_texts[name])
        button_text = button_texts[name]
        text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, text_rect)

    # Обновление экрана
    pygame.display.flip()

# Завершение Pygame
pygame.quit()
sys.exit()
