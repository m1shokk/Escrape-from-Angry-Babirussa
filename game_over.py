import pygame
import json
import os
import sys
from music_manager import music_manager
import settings

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Константы
WIDTH = 800
HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BUTTON_COLOR = (220, 220, 220)
BUTTON_HOVER_COLOR = (200, 200, 200)
BUTTON_BORDER_COLOR = (100, 100, 100)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Over - Escape from AB")
clock = pygame.time.Clock()

# Шрифты
title_font = pygame.font.Font(None, 74)
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Загрузка фонового изображения
try:
    background_image = pygame.image.load(os.path.join("assets", "bg", "test", "jakuzi.jpg"))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Error loading background: {e}")
    background_image = pygame.Surface((WIDTH, HEIGHT))
    background_image.fill(BLACK)

def get_high_score():
    try:
        with open("records.json", "r") as f:
            records = json.load(f)
            if records:
                return max(record["score"] for record in records)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0
    return 0

def show_game_over_screen(score, time_played, coins_collected):
    """Показывает экран окончания игры"""
    music_manager.play_menu_music()
    
    high_score = get_high_score()
    is_new_record = score > high_score
    entering_name = is_new_record
    name = ""
    show_menu_button = not is_new_record
    
    # Кнопка возврата в меню
    menu_button = pygame.Rect(WIDTH//2 - 100, HEIGHT - 100, 200, 50)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if entering_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip():
                        try:
                            # Получаем текущую карту из настроек
                            with open("temp_game_settings.json", "r") as f:
                                game_settings = json.load(f)
                                current_map = game_settings.get("map", "highway")
                            
                            settings.add_new_record(
                                score=score,
                                map_name=current_map,
                                time_played=time_played,
                                coins_collected=coins_collected,
                                record_name=name
                            )
                        except Exception as e:
                            print(f"Error saving record: {e}")
                        entering_name = False
                        show_menu_button = True
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 20 and event.unicode.isprintable():
                            name += event.unicode
                            
            elif show_menu_button:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_button.collidepoint(event.pos):
                        try:
                            pygame.quit()
                            import subprocess, sys
                            subprocess.Popen([sys.executable, 'menu.py'])
                            return
                        except Exception as e:
                            print(f"Error returning to menu: {e}")
        
        # Отрисовка
        screen.blit(background_image, (0, 0))
        
        # Заголовок
        title_text = "NEW RECORD!" if is_new_record else "GAME OVER!"
        title_color = RED if is_new_record else WHITE
        title_surface = title_font.render(title_text, True, title_color)
        screen.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 100))
        
        # Статистика
        stats = [
            f"Score: {score}",
            f"Best Score: {high_score}",
            f"Time: {time_played:.1f} sec",
            f"Coins: {coins_collected}"
        ]
        
        for i, stat in enumerate(stats):
            text = font.render(stat, True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i*50))
        
        if entering_name:
            prompt = small_font.render("Enter your name:", True, WHITE)
            name_surface = small_font.render(name + "|", True, WHITE)
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 400))
            screen.blit(name_surface, (WIDTH//2 - name_surface.get_width()//2, 450))
            
        if show_menu_button:
            mouse_pos = pygame.mouse.get_pos()
            button_color = BUTTON_HOVER_COLOR if menu_button.collidepoint(mouse_pos) else BUTTON_COLOR
            
            pygame.draw.rect(screen, button_color, menu_button, border_radius=15)
            pygame.draw.rect(screen, BUTTON_BORDER_COLOR, menu_button, 2, border_radius=15)
            
            menu_text = small_font.render("Back to Menu", True, BLACK)
            text_rect = menu_text.get_rect(center=menu_button.center)
            screen.blit(menu_text, text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)