import pygame
import os
import json
from music_manager import music_manager

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape from AB")

# Пути
image_folder = "assets/bg"
image_path = os.path.join(image_folder, "road.jpg")
background_image = pygame.image.load(image_path)
music_path = "assets/audio/tests.mp3"  # Тестовый файл музыки
settings_file = "settings.json"  # Файл с настройками
translations_file = "translations.json"  # Файл с переводами
records_file = "records.json"  # Файл с рекордами

# Загрузка переводов
with open(translations_file, "r", encoding="utf-8") as file:
    translations = json.load(file)

# Загрузка настроек
if os.path.exists(settings_file):
    with open(settings_file, "r", encoding="utf-8") as file:
        settings = json.load(file)
else:
    settings = {
        "language": "Русский",
        "sound": True
    }

# Загрузка рекордов
if os.path.exists(records_file):
    with open(records_file, "r", encoding="utf-8") as file:
        records = json.load(file)
else:
    records = []

# Переводы для записей
records_translations = {
    "Русский": {
        "title": "Рекорды",
        "back": "Назад",
        "name": "Имя",
        "score": "Счёт",
        "time": "Время",
        "coins": "Монеты",
        "confirm": "Очистить все рекорды?",
        "warning": "Это действие нельзя отменить!",
        "yes": "Да",
        "no": "Нет",
        "rank": "Место"
    },
    "English": {
        "title": "Records",
        "back": "Back",
        "name": "Name",
        "score": "Score",
        "time": "Time",
        "coins": "Coins",
        "confirm": "Clear all records?",
        "warning": "This action cannot be undone!",
        "yes": "Yes",
        "no": "No",
        "rank": "Rank"
    },
    "Français": {
        "title": "Records",
        "back": "Retour",
        "name": "Nom",
        "score": "Score",
        "time": "Temps",
        "coins": "Pièces",
        "confirm": "Effacer tous les records?",
        "warning": "Cette action ne peut pas être annulée!",
        "yes": "Oui",
        "no": "Non",
        "rank": "Rang"
    }
}

# Переводы для деталей записи
details_translations = {
    "Русский": {
        "name": "Имя",
        "map": "Карта",
        "score": "Счёт",
        "time": "Время",
        "coins": "Монеты",
        "back": "Назад"
    },
    "English": {
        "name": "Name",
        "map": "Map",
        "score": "Score",
        "time": "Time",
        "coins": "Coins",
        "back": "Back"
    },
    "Français": {
        "name": "Nom",
        "map": "Carte",
        "score": "Score",
        "time": "Temps",
        "coins": "Pièces",
        "back": "Retour"
    }
}

# Цвета
text_color = (0, 0, 0)  # Чёрный цвет текста
button_color = (100, 149, 237)  # Стильный синий цвет
button_hover_color = (65, 105, 225)  # Темно-синий при наведении
button_active_color = (25, 25, 112)  # Очень темно-синий при нажатии
button_border_color = (0, 0, 139)  # Темно-синий для обводки

# Шрифты
font = pygame.font.Font(None, 60)  # Основной шрифт
small_font = pygame.font.Font(None, 40)  # Шрифт для кнопок
font_medium = pygame.font.Font(None, 50)  # Шрифт для заголовков

# Функция для перевода текста
def get_translation(key):
    """Возвращает перевод для текущего языка или ключ, если перевода нет."""
    return translations.get(settings["language"], {}).get(key, key)

# Кнопки настроек (добавляем кнопку рекордов)
sound_button_rect = pygame.Rect(200, 150, 400, 60)
language_button_rect = pygame.Rect(200, 230, 400, 60)
records_button_rect = pygame.Rect(200, 310, 400, 60)  # Новая кнопка
back_button_rect = pygame.Rect(200, 500, 400, 60)

def show_record_details(record):
    """Показывает детали выбранного рекорда"""
    viewing_details = True
    
    # Загружаем изображение карты из сохраненного пути
    try:
        map_path = record.get("map_details", {}).get("path") or os.path.join(
            "assets", "bg_game",
            "forest.jpg" if record["map"] == "forest" else "Bg_1.jpg"
        )
        map_preview = pygame.image.load(map_path)
        map_preview = pygame.transform.scale(map_preview, (300, 200))
        
        # Получаем название карты
        map_name = record.get("map_details", {}).get("name") or (
            "Forest" if record["map"] == "forest" else "Highway"
        )
    except:
        # Fallback для старых записей
        map_path = os.path.join("assets", "bg_game", "Bg_1.jpg")
        map_preview = pygame.image.load(map_path)
        map_preview = pygame.transform.scale(map_preview, (300, 200))
        map_name = "Highway"

    # Используем переводы
    trans = records_translations[settings["language"]]
    
    # Кнопка возврата
    back_button = pygame.Rect(300, 500, 200, 40)

    while viewing_details:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return True

        screen.blit(background_image, (0, 0))
        
        # Отображение таблицы с деталями
        table_rect = pygame.Rect(150, 100, 500, 380)
        pygame.draw.rect(screen, button_color, table_rect, border_radius=15)
        pygame.draw.rect(screen, button_border_color, table_rect, 2, border_radius=15)
        
        # Заголовок
        title = font.render(trans["title"], True, text_color)
        title_rect = title.get_rect(center=(400, 130))
        screen.blit(title, title_rect)
        
        # Отображение превью карты
        preview_rect = map_preview.get_rect(center=(400, 250))
        screen.blit(map_preview, preview_rect)
        
        # Название карты под превью
        map_text = font_medium.render(map_name, True, text_color)
        map_rect = map_text.get_rect(center=(400, preview_rect.bottom + 20))
        screen.blit(map_text, map_rect)
        
        # Отображение деталей в виде таблицы
        details = [
            (trans["name"], record['name']),
            (trans["score"], str(record['score'])),
            (trans["time"], f"{record['time']} сек"),
            (trans["coins"], str(record['coins']))
        ]
        
        y = 380
        for label, value in details:
            text = font_medium.render(f"{label}: {value}", True, text_color)
            text_rect = text.get_rect(center=(400, y))
            screen.blit(text, text_rect)
            y += 30

        # Кнопка возврата
        mouse_pos = pygame.mouse.get_pos()
        back_color = button_hover_color if back_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, back_color, back_button, border_radius=10)
        pygame.draw.rect(screen, button_border_color, back_button, 2, border_radius=10)
        back_text = font_medium.render(trans["back"], True, text_color)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        pygame.display.flip()
    
    return True

def clear_records():
    """Очищает все рекорды"""
    # Очищаем records.json
    with open("records.json", "w", encoding="utf-8") as file:
        json.dump([], file)
    
    # Сбрасываем highscores.json
    with open("highscores.json", "w") as file:
        json.dump({"high_score": 0}, file)

def show_records():
    """Показывает список рекордов"""
    viewing_records = True
    scroll_offset = 0
    dragging_scrollbar = False
    scroll_speed = 0
    
    clock = pygame.time.Clock()
    
    # Кнопки
    back_button = pygame.Rect(300, 520, 200, 40)
    reset_button = pygame.Rect(650, 50, 40, 40)
    
    # Область рекордов и полоса прокрутки
    records_area = pygame.Rect(200, 150, 400, 350)
    scrollbar_bg = pygame.Rect(620, 150, 20, 350)  # Фон ползунка
    records_per_page = 5
    
    trans = records_translations[settings["language"]]
    highlighted_record = None

    while viewing_records:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if reset_button.collidepoint(mouse_pos):
                        if show_confirmation(trans):
                            clear_records()
                            records.clear()
                            return True
                    elif back_button.collidepoint(mouse_pos):
                        return True
                    elif scrollbar_bg.collidepoint(mouse_pos):
                        dragging_scrollbar = True
                        # Обновляем позицию прокрутки при клике на ползунок
                        scroll_ratio = (mouse_pos[1] - 150) / 350
                        scroll_offset = max(0, min(scroll_ratio * (len(records) - records_per_page),
                                                 len(records) - records_per_page))
                    else:
                        # Проверяем клик по записи
                        for i, record in enumerate(records[int(scroll_offset):int(scroll_offset) + records_per_page]):
                            record_rect = pygame.Rect(200, 200 + i * 70, 400, 60)
                            if record_rect.collidepoint(mouse_pos):
                                if not show_record_details(record):
                                    return False
                
                # Прокрутка колесиком
                elif event.button == 4:  # Вверх
                    scroll_speed = 20
                elif event.button == 5:  # Вниз
                    scroll_speed = -20
            
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_scrollbar = False
                
            elif event.type == pygame.MOUSEMOTION and dragging_scrollbar:
                # Обновляем позицию прокрутки при перетаскивании
                scroll_ratio = (mouse_pos[1] - 150) / 350
                scroll_offset = max(0, min(scroll_ratio * (len(records) - records_per_page),
                                         len(records) - records_per_page))

        # Обновление плавной прокрутки от колесика мыши
        if abs(scroll_speed) > 0.1:
            scroll_offset = max(0, min(scroll_offset - scroll_speed / 60,
                                     len(records) - records_per_page))
            scroll_speed *= 0.9
        else:
            scroll_speed = 0

        screen.blit(background_image, (0, 0))
        
        # Заголовок
        title = font.render(trans["title"], True, text_color)
        title_rect = title.get_rect(center=(400, 80))
        screen.blit(title, title_rect)

        # Область рекордов
        pygame.draw.rect(screen, button_color, records_area, border_radius=15)
        pygame.draw.rect(screen, button_border_color, records_area, 2, border_radius=15)
        
        # Отрисовка полосы прокрутки
        if len(records) > records_per_page:
            # Фон полосы прокрутки
            pygame.draw.rect(screen, (200, 200, 200), scrollbar_bg, border_radius=10)
            
            # Ползунок
            thumb_height = max(50, 350 * (records_per_page / len(records)))
            thumb_pos = 150 + (350 - thumb_height) * (scroll_offset / (len(records) - records_per_page))
            thumb_rect = pygame.Rect(620, thumb_pos, 20, thumb_height)
            
            # Отрисовка ползунка с подсветкой при перетаскивании
            thumb_color = button_hover_color if dragging_scrollbar else button_color
            pygame.draw.rect(screen, thumb_color, thumb_rect, border_radius=10)
            pygame.draw.rect(screen, button_border_color, thumb_rect, 2, border_radius=10)

        # Заголовки колонок
        headers = [(trans["rank"], 80), (trans["name"], 200), (trans["score"], 120)]
        x = 220
        for header, width in headers:
            text = small_font.render(header, True, text_color)
            screen.blit(text, (x, 160))
            x += width

        # Отображение записей
        visible_records = records[int(scroll_offset):int(scroll_offset) + records_per_page]
        for i, record in enumerate(visible_records):
            record_rect = pygame.Rect(200, 200 + i * 70, 400, 60)
            
            # Подсветка при наведении
            if highlighted_record == i:
                pygame.draw.rect(screen, button_hover_color, record_rect, border_radius=10)
            else:
                pygame.draw.rect(screen, button_color, record_rect, border_radius=10)
            
            pygame.draw.rect(screen, button_border_color, record_rect, 2, border_radius=10)
            
            # Данные записи
            rank_text = small_font.render(f"#{int(scroll_offset) + i + 1}", True, text_color)
            screen.blit(rank_text, (240, record_rect.centery - 10))
            
            name_text = small_font.render(record['name'], True, text_color)
            screen.blit(name_text, (320, record_rect.centery - 10))
            
            score_text = small_font.render(str(record['score']), True, text_color)
            screen.blit(score_text, (500, record_rect.centery - 10))

        # Кнопки
        # Кнопка сброса
        pygame.draw.rect(screen, button_color, reset_button, border_radius=10)
        pygame.draw.rect(screen, button_border_color, reset_button, 2, border_radius=10)
        reset_text = small_font.render("↺", True, text_color)
        reset_rect = reset_text.get_rect(center=reset_button.center)
        screen.blit(reset_text, reset_rect)

        # Кнопка возврата
        back_color = button_hover_color if back_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, back_color, back_button, border_radius=15)
        pygame.draw.rect(screen, button_border_color, back_button, 2, border_radius=15)
        back_text = small_font.render(trans["back"], True, text_color)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        pygame.display.flip()
        clock.tick(60)
    
    return True

def show_confirmation(trans):
    """Показывает окно подтверждения очистки рекордов"""
    confirmation = True
    yes_button = pygame.Rect(250, 350, 140, 40)
    no_button = pygame.Rect(410, 350, 140, 40)

    while confirmation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button.collidepoint(mouse_pos):
                    return True
                if no_button.collidepoint(mouse_pos):
                    return False

        screen.blit(background_image, (0, 0))
        
        # Текст подтверждения
        text = font.render(f"{trans['confirm']}", True, text_color)
        text_rect = text.get_rect(center=(400, 250))
        screen.blit(text, text_rect)
        
        # Подтекст предупреждения
        warning = small_font.render(f"{trans['warning']}", True, (255, 0, 0))
        warning_rect = warning.get_rect(center=(400, 300))
        screen.blit(warning, warning_rect)

        # Кнопки Да/Нет
        mouse_pos = pygame.mouse.get_pos()
        
        # Кнопка Да
        yes_color = button_hover_color if yes_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, yes_color, yes_button, border_radius=15)
        pygame.draw.rect(screen, button_border_color, yes_button, 2, border_radius=15)
        yes_text = small_font.render(f"{trans['yes']}", True, text_color)
        yes_text_rect = yes_text.get_rect(center=yes_button.center)
        screen.blit(yes_text, yes_text_rect)
        
        # Кнопка Нет
        no_color = button_hover_color if no_button.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, no_color, no_button, border_radius=15)
        pygame.draw.rect(screen, button_border_color, no_button, 2, border_radius=15)
        no_text = small_font.render(f"{trans['no']}", True, text_color)
        no_text_rect = no_text.get_rect(center=no_button.center)
        screen.blit(no_text, no_text_rect)

        pygame.display.flip()

    return False

def add_new_record(score, map_name, time_played, coins_collected, record_name=None):
    """Добавляет новый рекорд"""
    global records
    
    try:
        with open("records.json", "r", encoding="utf-8") as file:
            records = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []
    
    # Проверяем и нормализуем название карты
    if isinstance(map_name, str):
        map_id = map_name.lower()
    else:
        map_id = "highway"  # значение по умолчанию
    
    print(f"Adding record with map: {map_id}")  # Для отладки
    
    # Определяем детали карты
    map_details = {
        "highway": {
            "name": "Highway",
            "file": "Bg_1.jpg",
            "path": os.path.join("assets", "bg_game", "Bg_1.jpg")
        },
        "forest": {
            "name": "Forest",
            "file": "forest.jpg",
            "path": os.path.join("assets", "bg_game", "forest.jpg")
        }
    }
    
    # Получаем детали карты
    current_map = map_details.get(map_id, map_details["highway"])
    
    # Создаем новый рекорд
    new_record = {
        "name": record_name if record_name else f"Record #{len(records) + 1}",
        "score": score,
        "map": map_id,
        "map_details": current_map,
        "time": time_played,
        "coins": coins_collected
    }
    
    records.append(new_record)
    records.sort(key=lambda x: x["score"], reverse=True)
    records = records[:10]
    
    with open("records.json", "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

def open_settings():
    music_manager.play_menu_music()
    
    running = True
    language_options = list(translations.keys())  # Доступные языки

    # Флаги для отслеживания состояния кнопок
    sound_button_pressed = False
    language_button_pressed = False
    records_button_pressed = False
    back_button_pressed = False

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    if sound_button_rect.collidepoint(mouse_pos):
                        sound_button_pressed = True
                        settings["sound"] = not settings["sound"]
                        music_manager.toggle_music(settings["sound"])
                    elif language_button_rect.collidepoint(mouse_pos):
                        language_button_pressed = True
                        current_index = language_options.index(settings["language"])
                        settings["language"] = language_options[
                            (current_index + 1) % len(language_options)
                        ]
                    elif records_button_rect.collidepoint(mouse_pos):
                        if not show_records():
                            running = False
                    elif back_button_rect.collidepoint(mouse_pos):
                        back_button_pressed = True
                        with open(settings_file, "w", encoding="utf-8") as file:
                            json.dump(settings, file, ensure_ascii=False, indent=4)
                        running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    sound_button_pressed = False
                    language_button_pressed = False
                    back_button_pressed = False

        # Рисование фона
        screen.blit(background_image, (0, 0))

        # Заголовок "Настройки"
        title_text = font.render(get_translation("title"), True, text_color)
        title_rect = title_text.get_rect(center=(400, 100))
        screen.blit(title_text, title_rect)

        # Отображение настроек
        sound_text = f"{get_translation('sound')}: {'On' if settings['sound'] else 'Off'}"
        language_text = f"{get_translation('language')}: {settings['language']}"
        
        # Отрисовка кнопки звука
        if sound_button_pressed and sound_button_rect.collidepoint(mouse_pos):
            color = button_active_color
        elif sound_button_rect.collidepoint(mouse_pos):
            color = button_hover_color
        else:
            color = button_color
        pygame.draw.rect(screen, color, sound_button_rect, border_radius=15)
        pygame.draw.rect(screen, button_border_color, sound_button_rect, width=2, border_radius=15)
        sound_text_surface = small_font.render(sound_text, True, text_color)
        sound_text_rect = sound_text_surface.get_rect(center=sound_button_rect.center)
        screen.blit(sound_text_surface, sound_text_rect)

        # Отрисовка кнопки языка
        if language_button_pressed and language_button_rect.collidepoint(mouse_pos):
            color = button_active_color
        elif language_button_rect.collidepoint(mouse_pos):
            color = button_hover_color
        else:
            color = button_color
        pygame.draw.rect(screen, color, language_button_rect, border_radius=15)
        pygame.draw.rect(screen, button_border_color, language_button_rect, width=2, border_radius=15)
        language_text_surface = small_font.render(language_text, True, text_color)
        language_text_rect = language_text_surface.get_rect(center=language_button_rect.center)
        screen.blit(language_text_surface, language_text_rect)

        # Отрисовка кнопки рекордов
        if records_button_rect.collidepoint(mouse_pos):
            color = button_hover_color
        else:
            color = button_color
        pygame.draw.rect(screen, color, records_button_rect, border_radius=15)
        pygame.draw.rect(screen, button_border_color, records_button_rect, width=2, border_radius=15)
        records_text = small_font.render(get_translation("records"), True, text_color)
        records_text_rect = records_text.get_rect(center=records_button_rect.center)
        screen.blit(records_text, records_text_rect)

        # Кнопка "Назад"
        if back_button_pressed and back_button_rect.collidepoint(mouse_pos):
            color = button_active_color
        elif back_button_rect.collidepoint(mouse_pos):
            color = button_hover_color
        else:
            color = button_color
        pygame.draw.rect(screen, color, back_button_rect, border_radius=15)
        pygame.draw.rect(screen, button_border_color, back_button_rect, width=2, border_radius=15)
        back_text = small_font.render(get_translation("back"), True, text_color)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        # Обновление экрана
        pygame.display.flip()

# Тестирование вызова настроек
if __name__ == "__main__":
    open_settings()

    # Проверка сохранённых настроек
    print("Сохранённые настройки:", settings)
