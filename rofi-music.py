#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import eyed3
import subprocess
from rofi import Rofi
from argparse import ArgumentParser

'''
iterating over all the music takes too long obviously
maybe create a cache?
or maybe just piggy back off of mpd's cache?
No need to reinvent the wheel when this is meant to pair up with MPD

rofi's searching should not be case sensitive
'''

parser = ArgumentParser()
parser.add_argument('-u', '--update', default=False, action='store_true')
args = parser.parse_args()


class RofiTunes:
    def __init__(self):
        self.rofi = Rofi()
        self.songs = []
        self.mpd_dir = f"""{os.environ.get('HOME')}/.mpd"""

    def update_library(self):
        pass

    def build_library(self):
        # TODO: extract artist/genre/track ect from audio file
        proc = subprocess.Popen(['mpc', 'listall'], stdout=subprocess.PIPE)
        for song in proc.stdout.readlines():
            try:
                mp3 = eyed3.load("{}/{}".format('/home/jack/Music', song.decode('utf-8').strip())) 
                #TODO: Now you can extract all the relevant metadata
                title = mp3.tag.title
                album = mp3.tag.album
                artist = mp3.tag.artist
                self.songs.append("{} - {} - {}".format(title, album, artist))
            except AttributeError: pass
            except UnicodeDecodeError: pass
                #print("{} - Invalid or No attribute tag".format(song.decode('utf-8').strip()))

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
