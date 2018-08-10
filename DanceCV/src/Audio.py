# -*- coding: utf-8 -*-


import pygame
import sys


# Audioo class

class Audio():
    def __init__(self):
        pass

    def pre_open(self, frequency=44100, bits=16, stereo=True, bufferSize=1024):
        pygame.mixer.pre_init(frequency, -bits, stereo and 2 or 1, bufferSize)
        return True

    def open(self, frequency=44100, bits=16, stereo=True, bufferSize=1024):
        try:
            pygame.mixer.quit()
        except:
            pass

        try:
            pygame.mixer.init(frequency, -bits, stereo and 2 or 1, bufferSize)
        except:
            pygame.mixer.init()

        return True

    def getChannelCount(self):
        return pygame.mixer.get_num_channels()

    def getChannel(self, n):
        return Channel(n)

    def close(self):
        pygame.mixer.quit()

    def pause(self):
        pygame.mixer.pause()

    def unpause(self):
        pygame.mixer.unpause()

class Music():
    def __init__(self, fileName):
        pygame.mixer.music.load(fileName)

    @staticmethod
    def setEndEvent(event):
        pygame.mixer.music.set_endevent(event)

    def play(self, loops= -1, pos=0.0):
        pygame.mixer.music.play(loops, pos)

    def stop(self):
        pygame.mixer.music.stop()

    def rewind(self):
        pygame.mixer.music.rewind()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def fadeout(self, time):
        pygame.mixer.music.fadeout(time)

    def isPlaying(self):
        return pygame.mixer.music.get_busy()

    def getPosition(self):
        return pygame.mixer.music.get_pos()

class Channel(object):
    def __init__(self, id):
        self.channel = pygame.mixer.Channel(id)

    def play(self, sound):
        self.channel.play(sound.sound)

    def stop(self):
        self.channel.stop()

    def setVolume(self, volume):
        self.channel.set_volume(volume)

    def fadeout(self, time):
        self.channel.fadeout(time)

class Sound(object):
    def __init__(self, fileName):
        self.sound = pygame.mixer.Sound(fileName)

    def play(self, loops=0):
        self.sound.play(loops)

    def stop(self):
        self.sound.stop()

    def setVolume(self, volume):
        self.sound.set_volume(volume)

    def fadeout(self, time):
        self.sound.fadeout(time)
        
        

class StreamingSound(Sound):
    def __init__(self, engine, channel, fileName):
        Sound.__init__(self, fileName)

