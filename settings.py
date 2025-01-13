import pygame
import os
import sys

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape from AB")

# Загрузка изображения фона
image_folder = "images/bg"
image_path = os.path.join(image_folder, "road.jpg")
background_image = pygame.image.load(image_path)

# Загрузка музыки
music_path = "audio/test_music.mp3"  # Тестовый файл музыки
pygame.mixer.init()

# Настройки
settings = {
    "sound": True,  # Звук включён по умолчанию
    "language": "Русский",  # Язык по умолчанию
}

# Цвета
text_color = (0, 0, 0)  # Чёрный цвет текста
button_color = (200, 200, 200)
button_hover_color = (170, 170, 170)

# Шрифты
font = pygame.font.Font(None, 60)  # Основной шрифт
small_font = pygame.font.Font(None, 40)  # Шрифт для кнопок

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
    language_options = ["Русский", "English", "Français"]
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Перемещение вниз
                    selected_option = (selected_option + 1) % 2
                elif event.key == pygame.K_UP:  # Перемещение вверх
                    selected_option = (selected_option - 1) % 2
                elif event.key == pygame.K_RETURN:  # Выбор опции
                    if selected_option == 0:  # Переключение звука
                        settings["sound"] = not settings["sound"]
                        if not settings["sound"]:
                            pygame.mixer.music.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(1)
                    elif selected_option == 1:  # Переключение языка
                        current_index = language_options.index(settings["language"])
                        settings["language"] = language_options[
                            (current_index + 1) % len(language_options)
                        ]

        # Рисование фона
        screen.blit(background_image, (0, 0))

        # Заголовок "Настройки"
        title_text = font.render("Настройки", True, text_color)
        title_rect = title_text.get_rect(center=(400, 100))
        screen.blit(title_text, title_rect)

        # Отображение настроек
        sound_text = f"Звук: {'Включён' if settings['sound'] else 'Выключен'}"
        language_text = f"Язык: {settings['language']}"
        options = [sound_text, language_text]

        for i, option in enumerate(options):
            color = button_hover_color if i == selected_option else button_color
            option_text = small_font.render(option, True, text_color)
            option_rect = option_text.get_rect(center=(400, 200 + i * 100))
            pygame.draw.rect(screen, color, option_rect.inflate(20, 10), border_radius=15)
            screen.blit(option_text, option_rect)

        # Обновление экрана
        pygame.display.flip()

    pygame.mixer.music.stop()

# Тестирование вызова настроек
if __name__ == "__main__":
    open_settings()

    # Проверка сохранённых настроек
    print("Сохранённые настройки:", settings)
