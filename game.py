import pygame
import os
import sys
from settings import open_settings

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
PAUSE_MENU_BG = (0, 0, 0, 128)  # Semi-transparent black
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Пути к изображениям
player_path = "./assets/animations/player"
babirussa_path = "./assets/animations/babirussa"
background_path = "./assets/bg_game"
blocks_path = "./assets/blocks"

# Загрузка фона
background_image = pygame.image.load(os.path.join(background_path, "Bg_1.jpg"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Загрузка анимаций игрока
player_run_images = [
    pygame.image.load(os.path.join(player_path, f"Run_{i}.png")) for i in range(1, 3)
]
player_jump_image = pygame.image.load(os.path.join(player_path, "Jump_player.png"))
player_crouch_image = pygame.image.load(os.path.join(player_path, "Crouch_player.png"))

# Масштабирование изображений игрока
PLAYER_NORMAL_WIDTH = 100
PLAYER_NORMAL_HEIGHT = 100
PLAYER_CROUCH_WIDTH = 120  # Wider when crouching
PLAYER_CROUCH_HEIGHT = 70  # Lower when crouching

player_run_images = [pygame.transform.scale(img, (PLAYER_NORMAL_WIDTH, PLAYER_NORMAL_HEIGHT)) for img in player_run_images]
player_jump_image = pygame.transform.scale(player_jump_image, (PLAYER_NORMAL_WIDTH, PLAYER_NORMAL_HEIGHT))
player_crouch_image = pygame.transform.scale(player_crouch_image, (PLAYER_CROUCH_WIDTH, PLAYER_CROUCH_HEIGHT))

# Загрузка анимаций бабируссы
babirussa_run_images = [
    pygame.image.load(os.path.join(babirussa_path, f"run_{i}.png")) for i in range(1, 3)
]
babirussa_run_images = [pygame.transform.scale(img, (150, 100)) for img in babirussa_run_images]

# Загрузка блока
stone_image = pygame.image.load(os.path.join(blocks_path, "stone.png"))
stone_image = pygame.transform.scale(stone_image, (100, 100))  # Changed to square 100x100

# Переменные для игры
background_x = 0
score = 0
level = 0
start_time = pygame.time.get_ticks()
last_score_update = pygame.time.get_ticks()
pause_start_time = 0
total_pause_time = 0

# Переменные для паузы
paused = False

# Игрок
player_x, player_y = 300, 400  # Moved more to the left
player_frame = 0
player_state = "run"
jump_velocity = 0
gravity = 0.8
is_jumping = False
on_platform = False
is_crouching = False  # New variable for crouch state

# Бабирусса
babirussa_x, babirussa_y = 0, 400  # Changed to spawn at far left
babirussa_frame = 0
babirussa_jump_velocity = 0
babirussa_is_jumping = False

# Блоки
stone_x = WIDTH  # Start from right edge
stone_y = 400  # Adjusted to ground level
stone_spawned = False
stone_speed = 5

# Шрифты
font = pygame.font.Font(None, 40)

# Кнопки паузы
pause_button = pygame.Rect(WIDTH - 100, 20, 80, 40)

# Кнопки меню паузы
resume_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 50)
settings_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50)
menu_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
exit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 125, 200, 50)

def draw_text(text, font, color, x, y):
    """Отображение текста на экране."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def draw_pause_button():
    """Отрисовка кнопки паузы."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    color = PAUSE_BUTTON_HOVER_COLOR if pause_button.collidepoint(mouse_x, mouse_y) else PAUSE_BUTTON_COLOR
    pygame.draw.rect(screen, color, pause_button)
    draw_text("Pause", font, WHITE, pause_button.centerx, pause_button.centery)

def draw_pause_menu():
    """Отрисовка меню паузы."""
    # Полупрозрачный фон
    s = pygame.Surface((WIDTH, HEIGHT))
    s.fill((0, 0, 0))
    s.set_alpha(128)
    screen.blit(s, (0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Resume button
    color = BUTTON_HOVER_COLOR if resume_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(screen, color, resume_button)
    draw_text("Resume", font, WHITE, resume_button.centerx, resume_button.centery)
    
    # Settings button
    color = BUTTON_HOVER_COLOR if settings_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(screen, color, settings_button)
    draw_text("Settings", font, WHITE, settings_button.centerx, settings_button.centery)
    
    # Menu button
    color = BUTTON_HOVER_COLOR if menu_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(screen, color, menu_button)
    draw_text("Back to Menu", font, WHITE, menu_button.centerx, menu_button.centery)
    
    # Exit button
    color = BUTTON_HOVER_COLOR if exit_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(screen, color, exit_button)
    draw_text("Exit Game", font, WHITE, exit_button.centerx, exit_button.centery)

def handle_pause_menu_click(pos):
    """Обработка кликов в меню паузы."""
    global paused
    x, y = pos
    
    if resume_button.collidepoint(x, y):
        paused = False
    elif settings_button.collidepoint(x, y):
        open_settings()
    elif menu_button.collidepoint(x, y):
        try:
            import menu
            menu.main()
        except ImportError:
            print("Menu module not found")
    elif exit_button.collidepoint(x, y):
        pygame.quit()
        sys.exit()

def draw_blocks():
    """Отрисовка блоков."""
    if stone_spawned:
        screen.blit(stone_image, (stone_x, stone_y))

def check_collision(x, y, block_x, block_y):
    """Проверка столкновения с блоком"""
    player_rect = pygame.Rect(x, y, 100, 100)
    block_rect = pygame.Rect(block_x, block_y, 100, 100)
    return player_rect.colliderect(block_rect)

def check_platform_collision(x, y, block_x, block_y):
    """Проверка приземления на платформу"""
    player_feet = pygame.Rect(x + 25, y + 90, 50, 10)  # Узкая область под ногами игрока
    platform_top = pygame.Rect(block_x, block_y, 100, 10)  # Верхняя часть блока
    return player_feet.colliderect(platform_top)

def main():
    global background_x, paused, score, last_score_update, player_frame, player_state
    global babirussa_frame, babirussa_x, is_jumping, jump_velocity, player_y
    global babirussa_y, babirussa_jump_velocity, babirussa_is_jumping
    global stone_x, stone_spawned, player_x, on_platform, pause_start_time, total_pause_time
    global is_crouching

    # Initialize images before the game loop
    player_image = player_run_images[0]
    babirussa_image = babirussa_run_images[0]

    running = True
    animation_timer = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if pause_button.collidepoint(event.pos):
                        if not paused:
                            pause_start_time = pygame.time.get_ticks()
                        paused = not paused
                    elif paused:
                        handle_pause_menu_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not paused:
                        pause_start_time = pygame.time.get_ticks()
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_SPACE and (not is_jumping or on_platform):
                        is_jumping = True
                        on_platform = False
                        jump_velocity = -12
                    if event.key == pygame.K_LCTRL and not is_jumping:
                        player_state = "crouch"
                        is_crouching = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL and is_crouching:
                    player_state = "run"
                    is_crouching = False

        if paused:
            draw_pause_menu()
            pygame.display.flip()
            continue

        if pause_start_time > 0:
            total_pause_time += pygame.time.get_ticks() - pause_start_time
            pause_start_time = 0

        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time - total_pause_time) // 1000

        # Spawn stone after 10 seconds
        if elapsed_time >= 10 and not stone_spawned:
            stone_spawned = True
            stone_x = WIDTH

        # Move stone if spawned
        if stone_spawned:
            stone_x -= stone_speed
            if stone_x + 100 < 0:  # When stone is completely off screen
                stone_spawned = False

        # Управление прыжком и падением игрока
        if is_jumping or not on_platform:
            new_player_y = player_y + jump_velocity
            
            # Проверка приземления на платформу
            if stone_spawned and check_platform_collision(player_x, new_player_y, stone_x, stone_y):
                player_y = stone_y - (PLAYER_CROUCH_HEIGHT if is_crouching else PLAYER_NORMAL_HEIGHT)
                is_jumping = False
                on_platform = True
                jump_velocity = 0
            else:
                player_y = new_player_y
                jump_velocity += gravity
                
                # Проверка приземления на землю
                ground_level = 400 + (PLAYER_NORMAL_HEIGHT - (PLAYER_CROUCH_HEIGHT if is_crouching else PLAYER_NORMAL_HEIGHT))
                if player_y >= ground_level:
                    player_y = ground_level
                    is_jumping = False
                    on_platform = False
                    jump_velocity = 0

        # Если игрок на платформе
        if on_platform:
            # Проверяем, все еще ли игрок над платформой
            if not (stone_x <= player_x + 100 and player_x <= stone_x + 100):
                on_platform = False
                is_jumping = True
                jump_velocity = 0

        # Check if player hits stone while running
        if check_collision(player_x, player_y, stone_x, stone_y):
            if not is_jumping and not on_platform:
                player_x -= stone_speed  # Push player with stone

        # Автоматический прыжок бабируссы
        if not babirussa_is_jumping and stone_x - babirussa_x < 200:
            babirussa_is_jumping = True
            babirussa_jump_velocity = -12

        if babirussa_is_jumping:
            babirussa_y += babirussa_jump_velocity
            babirussa_jump_velocity += gravity
            if babirussa_y >= 400:
                babirussa_y = 400
                babirussa_is_jumping = False

        # Движение фона
        background_x -= 5
        if background_x <= -WIDTH:
            background_x = 0

        # Обновление очков
        if current_time - last_score_update >= 1000:
            score += 10
            last_score_update = current_time

        # Slower animations
        animation_timer += 1
        if animation_timer >= 15:  # Increased delay between frames
            # Анимация игрока
            if player_state == "run" and not is_jumping:
                player_frame = (player_frame + 1) % len(player_run_images)
                player_image = player_run_images[player_frame]
            elif player_state == "crouch":
                player_image = player_crouch_image
            else:
                player_image = player_jump_image

            # Анимация бабируссы
            babirussa_frame = (babirussa_frame + 1) % len(babirussa_run_images)
            babirussa_image = babirussa_run_images[babirussa_frame]
            
            animation_timer = 0

        # Отрисовка
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + WIDTH, 0))

        # Отображение блока
        draw_blocks()

        # Отображение игрока и бабируссы
        screen.blit(babirussa_image, (babirussa_x, babirussa_y))
        screen.blit(player_image, (player_x, player_y))

        # HUD
        draw_text(f"Time: {elapsed_time}s", font, BLACK, WIDTH // 2 - 150, 20)
        draw_text(f"Score: {score}", font, BLACK, WIDTH // 2, 20)

        # Кнопка паузы
        draw_pause_button()

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
