import pygame
import os

class MusicManager:
    def __init__(self):
        # Пробуем сначала WAV, потом MP3
        self.music_path = "./assets/audio/test.wav"  # Сначала пробуем WAV
        if not os.path.exists(self.music_path):
            self.music_path = "./assets/audio/test.mp3"  # Если WAV не найден, используем MP3
        
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        
        if os.path.exists(self.music_path):
            file_size = os.path.getsize(self.music_path)
            print(f"Файл музыки найден: {self.music_path}")
            print(f"Размер файла: {file_size} байт")
        else:
            print(f"Файл музыки не найден по пути: {self.music_path}")
        
    def play_menu_music(self):
        if not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f"Не удалось загрузить музыку: {self.music_path}")
                print(f"Ошибка: {e}")
    
    def stop_music(self):
        pygame.mixer.music.stop()
    
    def toggle_music(self, should_play):
        if should_play:
            pygame.mixer.music.set_volume(0.5)
            if not pygame.mixer.music.get_busy():
                self.play_menu_music()
        else:
            pygame.mixer.music.set_volume(0.0)

# Создаем глобальный экземпляр
music_manager = MusicManager() 