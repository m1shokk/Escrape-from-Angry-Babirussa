import pygame
import os
import sys
import random
from settings import open_settings
from music_manager import music_manager
from game_over import game_over

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
items_path = "./assets/items"

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

# Загрузка блока и комара
stone_image = pygame.image.load(os.path.join(blocks_path, "stone.png"))
stone_image = pygame.transform.scale(stone_image, (100, 100))  # Changed to square 100x100

mosquito_image = pygame.image.load(os.path.join(blocks_path, "Mustico.png"))
mosquito_image = pygame.transform.scale(mosquito_image, (50, 50))  # Маленький размер для комара

# Загрузка монеты
coin_image = pygame.image.load(os.path.join(items_path, "bitcoin.png"))
coin_image = pygame.transform.scale(coin_image, (40, 40))

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
MAX_STONES = 3
stones = []  # Список для хранения камней [{x, y, speed, size}, ...]
last_stone_spawn = 0
min_spawn_interval = 8000  # Минимальный интервал между спавнами в миллисекундах
stone_speed = 5

# Комары
MAX_MOSQUITOS = 2
mosquitos = []  # Список для хранения комаров [{x, y, speed}, ...]
last_mosquito_spawn = 0
min_mosquito_spawn_interval = 6000  # Интервал между спавнами комаров
mosquito_speed = 8  # Комары быстрее камней
MOSQUITO_Y_HIGH = 310  # Уровень головы стоящего игрока
MOSQUITO_Y_LOW = 430  # Уровень ног игрока

# Монеты
MAX_COINS = 4
coins = []  # Список для хранения монет [{x, y, speed}, ...]
last_coin_spawn = 0
min_coin_spawn_interval = 2000  # Интервал между спавнами монет
coin_speed = 5
COIN_Y_LEVELS = [430, 310, 200]  # Уровни появления монет (земля, голова, выше головы)

# Размеры камней
STONE_SIZES = [(100, 100), (80, 80), (60, 60)]  # Разные размеры камней
stone_images = {
    size: pygame.transform.scale(stone_image, size) for size in STONE_SIZES
}

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
            pygame.quit()
            os.system('python menu.py')
            sys.exit()
        except Exception as e:
            print(f"Error launching menu: {e}")
    elif exit_button.collidepoint(x, y):
        pygame.quit()
        sys.exit()

def draw_blocks():
    """Отрисовка блоков."""
    for stone in stones:
        screen.blit(stone_images[stone['size']], (stone['x'], stone['y']))
    for mosquito in mosquitos:
        screen.blit(mosquito_image, (mosquito['x'], mosquito['y']))
    for coin in coins:
        screen.blit(coin_image, (coin['x'], coin['y']))

def check_collision(x, y, block_x, block_y, block_size):
    """Проверка столкновения с блоком"""
    player_rect = pygame.Rect(x, y, 100, 100)
    block_rect = pygame.Rect(block_x, block_y, block_size[0], block_size[1])
    return player_rect.colliderect(block_rect)

def check_mosquito_collision(x, y, mosquito_x, mosquito_y):
    """Проверка столкновения с комаром"""
    player_rect = pygame.Rect(x, y, PLAYER_NORMAL_WIDTH, PLAYER_NORMAL_HEIGHT if not is_crouching else PLAYER_CROUCH_HEIGHT)
    mosquito_rect = pygame.Rect(mosquito_x, mosquito_y, 50, 50)
    return player_rect.colliderect(mosquito_rect)

def check_coin_collision(x, y, coin_x, coin_y):
    """Проверка столкновения с монетой"""
    player_rect = pygame.Rect(x, y, PLAYER_NORMAL_WIDTH, PLAYER_NORMAL_HEIGHT if not is_crouching else PLAYER_CROUCH_HEIGHT)
    coin_rect = pygame.Rect(coin_x, coin_y, 40, 40)
    return player_rect.colliderect(coin_rect)

def check_platform_collision(x, y, block_x, block_y, block_size):
    """Проверка приземления на платформу"""
    player_feet = pygame.Rect(x + 25, y + 90, 50, 10)  # Узкая область под ногами игрока
    platform_top = pygame.Rect(block_x, block_y, block_size[0], 10)  # Верхняя часть блока
    return player_feet.colliderect(platform_top)

def spawn_stones(current_time, elapsed_time):
    """Спавн камней с учетом времени и интервалов"""
    global last_stone_spawn
    
    # Не спавним камни до 10 секунд игры
    if elapsed_time < 10:
        return
        
    # Проверяем интервал между спавнами
    if current_time - last_stone_spawn < min_spawn_interval:
        return
        
    # Проверяем количество камней на экране
    if len(stones) >= MAX_STONES:
        return
        
    # Рандомно определяем количество камней для спавна (1-3)
    num_stones = random.randint(1, min(3, MAX_STONES - len(stones)))
    
    # Выбираем случайный размер для группы камней
    stone_size = random.choice(STONE_SIZES)
    
    for _ in range(num_stones):
        stones.append({
            'x': WIDTH + (_ * 150),  # Располагаем камни с небольшим отступом друг от друга
            'y': 400 + (100 - stone_size[1]),  # Корректируем Y в зависимости от размера
            'speed': stone_speed,
            'size': stone_size
        })
    
    last_stone_spawn = current_time

def spawn_mosquitos(current_time, elapsed_time):
    """Спавн комаров"""
    global last_mosquito_spawn
    
    if elapsed_time < 15:  # Changed from 10 to 15 seconds
        return
        
    if current_time - last_mosquito_spawn < min_mosquito_spawn_interval:
        return
        
    if len(mosquitos) >= MAX_MOSQUITOS:
        return
        
    # Исправляем порядок аргументов: от меньшего к большему
    mosquito_y = random.randint(MOSQUITO_Y_HIGH, MOSQUITO_Y_LOW)  # HIGH теперь первый аргумент, т.к. он меньше
        
    mosquitos.append({
        'x': WIDTH,
        'y': mosquito_y,
        'speed': mosquito_speed
    })
    
    last_mosquito_spawn = current_time

def spawn_coins(current_time, elapsed_time):
    """Спавн монет"""
    global last_coin_spawn
    
    if elapsed_time < 11:  # Начинаем спавнить монеты после 11 секунд
        return
        
    if current_time - last_coin_spawn < min_coin_spawn_interval:
        return
        
    if len(coins) >= MAX_COINS:
        return
        
    # Определяем количество монет для спавна (1-4)
    num_coins = random.randint(1, 4)
    
    # Определяем уровень появления монет
    if stones and random.random() < 0.3:  # 30% шанс появления на камне
        stone = random.choice(stones)
        coin_y = stone['y'] - 50  # Размещаем монету над камнем
    else:
        coin_y = random.choice(COIN_Y_LEVELS)  # Случайный уровень
    
    for i in range(num_coins):
        coins.append({
            'x': WIDTH + (i * 60),  # Располагаем монеты с отступом
            'y': coin_y,
            'speed': coin_speed
        })
    
    last_coin_spawn = current_time

def update_stones():
    """Обновление позиций камней"""
    global stones
    stones = [stone for stone in stones if stone['x'] + stone['size'][0] >= 0]  # Удаляем камни, ушедшие за экран
    
    for stone in stones:
        stone['x'] -= stone['speed']

def update_mosquitos():
    """Обновление позиций комаров"""
    global mosquitos
    mosquitos = [mosquito for mosquito in mosquitos if mosquito['x'] >= 0]  # Удаляем комаров, ушедшие за экран
    
    for mosquito in mosquitos:
        mosquito['x'] -= mosquito['speed']

def update_coins():
    """Обновление позиций монет"""
    global coins
    coins = [coin for coin in coins if coin['x'] >= 0]  # Удаляем монеты, ушедшие за экран
    
    for coin in coins:
        coin['x'] -= coin['speed']

def main():
    music_manager.stop_music()  # Останавливаем музыку меню
    global background_x, paused, score, last_score_update, player_frame, player_state
    global babirussa_frame, babirussa_x, is_jumping, jump_velocity, player_y
    global babirussa_y, babirussa_jump_velocity, babirussa_is_jumping
    global player_x, on_platform, pause_start_time, total_pause_time
    global is_crouching, stones, last_stone_spawn, mosquitos, last_mosquito_spawn
    global coins, last_coin_spawn
    collected_coins = 0

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
                        player_image = player_crouch_image  # Мгновенное обновление спрайта
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL and is_crouching:
                    player_state = "run"
                    is_crouching = False
                    player_image = player_run_images[player_frame]  # Мгновенное обновление спрайта

        if paused:
            draw_pause_menu()
            pygame.display.flip()
            continue

        if pause_start_time > 0:
            total_pause_time += pygame.time.get_ticks() - pause_start_time
            pause_start_time = 0

        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time - total_pause_time) // 1000

        # Спавн и обновление препятствий и монет
        spawn_stones(current_time, elapsed_time)
        spawn_mosquitos(current_time, elapsed_time)
        spawn_coins(current_time, elapsed_time)
        update_stones()
        update_mosquitos()
        update_coins()

        # Проверка столкновения с монетами
        for coin in coins[:]:  # Используем копию списка для безопасного удаления
            if check_coin_collision(player_x, player_y, coin['x'], coin['y']):
                coins.remove(coin)
                score += 500
                collected_coins += 1

        # Управление прыжком и падением игрока
        if is_jumping or not on_platform:
            new_player_y = player_y + jump_velocity
            
            # Проверка приземления на платформу
            on_any_platform = False
            for stone in stones:
                if check_platform_collision(player_x, new_player_y, stone['x'], stone['y'], stone['size']):
                    player_y = stone['y'] - (PLAYER_CROUCH_HEIGHT if is_crouching else PLAYER_NORMAL_HEIGHT)
                    is_jumping = False
                    on_platform = True
                    jump_velocity = 0
                    on_any_platform = True
                    break
                    
            if not on_any_platform:
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
            # Проверяем, все еще ли игрок над какой-либо платформой
            still_on_platform = False
            for stone in stones:
                if stone['x'] <= player_x + 100 and player_x <= stone['x'] + stone['size'][0]:
                    still_on_platform = True
                    break
            if not still_on_platform:
                on_platform = False
                is_jumping = True
                jump_velocity = 0

        # Check if player hits stone while running
        for stone in stones:
            if check_collision(player_x, player_y, stone['x'], stone['y'], stone['size']):
                if not is_jumping and not on_platform:
                    player_x -= stone['speed']  # Push player with stone

        # Check if player hits mosquito
        for mosquito in mosquitos:
            if check_mosquito_collision(player_x, player_y, mosquito['x'], mosquito['y']):
                if not is_crouching:  # Только если игрок не пригнулся
                    player_x -= mosquito['speed']  # Push player with mosquito

        # Автоматический прыжок бабируссы
        if not babirussa_is_jumping and stones and stones[0]['x'] - babirussa_x < 200:
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

        # Анимация только для бега
        animation_timer += 1
        if animation_timer >= 15:  # Increased delay between frames
            # Анимация игрока только для бега
            if player_state == "run" and not is_jumping and not is_crouching:
                player_frame = (player_frame + 1) % len(player_run_images)
                player_image = player_run_images[player_frame]
            elif is_jumping:
                player_image = player_jump_image

            # Анимация бабируссы
            babirussa_frame = (babirussa_frame + 1) % len(babirussa_run_images)
            babirussa_image = babirussa_run_images[babirussa_frame]
            
            animation_timer = 0

        # Проверка столкновения с бабируссой
        player_rect = pygame.Rect(player_x, player_y, 
                                PLAYER_NORMAL_WIDTH, 
                                PLAYER_NORMAL_HEIGHT if not is_crouching else PLAYER_CROUCH_HEIGHT)
        babirussa_rect = pygame.Rect(babirussa_x, babirussa_y, 150, 100)
        
        if player_rect.colliderect(babirussa_rect):
            # Остановка игры и показ экрана окончания
            result = game_over.show_game_over(score, collected_coins, elapsed_time)
            if result == "menu":
                try:
                    pygame.quit()
                    os.system('python menu.py')
                    sys.exit()
                except Exception as e:
                    print(f"Error launching menu: {e}")
            elif result == "quit":
                pygame.quit()
                sys.exit()

        # Отрисовка
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + WIDTH, 0))

        # Отображение блока
        draw_blocks()

        # Отображение игрока и бабируссы
        screen.blit(babirussa_image, (babirussa_x, babirussa_y))
        screen.blit(player_image, (player_x, player_y))

        # HUD
        draw_text(f"Score: {score}", font, BLACK, WIDTH // 2, 20)

        # Кнопка паузы
        draw_pause_button()

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
