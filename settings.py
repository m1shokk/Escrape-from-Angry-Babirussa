import pygame
import os
import json

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape from AB")

# Пути
image_folder = "images/bg"
image_path = os.path.join(image_folder, "road.jpg")
background_image = pygame.image.load(image_path)
music_path = "audio/test_music.mp3"  # Тестовый файл музыки
settings_file = "settings.json"  # Файл с настройками
translations_file = "translations.json"  # Файл с переводами

# Загрузка настроек
if os.path.exists(settings_file):
    with open(settings_file, "r", encoding="utf-8") as file:
        settings = json.load(file)
else:
    settings = {"sound": True, "language": "English"}

# Загрузка переводов
if os.path.exists(translations_file):
    with open(translations_file, "r", encoding="utf-8") as file:
        translations = json.load(file)
else:
    print(f"Файл переводов {translations_file} не найден.")
    translations = {}

# Цвета
text_color = (0, 0, 0)  # Чёрный цвет текста
button_color = (200, 200, 200)
button_hover_color = (170, 170, 170)
button_border_color = (50, 50, 50)

# Шрифты
font = pygame.font.Font(None, 60)  # Основной шрифт
small_font = pygame.font.Font(None, 40)  # Шрифт для кнопок

# Функция для перевода текста
def get_translation(key):
    """Возвращает перевод для текущего языка или ключ, если перевода нет."""
    return translations.get(settings["language"], {}).get(key, key)

# Функция настроек
def open_settings():
    # Включение музыки
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # Бесконечный повтор
    else:
        print("Музыка не найдена:", music_path)

    running = True
    selected_option = 0  # Индекс текущей настройки
    language_options = list(translations.keys())  # Доступные языки

    # Добавляем кнопку "Назад"
    back_button_rect = pygame.Rect(300, 500, 200, 60)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button_rect.collidepoint(mouse_pos):
                        # Сохранение настроек перед выходом
                        with open(settings_file, "w", encoding="utf-8") as file:
                            json.dump(settings, file, ensure_ascii=False, indent=4)
                        running = False  # Выход из настроек
                elif selected_option == 0:  # Переключение звука
                    settings["sound"] = not settings["sound"]
                    pygame.mixer.music.set_volume(1 if settings["sound"] else 0)
                elif selected_option == 1:  # Переключение языка
                    current_index = language_options.index(settings["language"])
                    settings["language"] = language_options[
                        (current_index + 1) % len(language_options)
                    ]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Перемещение вниз
                    selected_option = (selected_option + 1) % 2
                elif event.key == pygame.K_UP:  # Перемещение вверх
                    selected_option = (selected_option - 1) % 2
                elif event.key == pygame.K_RETURN:  # Выбор опции
                    if selected_option == 0:  # Переключение звука
                        settings["sound"] = not settings["sound"]
                        pygame.mixer.music.set_volume(1 if settings["sound"] else 0)
                    elif selected_option == 1:  # Переключение языка
                        current_index = language_options.index(settings["language"])
                        settings["language"] = language_options[
                            (current_index + 1) % len(language_options)
                        ]

        # Рисование фона
        screen.blit(background_image, (0, 0))

        # Заголовок "Настройки"
        title_text = font.render(get_translation("title"), True, text_color)
        title_rect = title_text.get_rect(center=(400, 100))
        screen.blit(title_text, title_rect)

        # Отображение настроек
        sound_text = f"{get_translation('sound')}: {'On' if settings['sound'] else 'Off'}"
        language_text = f"{get_translation('language')}: {settings['language']}"
        options = [sound_text, language_text]

        for i, option in enumerate(options):
            color = button_hover_color if i == selected_option else button_color
            option_text = small_font.render(option, True, text_color)
            option_rect = option_text.get_rect(center=(400, 200 + i * 100))
            pygame.draw.rect(screen, color, option_rect.inflate(20, 10), border_radius=15)
            screen.blit(option_text, option_rect)

        # Кнопка "Назад"
        pygame.draw.rect(screen, button_color, back_button_rect, border_radius=15)
        pygame.draw.rect(screen, button_border_color, back_button_rect, width=2, border_radius=15)
        back_text = small_font.render(get_translation("back"), True, text_color)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        # Обновление экрана
        pygame.display.flip()

    pygame.mixer.music.stop()

# Тестирование вызова настроек
if __name__ == "__main__":
    open_settings()

    # Проверка сохранённых настроек
    print("Сохранённые настройки:", settings)
