import pygame
import os
import sys
import json
from music_manager import music_manager

# Инициализация Pygame
pygame.init()

# После инициализации pygame и перед созданием окна
game_icon = pygame.image.load(os.path.join("assets", "logo", "game_logo.jpg"))
pygame.display.set_icon(game_icon)

# Настройка окна
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape from AB")

# Загрузка изображения фона
image_folder = "assets/bg"
image_path = os.path.join(image_folder, "road.jpg")
background_image = pygame.image.load(image_path)

# Настройки
settings_file = "settings.json"
if os.path.exists(settings_file):
    with open(settings_file, "r", encoding="utf-8") as file:
        settings = json.load(file)
else:
    settings = {
        "language": "Русский",  # Язык по умолчанию
        "sound": True  # Звук включен по умолчанию
    }

# Загрузка переводов для меню
def load_menu_translations(language):
    with open("menu_translations.json", "r", encoding="utf-8") as file:
        translations = json.load(file)
    return translations[language]

# Загрузка текущих переводов
menu_translations = load_menu_translations(settings["language"])

# Цвета
text_color = (0, 0, 0)  # Чёрный цвет текста
button_color = (200, 200, 200)
button_hover_color = (170, 170, 170)
button_border_color = (50, 50, 50)

# Шрифты
font = pygame.font.Font(None, 80)  # Для заголовка
button_font = pygame.font.Font(None, 50)  # Для кнопок

# Заголовок
title_text = font.render(menu_translations["title"], True, text_color)
title_rect = title_text.get_rect(center=(400, 150))  # По центру экрана

# Кнопки
button_width, button_height = 200, 60
button_spacing = 50
start_x = (800 - (3 * button_width + 2 * button_spacing)) // 2  # Центрирование кнопок

buttons = {
    "Play": pygame.Rect(start_x, 450, button_width, button_height),
    "Settings": pygame.Rect(start_x + button_width + button_spacing, 450, button_width, button_height),
    "Exit": pygame.Rect(start_x + 2 * (button_width + button_spacing), 450, button_width, button_height),
}

# Текст кнопок
def update_button_texts():
    global button_texts
    button_texts = {
        "Play": button_font.render(menu_translations["play"], True, text_color),
        "Settings": button_font.render(menu_translations["settings"], True, text_color),
        "Exit": button_font.render(menu_translations["exit"], True, text_color),
    }

update_button_texts()

# Функция кнопок
def draw_button(screen, rect, color, border_color, text, hover=False):
    pygame.draw.rect(screen, color, rect, border_radius=15)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=15)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

# Запуск игры
def start_game():
    try:
        from modes import main
        main()
    except ImportError:
        print("Файл modes.py не найден!")

# Открытие настроек
def open_settings():
    try:
        from settings import open_settings
        open_settings()
        # Перезагрузка настроек после возвращения
        with open(settings_file, "r", encoding="utf-8") as file:
            global settings
            settings = json.load(file)
        global menu_translations
        menu_translations = load_menu_translations(settings["language"])
        update_button_texts()
        global title_text
        title_text = font.render(menu_translations["title"], True, text_color)
    except ImportError:
        print("Settings module not found")

# В начале main() или сразу после инициализации pygame:
music_manager.play_menu_music()

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
                    running = False  # Завершение игры
                elif buttons["Play"].collidepoint(mouse_pos):
                    start_game()  # Запуск игры
                elif buttons["Settings"].collidepoint(mouse_pos):
                    open_settings()  # Открытие настроек

    # Рисование фона
    screen.blit(background_image, (0, 0))

    # Рисование заголовка
    screen.blit(title_text, title_rect)

    # Рисование кнопок
    for name, rect in buttons.items():
        mouse_pos = pygame.mouse.get_pos()
        color = button_hover_color if rect.collidepoint(mouse_pos) else button_color
        draw_button(screen, rect, color, button_border_color, button_texts[name])

    # Обновление экрана
    pygame.display.flip()

# Сохранение настроек перед выходом
with open(settings_file, "w", encoding="utf-8") as file:
    json.dump(settings, file, ensure_ascii=False, indent=4)

pygame.quit()
sys.exit()
