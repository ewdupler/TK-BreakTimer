# Music.py for jeopardy them song

import time
import pygame

class songtime:
    def __init__(self):
        self.song = './Jeopardy-theme-song.mp3'
        self.channel = ""
        self.event = ""

    def loop(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.play(loops=-1)

    def stop(self):
        pygame.mixer.music.stop()

if __name__ == '__main__':

    sound = songtime()
    sound.loop()
    time.sleep(3)
    sound.stop()