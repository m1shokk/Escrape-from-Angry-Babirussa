import pygame
import os
import sys
import json
import importlib
from music_manager import music_manager

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Modes - Escape from AB")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 128, 255)

# Шрифты
font_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 36)

# Загрузка фона
background_path = os.path.join("assets/bg", "road.jpg")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Загрузка изображения шоссе
highway_path = os.path.join("images/bg_game", "Bg_1.jpg")
highway_image = pygame.image.load(highway_path)
highway_image = pygame.transform.scale(highway_image, (300, 150))

# Кнопка локации
location_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 100, 300, 150)

# Слайдер сложности
slider_width = 300
slider_height = 10
slider_x = WIDTH//2 - slider_width//2
slider_y = HEIGHT//2 + 100
slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)

# Ползунок слайдера
handle_width = 20
handle_height = 30
handle_x = slider_x + slider_width//2  # Начальная позиция (medium)
handle_rect = pygame.Rect(handle_x - handle_width//2, slider_y - handle_height//4, handle_width, handle_height)

# Сложность
difficulties = ["Easy", "Medium", "Hard"]
current_difficulty = "Medium"
dragging = False

def draw_location_button():
    """Отрисовка кнопки локации"""
    mouse_pos = pygame.mouse.get_pos()
    color = LIGHT_GRAY if location_button.collidepoint(mouse_pos) else GRAY
    
    pygame.draw.rect(screen, color, location_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, location_button, 2, border_radius=15)
    
    # Отображение изображения шоссе
    screen.blit(highway_image, location_button)
    
    # Текст на кнопке
    text = font_large.render("Highway", True, BLACK)
    text_rect = text.get_rect(center=location_button.center)
    screen.blit(text, text_rect)

def draw_difficulty_slider():
    """Отрисовка слайдера сложности"""
    # Линия слайдера
    pygame.draw.rect(screen, GRAY, slider_rect, border_radius=5)
    
    # Ползунок
    pygame.draw.rect(screen, BLUE, handle_rect, border_radius=5)
    
    # Метки сложности
    for i, diff in enumerate(difficulties):
        x = slider_x + (i * slider_width//2)
        text = font_medium.render(diff, True, BLACK)
        text_rect = text.get_rect(center=(x, slider_y - 20))
        screen.blit(text, text_rect)

def get_difficulty_from_position(x):
    """Определение сложности на основе позиции ползунка"""
    first_third = slider_x + slider_width//3
    second_third = slider_x + (slider_width * 2)//3
    
    if x < first_third:
        return "Easy"
    elif x < second_third:
        return "Medium"
    else:
        return "Hard"

def return_to_menu():
    pygame.quit()
    os.execv(sys.executable, ['python'] + ['menu.py'])

def main():
    music_manager.play_menu_music()  # Продолжаем воспроизведение музыки
    global handle_rect, current_difficulty, dragging
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return_to_menu()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Проверка клика на кнопку локации
                    if location_button.collidepoint(event.pos):
                        try:
                            music_manager.stop_music()  # Останавливаем музыку перед запуском игры
                            # Перезагрузка модуля game
                            if 'game' in sys.modules:
                                importlib.reload(sys.modules['game'])
                            import game
                            game.main()
                        except ImportError:
                            print("Game module not found!")
                    
                    # Начало перетаскивания ползунка
                    if handle_rect.collidepoint(event.pos):
                        dragging = True
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    new_x = event.pos[0]
                    # Ограничение движения ползунка
                    if new_x < slider_x:
                        new_x = slider_x
                    elif new_x > slider_x + slider_width:
                        new_x = slider_x + slider_width
                    
                    handle_rect.centerx = new_x
                    current_difficulty = get_difficulty_from_position(new_x)

        # Отрисовка
        screen.blit(background, (0, 0))
        
        # Заголовок
        title = font_large.render("Select Game Mode", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 50))
        screen.blit(title, title_rect)
        
        # Отрисовка элементов
        draw_location_button()
        draw_difficulty_slider()
        
        # Текущая сложность
        diff_text = font_medium.render(f"Selected difficulty: {current_difficulty}", True, BLACK)
        diff_rect = diff_text.get_rect(center=(WIDTH//2, slider_y + 50))
        screen.blit(diff_text, diff_rect)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()