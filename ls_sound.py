#!/usr/bin/env python

# Simple test script that plays (some) wav files

from __future__ import print_function

import sys
import wave
import getopt
import alsaaudio
import _thread
import time
import pygame.midi

WAV_DEFAULT = './music/canon.mid'

class LsSound(object):
    running = False
    recoding = False
    inp = None
    notes = set()

    def __init__(self, device='default'):
        if device is None:
            self.device = alsaaudio.PCM(device="default")
        else:
            self.device = device


    def device_init(self):
        if self.device is None:
            return
        # Set attributes

    def playToDevice(self, device, f):
        print('%d channels, %d sampling rate\n' % (f.getnchannels(),
                                                   f.getframerate()))
        # Set attributes
        device.setchannels(f.getnchannels())
        device.setrate(f.getframerate())

        # 8bit is unsigned in wav files
        if f.getsampwidth() == 1:
            device.setformat(alsaaudio.PCM_FORMAT_U8)
        # Otherwise we assume signed data, little endian
        elif f.getsampwidth() == 2:
            device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        elif f.getsampwidth() == 3:
            device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
        elif f.getsampwidth() == 4:
            device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
        else:
            raise ValueError('Unsupported format')

        periodsize = int(f.getframerate() / 8)

        device.setperiodsize(periodsize)

        data = f.readframes(periodsize)
        while data and self.running:
            # Read data from stdin
            device.write(data)
            data = f.readframes(periodsize)

    def play(self, wav_name=WAV_DEFAULT):
        if not self.running:
            self.running = True
            _thread.start_new_thread(self.play_loop, (wav_name,))

    def play_loop(self, wav_name=WAV_DEFAULT):
        f = wave.open(wav_name, 'rb')
        device = alsaaudio.PCM(device="default")
        try:
            self.playToDevice(device, f)
        finally:
            f.close()
        self.running = False

    def start_record(self):
        if self.recoding:
            return

        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device="default")

        # Set attributes: Mono, 44100 Hz, 16 bit little endian samples
        self.inp.setchannels(2)
        self.inp.setrate(16000)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.inp.setperiodsize(160)#10ms
        self.recoding = True

        _thread.start_new_thread(self.record_loop, ('',))

    def record_loop(self):

        while self.recoding:
            l, data = self.inp.read()
            self.notes.clear()
            for fq in data:
                note = pygame.midi.frequency_to_midi(fq)
                if note<30 or note >80:
                    continue
                self.notes.add(note)

    def stop(self):
        self.running = False

    def usage(self, ):
        print('usage: playwav.py [-d <device>] <file>', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':

    s = LsSound()

    s.start_record()
    s.play(WAV_DEFAULT)
    time.sleep(10)



