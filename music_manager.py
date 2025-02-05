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
        
        self.current_music = None
        self.is_playing = False
        self.volume = 0.5

    def play_music(self, music_file):
        """Воспроизводит музыку"""
        if self.current_music != music_file:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # -1 для бесконечного повтора
            pygame.mixer.music.set_volume(self.volume)
            self.current_music = music_file
            self.is_playing = True

    def ensure_playing(self):
        """Убеждается, что музыка продолжает играть"""
        if not pygame.mixer.music.get_busy() and self.current_music:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.volume)
            self.is_playing = True

    def stop_music(self):
        """Останавливает музыку"""
        pygame.mixer.music.stop()
        self.is_playing = False

    def set_volume(self, volume):
        """Устанавливает громкость"""
        self.volume = volume
        pygame.mixer.music.set_volume(volume)

    def play_menu_music(self):
        if not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f"Не удалось загрузить музыку: {self.music_path}")
                print(f"Ошибка: {e}")
    
    def toggle_music(self, should_play):
        if should_play:
            pygame.mixer.music.set_volume(0.5)
            if not pygame.mixer.music.get_busy():
                self.play_menu_music()
        else:
            pygame.mixer.music.set_volume(0.0)

# Создаем глобальный экземпляр
music_manager = MusicManager() 