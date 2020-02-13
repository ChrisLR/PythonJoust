import os
import pygame


class SilentMixer(object):
    """
    This allows the game to be silent when configured so without using special code
    """
    def play(self, sound_name):
        pass

    def play_bump(self):
        pass

    def play_flap(self):
        pass

    def play_skid(self):
        pass


class SoundMixer(object):
    sound_folder = os.path.join("pythonjoust", "sounds")

    def __init__(self):
        self.channel = pygame.mixer.Channel(1)
        self.channel.set_volume(0.1)
        self.sound_names = [
            sound_name for sound_name in os.listdir(self.sound_folder)
            if sound_name.endswith(".wav")
        ]
        self.sounds = {
            sound_name: pygame.mixer.Sound(os.path.join(self.sound_folder, sound_name))
            for sound_name in self.sound_names
        }

    def play(self, sound_name):
        self.channel.stop()
        sound = self.sounds.get(sound_name)
        if sound is not None:
            self.channel.play(sound)

    def play_bump(self):
        # Convenience method
        self.play("joustthu.wav")

    def play_flap(self):
        # Convenience method
        self.play("joustflaedit.wav")

    def play_skid(self):
        # Convenience method
        self.play("joustski.wav")
