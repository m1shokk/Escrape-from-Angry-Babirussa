import pygame
import json
import os
from music_manager import music_manager

class GameOver:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()  # Добавляем инициализацию pygame
        pygame.font.init()  # Добавляем инициализацию шрифтов
        
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game Over - Escape from AB")

        # Загрузка фонового изображения
        self.background = pygame.image.load(os.path.join("assets", "bg", "test", "jakuzi.jpg"))
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)

        # Шрифты
        self.title_font = pygame.font.Font(None, 74)
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

        # Кнопки
        self.button_width = 200
        self.button_height = 50
        self.menu_button = pygame.Rect(self.WIDTH//2 - self.button_width//2, 
                                     self.HEIGHT - 100, 
                                     self.button_width, 
                                     self.button_height)

        # Файл для хранения рекордов
        self.scores_file = "highscores.json"
        self.load_high_score()

    def load_high_score(self):
        """Загрузка лучшего результата из файла"""
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as f:
                data = json.load(f)
                self.high_score = data.get('high_score', 0)
        else:
            self.high_score = 0

    def save_high_score(self, score):
        """Сохранение лучшего результата"""
        if score > self.high_score:
            self.high_score = score
            with open(self.scores_file, 'w') as f:
                json.dump({'high_score': self.high_score}, f)

    def draw_text_centered(self, text, font, color, y_offset):
        """Отрисовка текста по центру"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.WIDTH//2, y_offset))
        self.screen.blit(text_surface, text_rect)

    def show_game_over(self, score, coins, time_played):
        """Показать экран окончания игры"""
        # Сохраняем рекорд, если текущий счет больше
        self.save_high_score(score)
        
        # Включаем музыку меню
        music_manager.play_menu_music()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        if self.menu_button.collidepoint(event.pos):
                            return "menu"

            # Отрисовка фона
            self.screen.blit(self.background, (0, 0))

            # Отрисовка заголовка
            self.draw_text_centered("GAME OVER", self.title_font, self.RED, 100)

            # Отрисовка статистики
            self.draw_text_centered(f"Score: {score}", self.font, self.BLACK, 200)
            self.draw_text_centered(f"Coins collected: {coins}", self.font, self.BLACK, 250)
            self.draw_text_centered(f"Time survived: {time_played} seconds", self.font, self.BLACK, 300)
            self.draw_text_centered(f"High Score: {self.high_score}", self.font, self.BLACK, 350)

            # Отрисовка кнопки
            mouse_pos = pygame.mouse.get_pos()
            button_color = self.GRAY if self.menu_button.collidepoint(mouse_pos) else self.BLACK
            pygame.draw.rect(self.screen, button_color, self.menu_button)
            self.draw_text_centered("Back to Menu", self.small_font, self.WHITE, self.HEIGHT - 75)

            pygame.display.flip()

game_over = GameOver()