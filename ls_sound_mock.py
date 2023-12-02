#!/usr/bin/env python

# Simple test script that plays (some) wav files

from __future__ import print_function

import time
from audio_dsp_sample import *
import _thread

WAV_DEFAULT = './music/canon.mid'


class LsSound(object):
    running = False
    recoding = False
    inp = None
    notes = set()
    note = 0
    device = None

    def __init__(self, device=None):
        pass

    def device_init(self):
        pass

    def playToDevice(self, device, f):
        pass

    def play(self, wav_name=WAV_DEFAULT):
        pass

    def play_loop(self, wav_name=WAV_DEFAULT):
        pass

    def record_loop(self, msg):
        pitches = iter(midi_pitch_from_mic(50))
        while True:
            print('start recording')
            note = next(pitches)
            try:
                if note < 35 or note > 80:
                    continue
                self.note = int(note)
                # self.notes.clear()
                # self.notes.add(note)
                print('note=', int(note))

            except:
                pass

    def start_record(self):
        if not self.running:
            self.running = True
            #_thread.start_new_thread(self.record_loop, ('',))

    def stop(self):
        pass

    def usage(self, ):
        print('usage: playwav.py [-d <device>] <file>', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    # pitches = iter(midi_pitch_from_mic(100))
    # while True:
    #     x =next(pitches)
    #     print(x)
    s = LsSound()

    s.start_record()

    time.sleep(300)



