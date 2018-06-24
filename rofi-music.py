#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from rofi import Rofi

class RofiTunes:
    def __init__(self):
        self.rofi = Rofi()
        self.songs = []

    def build_library(self):
        proc = subprocess.Popen(['mpc', 'listall'], stdout=subprocess.PIPE)
        for song in proc.stdout.readlines():
            self.songs.append(song.decode())

    def build_menu(self):
        choice = self.rofi.select(">", self.songs, key1=("Alt+1", "Description"))
        print(choice)
        if choice[1] >= 1:
            # NOTE: A hotkey was pushed
            pass
        elif choice[0] != -1:
            return self.play_song(choice[0])

    def play_song(self, choice):
        proc = subprocess.Popen(['mpc', 'play', str(choice)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
        print(self.songs[choice].strip())
        try: 
            outs, errs = proc.communicate(timeout=15)
            print(outs.decode())
            print(errs.decode())
        except TimeoutError:
            proc.kill()
            outs, errs = proc.communicate()
            print(outs.decode())
            print(errs.decode())
    
if __name__ == '__main__':
    r = RofiTunes()
    r.build_library()
    r.build_menu()
