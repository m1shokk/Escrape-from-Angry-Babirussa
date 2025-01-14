import pygame
import os
import sys
from settings import open_settings  # Импортируем меню настроек из settings.py

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape from AB")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PAUSE_BUTTON_COLOR = (0, 128, 255)
PAUSE_BUTTON_HOVER_COLOR = (0, 102, 204)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Пути
player_path = "./images/animations/player"
babirussa_path = "./images/animations/babirussa"
background_path = "./images/bg_game"

# Загрузка изображений фона
background_image = pygame.image.load(os.path.join(background_path, "Bg_1.jpg"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Загрузка анимаций игрока
player_run_images = [
    pygame.image.load(os.path.join(player_path, f"Run_{i}.png")) for i in range(1, 3)
]
player_jump_image = pygame.image.load(os.path.join(player_path, "Jump_player.png"))
player_crouch_image = pygame.image.load(os.path.join(player_path, "Crouch_player.png"))

# Загрузка анимаций бабируссы
babirussa_run_images = [
    pygame.image.load(os.path.join(babirussa_path, f"run_{i}.png")) for i in range(1, 3)
]

# Масштабирование изображений
player_run_images = [pygame.transform.scale(img, (100, 100)) for img in player_run_images]
player_jump_image = pygame.transform.scale(player_jump_image, (100, 100))
player_crouch_image = pygame.transform.scale(player_crouch_image, (100, 100))

babirussa_run_images = [pygame.transform.scale(img, (100, 100)) for img in babirussa_run_images]

# Скорости
BACKGROUND_SPEED = 5
PLAYER_SPEED = 3
BABIRUSSA_SPEED = PLAYER_SPEED  # Бабирусса двигается с той же скоростью, что и игрок

# Переменные
background_x = 0  # Координата фона
player_x, player_y = 200, 400
babirussa_x, babirussa_y = 100, 400  # Начальная позиция бабируссы на 1/4 экрана позади игрока

# Анимация
player_frame = 0
babirussa_frame = 0
player_state = "run"  # Состояния: run, jump, crouch

# Таймер для анимации бабируссы (чтобы менять её кадры медленно)
babirussa_animation_time = 0.5  # Увеличена задержка между сменами кадров
last_babirussa_change_time = 0

# Таймер
start_time = pygame.time.get_ticks()

# Переменные для паузы
paused = False
pause_button_hovered = False

# Шрифты
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 60)

# Кнопки паузы
pause_button = pygame.Rect(WIDTH - 100, 20, 80, 40)
resume_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 60)
settings_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)
quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 60)

def draw_text(text, font, color, x, y):
    """Отображение текста на экране."""
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_pause_menu():
    pygame.draw.rect(screen, WHITE, resume_button)
    pygame.draw.rect(screen, WHITE, settings_button)
    pygame.draw.rect(screen, WHITE, quit_button)
    
    draw_text("Resume", button_font, BLACK, resume_button.centerx - 70, resume_button.centery - 20)
    draw_text("Settings", button_font, BLACK, settings_button.centerx - 80, settings_button.centery - 20)
    draw_text("Quit", button_font, BLACK, quit_button.centerx - 50, quit_button.centery - 20)

def check_pause_menu_click(pos):
    """Проверка клика по кнопкам меню паузы."""
    global paused
    if resume_button.collidepoint(pos):
        paused = False
    elif settings_button.collidepoint(pos):
        open_settings()  # Открытие меню настроек
    elif quit_button.collidepoint(pos):
        pygame.quit()
        sys.exit()

def draw_pause_button():
    """Отрисовка кнопки паузы с улучшенным дизайном."""
    global pause_button_hovered
    
    # Проверка, наведена ли мышь на кнопку паузы
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pause_button.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, PAUSE_BUTTON_HOVER_COLOR, pause_button)
        pause_button_hovered = True
    else:
        pygame.draw.rect(screen, PAUSE_BUTTON_COLOR, pause_button)
        pause_button_hovered = False
    
    # Текст на кнопке
    draw_text("Pause", font, WHITE, pause_button.centerx - 35, pause_button.centery - 10)

def main():
    global background_x, player_x, babirussa_x, player_frame, babirussa_frame, player_state, player_y
    global last_babirussa_change_time, paused

    running = True
    jump_velocity = 0
    gravity = 0.5
    is_jumping = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if paused:
                    check_pause_menu_click(event.pos)
                elif pause_button.collidepoint(event.pos):
                    paused = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Нажатие P для паузы
                    paused = not paused

        if paused:
            # Отображаем меню паузы
            draw_pause_menu()
            pygame.display.flip()
            continue  # Пропускаем остальную логику игры

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping:  # Прыжок
            is_jumping = True
            jump_velocity = -10
            player_state = "jump"
        elif keys[pygame.K_LCTRL] and not is_jumping:  # Пригнуться
            player_state = "crouch"
        elif not is_jumping:
            player_state = "run"

        # Движение игрока
        if is_jumping:
            player_y += jump_velocity
            jump_velocity += gravity
            if player_y >= 400:  # Назад на землю
                player_y = 400
                is_jumping = False

        # Движение фона
        background_x -= BACKGROUND_SPEED
        if background_x <= -WIDTH:
            background_x = 0

        # Движение бабируссы (синхронизировано с игроком)
        babirussa_x = player_x - WIDTH // 4  # Бабирусса на 1/4 экрана позади игрока

        # Таймер для смены анимации бабируссы
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - last_babirussa_change_time > babirussa_animation_time:
            last_babirussa_change_time = current_time
            babirussa_frame = 1 if babirussa_frame == 0 else 0  # Медленно переключаем кадры

        # Анимация игрока
        if player_state == "run":
            player_frame = (player_frame + 1) % len(player_run_images)
            player_image = player_run_images[player_frame]
        elif player_state == "jump":
            player_image = player_jump_image
        elif player_state == "crouch":
            player_image = player_crouch_image

        # Анимация бабируссы
        babirussa_image = babirussa_run_images[babirussa_frame]

        # Отрисовка фона
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + WIDTH, 0))

        # Отрисовка персонажей
        screen.blit(player_image, (player_x, player_y))
        screen.blit(babirussa_image, (babirussa_x, babirussa_y))

        # Отображение кнопки паузы
        draw_pause_button()

        # Счётчик времени
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        draw_text(f"Time: {elapsed_time} s", font, BLACK, 10, 10)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
