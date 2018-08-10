#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Resource import Resource
from Audio import Audio
from Scene import Scene
from Song import Song, Note, loadSong
from Input import Input
import pygame
from pygame.locals import *
import sys
import getopt
import Constants
#import cProfile as profile

class DanceCV():
    def __init__(self, song, speed):

        self.input = Input()
        self.resource = Resource()
        self.audio = Audio()
        self.audio.pre_open()
        pygame.init()
        self.audio.open()
        if song != None:
            self.song = loadSong(self.resource, song)
        else:
            self.song = loadSong(self.resource, "gangnam")
        self.clock = pygame.time.Clock()
        pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        pygame.display.set_caption("DanceCV")
        screen = pygame.display.get_surface()
        if speed != None:
            self.scene = Scene(self.resource, self.song, screen, self.input, speed)
        else:
            self.scene = Scene(self.resource, self.song, screen, self.input, 2)

        
        
    def run(self):
        while True:
            for events in pygame.event.get():
                if events.type == QUIT:
                    sys.exit(0)
            self.input.run()
            self.scene.run()
            pygame.display.update()
            self.clock.tick(30)
    
    
    
if __name__ == "__main__":
    song = None
    speed = None
    options, remainder = getopt.getopt(sys.argv[1:], 's:x:')
    for opt, arg in options:
        
        if opt in ('-s'):
            song = arg
        elif opt in ('-x'):
            speed = float(arg)
    game = DanceCV(song, speed)
    game.run()
    
