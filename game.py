import pygame
import os
import sys
import random
import json
from settings import open_settings
from music_manager import music_manager
import game_over

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

# Загрузка монеты, бустера и джетпака
coin_image = pygame.image.load(os.path.join(items_path, "bitcoin.png"))
coin_image = pygame.transform.scale(coin_image, (40, 40))

boost_image = pygame.image.load(os.path.join(items_path, "boost.png"))
boost_image = pygame.transform.scale(boost_image, (50, 50))

# Загрузка джетпака для игрового поля (большой размер)
jetpack_image = pygame.image.load(os.path.join(items_path, "jet.png"))
jetpack_image = pygame.transform.scale(jetpack_image, (150, 150))  # Увеличили в 3 раза

# Загрузка джетпака для иконки таймера (средний размер)
jetpack_icon = pygame.image.load(os.path.join(items_path, "jet.png"))
jetpack_icon = pygame.transform.scale(jetpack_icon, (50, 50))  # Увеличили иконку для таймера

# Загрузка голубца
adrian_image = pygame.image.load(os.path.join(items_path, "adrian.png"))
adrian_image = pygame.transform.scale(adrian_image, (60, 60))  # Увеличили размер голубца

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
player_speed = 0  # Новая переменная для скорости игрока

# Джетпак
jetpack_active = False
jetpack_start_time = 0
jetpack_duration = 0
last_jetpack_spawn = 0
jetpack_spawn_cooldown = 120000  # 2 minutes in milliseconds
jetpack = None
jetpack_spawned = False
BOOST_Y_LEVEL = 310  # Уровень головы персонажа

# Голубцы
MAX_ADRIANS = 8  # Больше чем монет
adrians = []
last_adrian_spawn = 0
min_adrian_spawn_interval = 1000  # Чаще чем монеты
adrian_speed = 5
ADRIAN_Y_LEVELS = [100, 150, 200]  # Только в небе

# Бустер
boost_active = False
boost_multiplier = 1.0
boost_start_time = 0
boost_duration = 0
last_boost_spawn = 0
boost_spawn_cooldown = 120000  # 2 minutes in milliseconds
boost = None
boost_spawned = False
forced_boost_spawn = False
BOOST_Y_LEVEL = 310  # Уровень головы персонажа

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

def draw_boost_timer():
    """Отображение таймера бустера и джетпака."""
    if boost_active:
        remaining_time = int((boost_duration - (pygame.time.get_ticks() - boost_start_time)) / 1000)
        if remaining_time > 0:
            screen.blit(boost_image, (20, 20))
            draw_text(f"{remaining_time}s", font, BLACK, 100, 40)
    
    if jetpack_active:
        remaining_time = int((jetpack_duration - (pygame.time.get_ticks() - jetpack_start_time)) / 1000)
        if remaining_time > 0:
            screen.blit(jetpack_icon, (20, 70))  # Используем маленькую иконку для таймера
            draw_text(f"{remaining_time}s", font, BLACK, 100, 90)

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
    for adrian in adrians:
        screen.blit(adrian_image, (adrian['x'], adrian['y']))
    if boost:
        screen.blit(boost_image, (boost['x'], boost['y']))
    if jetpack:
        screen.blit(jetpack_image, (jetpack['x'], jetpack['y']))

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

def check_adrian_collision(x, y, adrian_x, adrian_y):
    """Проверка столкновения с голубцом"""
    player_rect = pygame.Rect(x, y, PLAYER_NORMAL_WIDTH, PLAYER_NORMAL_HEIGHT if not is_crouching else PLAYER_CROUCH_HEIGHT)
    adrian_rect = pygame.Rect(adrian_x, adrian_y, 60, 60)
    return player_rect.colliderect(adrian_rect)

def check_boost_collision(x, y, boost_x, boost_y):
    """Проверка столкновения с бустером"""
    player_rect = pygame.Rect(x, y, PLAYER_NORMAL_WIDTH, PLAYER_NORMAL_HEIGHT if not is_crouching else PLAYER_CROUCH_HEIGHT)
    boost_rect = pygame.Rect(boost_x, boost_y, 50, 50)  # Увеличенный размер бустера
    return player_rect.colliderect(boost_rect)

def check_jetpack_collision(x, y, jetpack_x, jetpack_y):
    """Проверка столкновения с джетпаком"""
    player_rect = pygame.Rect(x, y, PLAYER_NORMAL_WIDTH, PLAYER_NORMAL_HEIGHT if not is_crouching else PLAYER_CROUCH_HEIGHT)
    jetpack_rect = pygame.Rect(jetpack_x, jetpack_y, 150, 150)
    return player_rect.colliderect(jetpack_rect)

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
    """Спавн монет или голубцов в зависимости от активности джетпака"""
    global last_coin_spawn, coins, adrians
    
    if elapsed_time < 11:  # Начинаем спавнить после 11 секунд
        return
        
    if current_time - last_coin_spawn < min_coin_spawn_interval:
        return
        
    if jetpack_active:  # Если активен джетпак, спавним голубцы
        if len(adrians) >= 3:  # Уменьшили максимальное количество голубцов
            return
            
        # Спавним 1-2 голубца за раз
        num_adrians = random.randint(1, 2)
        
        # Спавним только в верхней части экрана (от 50 до HEIGHT//2)
        adrian_y = random.randint(50, HEIGHT//2 - 50)
        
        for i in range(num_adrians):
            adrians.append({
                'x': WIDTH + (i * 120),  # Увеличили расстояние между голубцами
                'y': adrian_y,
                'speed': coin_speed * 0.8
            })
    else:  # Если джетпак не активен, спавним обычные монеты
        if len(coins) >= MAX_COINS:
            return
            
        num_coins = random.randint(1, 4)
        coin_y = random.choice(COIN_Y_LEVELS)
        
        for i in range(num_coins):
            coins.append({
                'x': WIDTH + (i * 60),
                'y': coin_y,
                'speed': coin_speed
            })
    
    last_coin_spawn = current_time + 500

def spawn_adrians(current_time, elapsed_time):
    """Спавн голубцов"""
    global last_adrian_spawn
    
    if not jetpack_active:  # Спавним только при активном джетпаке
        return
        
    if current_time - last_adrian_spawn < min_adrian_spawn_interval:
        return
        
    if len(adrians) >= MAX_ADRIANS:
        return
        
    # Определяем количество голубцов для спавна (2-6)
    num_adrians = random.randint(2, 6)
    
    # Определяем уровень появления голубцов (только в небе)
    adrian_y = random.choice(ADRIAN_Y_LEVELS)
    
    for i in range(num_adrians):
        adrians.append({
            'x': WIDTH + (i * 40),
            'y': adrian_y,
            'speed': adrian_speed
        })
    
    last_adrian_spawn = current_time

def spawn_boost(current_time, elapsed_time):
    """Спавн бустера"""
    global boost, last_boost_spawn, boost_spawned, forced_boost_spawn
    
    if elapsed_time < 60:  # Не спавним раньше 1 минуты
        return
        
    if elapsed_time > 120:  # Не спавним после 2 минут
        return
        
    if boost or boost_active:  # Если бустер уже есть или активен
        return
        
    if not boost_spawned and random.random() < 0.01:  # 1% шанс спавна каждый тик в промежутке 1-2 минуты
        boost = {
            'x': WIDTH,
            'y': BOOST_Y_LEVEL,  # Всегда на уровне головы
            'speed': 5
        }
        boost_spawned = True
        last_boost_spawn = current_time

def spawn_jetpack(current_time, elapsed_time):
    """Спавн джетпака"""
    global jetpack, last_jetpack_spawn, jetpack_spawned
    
    if elapsed_time < 60:  # Не спавним раньше 1 минуты
        return
        
    if elapsed_time > 120:  # Не спавним после 2 минут
        return
        
    if jetpack or jetpack_active:  # Если джетпак уже есть или активен
        return
        
    if not jetpack_spawned and random.random() < 0.01:  # 1% шанс спавна каждый тик в промежутке 1-2 минуты
        jetpack = {
            'x': WIDTH,
            'y': BOOST_Y_LEVEL,  # Используем ту же высоту, что и у бустера
            'speed': 5
        }
        jetpack_spawned = True
        last_jetpack_spawn = current_time

def force_spawn_boost():
    """Принудительный спавн бустера"""
    global boost, boost_spawned
    
    if not boost and not boost_active:  # Только если нет активного бустера
        boost = {
            'x': WIDTH,
            'y': BOOST_Y_LEVEL,  # Всегда на уровне головы
            'speed': 5
        }
        boost_spawned = True

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
    """Обновление позиций монет и голубцов"""
    global coins, adrians
    
    # Обновляем позиции монет
    if not jetpack_active:
        coins = [coin for coin in coins if coin['x'] >= 0]
        for coin in coins:
            coin['x'] -= coin['speed']
    else:
        coins = []  # Очищаем монеты при активном джетпаке
        
    # Обновляем позиции голубцов
    adrians = [adrian for adrian in adrians if adrian['x'] >= 0]
    for adrian in adrians:
        adrian['x'] -= adrian['speed']

def update_boost():
    """Обновление позиции бустера"""
    global boost, boost_active, boost_multiplier, boost_start_time, boost_duration, player_speed
    
    if boost:
        boost['x'] -= boost['speed']
        if boost['x'] < 0:
            boost = None
            
    # Проверка окончания действия бустера
    if boost_active and pygame.time.get_ticks() - boost_start_time > boost_duration:
        boost_active = False
        boost_multiplier = 1.0
        player_speed = 0  # Сброс скорости игрока

def update_jetpack():
    """Обновление позиции джетпака"""
    global jetpack, jetpack_active, jetpack_start_time, jetpack_duration
    
    if jetpack:
        jetpack['x'] -= jetpack['speed']
        if jetpack['x'] < 0:
            jetpack = None
            
    # Проверка окончания действия джетпака
    if jetpack_active and pygame.time.get_ticks() - jetpack_start_time > jetpack_duration:
        jetpack_active = False

def init_game():
    """Инициализация игры"""
    global running, player_x, player_y, score, collected_coins, start_time, current_map, background_image
    
    # Инициализация переменных
    running = True
    player_x = WIDTH // 4
    player_y = HEIGHT // 2
    score = 0
    collected_coins = 0
    start_time = pygame.time.get_ticks()
    
    # Загрузка настроек карты и соответствующего фона
    try:
        with open("temp_game_settings.json", "r") as f:
            settings = json.load(f)
            current_map = settings.get("map", "highway")
            
            # Загружаем соответствующий фон
            if current_map == "forest":
                background_path = os.path.join("assets", "bg_game", "forest.jpg")
            else:  # highway
                background_path = os.path.join("assets", "bg_game", "Bg_1.jpg")
                
            background_image = pygame.image.load(background_path)
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            
    except Exception as e:
        print(f"Error loading map settings or background: {e}")
        current_map = "highway"
        # Загружаем фон по умолчанию
        background_path = os.path.join("assets", "bg_game", "Bg_1.jpg")
        background_image = pygame.image.load(background_path)
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    
    # Запуск музыки
    try:
        music_manager.stop_music()
        music_manager.play_menu_music()
    except Exception as e:
        print(f"Error playing music: {e}")

def main():
    music_manager.stop_music()  # Останавливаем музыку меню
    global background_x, paused, score, last_score_update, player_frame, player_state
    global babirussa_frame, babirussa_x, is_jumping, jump_velocity, player_y
    global babirussa_y, babirussa_jump_velocity, babirussa_is_jumping
    global player_x, on_platform, pause_start_time, total_pause_time
    global is_crouching, stones, last_stone_spawn, mosquitos, last_mosquito_spawn
    global coins, last_coin_spawn, boost, boost_active, boost_multiplier
    global boost_start_time, boost_duration, player_speed, jetpack, jetpack_active
    global jetpack_start_time, jetpack_duration, adrians
    collected_coins = 0
    collected_adrians = 0

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
                    if event.key == pygame.K_SPACE:
                        if jetpack_active:
                            jump_velocity = -8
                        elif not is_jumping or on_platform:
                            is_jumping = True
                            on_platform = False
                            jump_velocity = -12
                    if event.key == pygame.K_LCTRL and not is_jumping:
                        player_state = "crouch"
                        is_crouching = True
                        player_image = player_crouch_image
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Чит-код для тестирования джетпака
                        print("Кнопка + нажата")
                        if not jetpack and not jetpack_active:
                            print("Создаем джетпак")
                            jetpack = {
                                'x': WIDTH,
                                'y': BOOST_Y_LEVEL,  # Используем ту же высоту, что и у бустера
                                'speed': 5
                            }
                            jetpack_spawned = True
                            print(f"Джетпак создан: {jetpack}")
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

        # Спавн и обновление препятствий и предметов
        spawn_stones(current_time, elapsed_time)
        spawn_mosquitos(current_time, elapsed_time)
        spawn_coins(current_time, elapsed_time)
        spawn_boost(current_time, elapsed_time)
        spawn_jetpack(current_time, elapsed_time)
        spawn_adrians(current_time, elapsed_time)
        update_stones()
        update_mosquitos()
        update_coins()
        update_boost()
        update_jetpack()

        # Проверка столкновения с монетами/голубцами
        for coin in coins[:]:
            if check_coin_collision(player_x, player_y, coin['x'], coin['y']):
                coins.remove(coin)
                score += 500
                collected_coins += 1
                
        for adrian in adrians[:]:
            if check_adrian_collision(player_x, player_y, adrian['x'], adrian['y']):
                adrians.remove(adrian)
                score += 100  # Уменьшили количество очков за голубцы до 100
                collected_coins += 1  # По-прежнему считаем в общем количестве монет

        # Проверка столкновения с бустером
        if boost and check_boost_collision(player_x, player_y, boost['x'], boost['y']):
            boost_active = True
            boost_multiplier = random.uniform(1.0, 1.05)  # Уменьшили до 1.0-1.05
            boost_duration = random.randint(8000, 20000)  # 8-20 секунд
            boost_start_time = pygame.time.get_ticks()
            player_speed = 0.5  # Уменьшили с 1 до 0.5
            boost = None

        # Управление прыжком и падением игрока
        if is_jumping or not on_platform:
            new_player_y = player_y + jump_velocity
            
            # Ограничение по верхней границе экрана
            if new_player_y < 0:
                new_player_y = 0
                jump_velocity = 0
            
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

        # Обновление позиции игрока при активном бустере
        if boost_active:
            new_player_x = player_x + player_speed
            # Проверка правой границы экрана
            if new_player_x < WIDTH - PLAYER_NORMAL_WIDTH:
                player_x = new_player_x

        # Check if player hits stone while running
        for stone in stones:
            if check_collision(player_x, player_y, stone['x'], stone['y'], stone['size']):
                if not is_jumping and not on_platform:
                    player_x -= stone['speed']  # Отталкивание без учета бустера

        # Check if player hits mosquito
        for mosquito in mosquitos:
            if check_mosquito_collision(player_x, player_y, mosquito['x'], mosquito['y']):
                if not is_crouching:  # Только если игрок не пригнулся
                    player_x -= mosquito['speed']  # Отталкивание без учета бустера

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
            result = game_over.show_game_over_screen(score, elapsed_time, collected_coins)
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

        # Проверка столкновения с джетпаком
        if jetpack and check_jetpack_collision(player_x, player_y, jetpack['x'], jetpack['y']):
            jetpack_active = True
            jetpack_duration = 10000  # 10 секунд действия джетпака
            jetpack_start_time = pygame.time.get_ticks()
            jetpack = None

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
        draw_boost_timer()

        # Кнопка паузы
        draw_pause_button()

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    init_game()
    main()