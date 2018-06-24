#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from rofi import Rofi

class RofiTunes:
    def __init__(self):
        self.rofi = Rofi()
        self.songs = []

    def build_library(self, folder=f"{os.environ.get('HOME')}/Music"):
        for folderName, subfolders, filenames in os.walk(folder):
            if subfolders:
                for subfolder in subfolders:
                    self.build_library(subfolder)
            for filename in filenames:
                if 'mp3' in filename:
                    self.songs.append("{}/{}".format(folderName, filename))

    def remove_duplicates(self):
        self.songs = list(set(self.songs))

    def build_menu(self):
        self.rofi.select(">", self.songs, key1=("Alt+1", "Description"))

    
if __name__ == '__main__':
    r = RofiTunes()
    r.build_library()
    r.remove_duplicates()
    r.build_menu()
