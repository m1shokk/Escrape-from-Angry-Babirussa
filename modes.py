import pygame
import os
import sys
import json
import importlib
from music_manager import music_manager
import subprocess

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
font_small = pygame.font.Font(None, 24)

# Загрузка фона
background_path = os.path.join("assets/bg", "road.jpg")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Загрузка изображений локаций
highway_path = os.path.join("images/bg_game", "Bg_1.jpg")
forest_path = os.path.join("assets/bg_game", "forest.jpg")

highway_image = pygame.image.load(highway_path)
forest_image = pygame.image.load(forest_path)

highway_image = pygame.transform.scale(highway_image, (300, 150))
forest_image = pygame.transform.scale(forest_image, (300, 150))

# Кнопки локаций
highway_button = pygame.Rect(WIDTH//2 - 320, HEIGHT//2 - 100, 300, 150)
forest_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 - 100, 300, 150)

# Кнопка возврата в меню (одна, по центру внизу)
menu_button = pygame.Rect(WIDTH//2 - 100, HEIGHT - 60, 200, 40)  # Увеличили ширину и опустили ниже

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

def draw_location_buttons():
    """Отрисовка кнопок локаций"""
    mouse_pos = pygame.mouse.get_pos()
    
    # Highway кнопка
    color = LIGHT_GRAY if highway_button.collidepoint(mouse_pos) else GRAY
    pygame.draw.rect(screen, color, highway_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, highway_button, 2, border_radius=15)
    screen.blit(highway_image, highway_button)
    text = font_large.render("Highway", True, BLACK)
    text_rect = text.get_rect(center=highway_button.center)
    screen.blit(text, text_rect)
    
    # Forest кнопка
    color = LIGHT_GRAY if forest_button.collidepoint(mouse_pos) else GRAY
    pygame.draw.rect(screen, color, forest_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, forest_button, 2, border_radius=15)
    screen.blit(forest_image, forest_button)
    text = font_large.render("Forest", True, BLACK)
    text_rect = text.get_rect(center=forest_button.center)
    screen.blit(text, text_rect)

def draw_menu_button():
    """Отрисовка кнопки возврата в главное меню"""
    mouse_pos = pygame.mouse.get_pos()
    color = LIGHT_GRAY if menu_button.collidepoint(mouse_pos) else GRAY
    
    pygame.draw.rect(screen, color, menu_button, border_radius=5)
    pygame.draw.rect(screen, BLACK, menu_button, 2, border_radius=5)
    
    text = font_medium.render("Back to Menu", True, BLACK)
    text_rect = text.get_rect(center=menu_button.center)
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
    """Возврат в главное меню без остановки музыки"""
    import menu
    menu.main()

def load_translations():
    """Загружает переводы для текущего языка"""
    with open("settings.json", "r", encoding="utf-8") as file:
        settings = json.load(file)
    with open("game_translations.json", "r", encoding="utf-8") as file:
        translations = json.load(file)
    return translations[settings["language"]]

def start_game(selected_map, difficulty):
    """Запускает игру с выбранными настройками"""
    try:
        # Сохраняем выбранные настройки
        game_settings = {
            "map": selected_map,
            "difficulty": difficulty
        }
        with open("temp_game_settings.json", "w", encoding="utf-8") as f:
            json.dump(game_settings, f)
        
        # Запускаем игру
        pygame.quit()
        subprocess.Popen([sys.executable, 'game.py'])
    except Exception as e:
        print(f"Error starting game: {e}")

def main():
    """Основная функция выбора режима игры"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Продолжаем воспроизведение музыки из меню
    music_manager.ensure_playing()
    
    # Загружаем переводы
    trans = load_translations()
    
    # Шрифты
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    
    # Константы для дизайна
    BUTTON_COLOR = (220, 220, 220)
    BUTTON_HOVER_COLOR = (200, 200, 200)
    BUTTON_BORDER_COLOR = (100, 100, 100)
    TEXT_COLOR = (50, 50, 50)
    SLIDER_COLOR = (180, 180, 180)
    SLIDER_HANDLE_COLOR = (100, 150, 255)
    START_BUTTON_COLOR = (100, 200, 100)
    START_BUTTON_HOVER_COLOR = (120, 220, 120)
    
    # Создаем кнопки с новым дизайном
    highway_button = pygame.Rect(150, 150, 200, 250)
    forest_button = pygame.Rect(450, 150, 200, 250)
    
    # Кнопка возврата в меню
    back_button = pygame.Rect(30, 30, 100, 40)
    
    # Кнопка запуска игры
    start_button = pygame.Rect(300, 500, 200, 50)
    
    # Слайдер сложности
    slider_rect = pygame.Rect(200, 420, 400, 10)
    handle_rect = pygame.Rect(slider_rect.x, slider_rect.y - 10, 30, 30)
    
    # Загрузка и масштабирование изображений карт
    highway_image = pygame.image.load(os.path.join("images/bg_game", "Bg_1.jpg"))
    forest_image = pygame.image.load(os.path.join("assets/bg_game", "forest.jpg"))
    
    highway_image = pygame.transform.scale(highway_image, (180, 180))
    forest_image = pygame.transform.scale(forest_image, (180, 180))
    
    # Переменные для управления
    dragging = False
    current_difficulty = "medium"
    selected_location = "highway"
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if back_button.collidepoint(mouse_pos):
                    try:
                        pygame.quit()
                        subprocess.Popen([sys.executable, 'menu.py'])
                        return
                    except Exception as e:
                        print(f"Error returning to menu: {e}")
                        continue
                
                elif start_button.collidepoint(mouse_pos):
                    start_game(selected_location, current_difficulty)
                    return
                
                elif highway_button.collidepoint(mouse_pos):
                    selected_location = "highway"
                elif forest_button.collidepoint(mouse_pos):
                    selected_location = "forest"
                
                elif handle_rect.collidepoint(mouse_pos):
                    dragging = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x = event.pos[0]
                handle_rect.centerx = max(slider_rect.left, min(mouse_x, slider_rect.right))
                
                position = (handle_rect.centerx - slider_rect.left) / slider_rect.width
                if position < 0.33:
                    current_difficulty = "easy"
                elif position < 0.66:
                    current_difficulty = "medium"
                else:
                    current_difficulty = "hard"
        
        # Отрисовка
        screen.fill((240, 240, 240))
        
        # Заголовок
        title = font_large.render(trans["select_game_mode"], True, TEXT_COLOR)
        title_rect = title.get_rect(center=(400, 50))
        screen.blit(title, title_rect)
        
        # Отрисовка кнопок карт
        for button, image, text, is_selected in [
            (highway_button, highway_image, trans["highway"], selected_location == "highway"),
            (forest_button, forest_image, trans["forest"], selected_location == "forest")
        ]:
            shadow_rect = button.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(screen, (200, 200, 200), shadow_rect, border_radius=15)
            
            color = BUTTON_HOVER_COLOR if button.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
            if is_selected:
                pygame.draw.rect(screen, SLIDER_HANDLE_COLOR, button, border_radius=15)
            else:
                pygame.draw.rect(screen, color, button, border_radius=15)
            
            pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button, 2, border_radius=15)
            
            image_rect = image.get_rect(center=(button.centerx, button.centery - 30))
            screen.blit(image, image_rect)
            
            text_surface = font_medium.render(text, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(button.centerx, button.bottom - 30))
            screen.blit(text_surface, text_rect)
        
        # Отрисовка слайдера
        pygame.draw.rect(screen, SLIDER_COLOR, slider_rect, border_radius=5)
        pygame.draw.circle(screen, SLIDER_HANDLE_COLOR, handle_rect.center, 15)
        
        # Метки сложности
        difficulties = [(trans["easy"], 0), (trans["medium"], 0.5), (trans["hard"], 1)]
        for text, pos in difficulties:
            x = slider_rect.left + (slider_rect.width * pos)
            text_surface = font_small.render(text, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(x, slider_rect.bottom + 30))
            screen.blit(text_surface, text_rect)
        
        # Кнопка возврата
        mouse_pos = pygame.mouse.get_pos()
        back_color = BUTTON_HOVER_COLOR if back_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, back_color, back_button, border_radius=10)
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, back_button, 2, border_radius=10)
        back_text = font_small.render(trans["back"], True, TEXT_COLOR)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)
        
        # Кнопка запуска игры
        start_color = START_BUTTON_HOVER_COLOR if start_button.collidepoint(mouse_pos) else START_BUTTON_COLOR
        pygame.draw.rect(screen, start_color, start_button, border_radius=15)
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, start_button, 2, border_radius=15)
        start_text = font_medium.render(trans["start"], True, (255, 255, 255))
        start_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()