# Alpha-DoMi

**Artificial Intelligence-based Musical Instrument Accompaniment System** — a Raspberry Pi cello practice companion.

Tap **Play** and, after a countdown, a MIDI backing track (Pachelbel's Canon) plays while the app listens to the microphone, detects your pitch in real time, and matches it against the melody in the score. Correct notes earn a success sound and a flashing *great!* graphic; at the end of the track your run is graded (more than 50% of notes matched plays a "great" fanfare, otherwise a "try again" one). Chinese-language practice tips for string players live in `hints.txt`.

## Features

- **MIDI backing-track playback** via `pygame.mixer` — plays any `.mid` file in `music/`
- **Real-time pitch detection** from the mic (`audio_dsp_sample.py`): a DFT-peak pitch follower built on AudioLazy + numpy, biased toward the fundamental so it tracks the played note a few times a second
- **Score following**: `mido_lib.py` parses the backing track, extracts the melody from any track named *cello* or *solo*, and the main loop scores your playing against the expected notes
- **Live feedback**: current and upcoming notes on screen, a running matched/total score, a per-note success sound, and end-of-track great/bad jingles
- **Practice hints** from `hints.txt` (toggle with `HINT_VISIBLE` in `m.py`)
- **QR-code song selection** (present but not wired in — the call in `m.py` is commented out): `ls_camera.py` / `qr_sample.py` decode a QR code with the Pi camera + OpenCV/pyzbar, matching it against the song list; printable codes ship in `imgs/brCode*.png`. An MFRC522 RFID driver (`MFRC522V2.py`) is also bundled for future tag-based selection.

## Requirements

- Raspberry Pi (or any desktop, for development) with a microphone, speakers, and a 1024×580 display with mouse/touch
- Python 3 with `pygame`, `mido`, `audiolazy`, and `numpy` (AudioLazy needs PortAudio for mic capture — on Raspberry Pi OS, `sudo apt install libportaudio2`)
- Pi-only extras for the hardware paths: `picamera`, `opencv-python`, `pyzbar` (camera/QR) and `pyalsaaudio`, `RPi.GPIO`, `spidev`
- `ls_camera_mock.py` / `ls_sound_mock.py` stand in for the Pi hardware, so the app runs on a plain desktop as-is
- CJK-capable system fonts (SimSun/NSimSun, WenQuanYi Micro Hei) for the Chinese on-screen text

## Getting started

```sh
python3 m.py
```

Pass an optional PortAudio API name to choose the audio backend, e.g. `python3 m.py jack`. Press **Play** to start; **Pause** and **Stop** control playback. For autostart on the Pi, install the project at `/home/pi/k/` and copy the `k.desktop` launcher to an autostart location.

> **Note:** the sound-effect paths in `m.py` and `pgtest.py` are written Windows-style (`.\music\...`); switch them to forward slashes (`./music/...`) before running on Linux / Raspberry Pi OS.

## Project structure

| Path | Role |
|---|---|
| `m.py` | Main application — pygame UI, playback, countdown, scoring loop |
| `mido_lib.py` | MIDI score parser and note matcher |
| `audio_dsp_sample.py` | Microphone pitch-detection engine (AudioLazy) |
| `ls_camera.py` / `ls_sound.py` (+ `_mock`) | Pi camera/QR and ALSA sound modules, with desktop mocks |
| `MFRC522V2.py` | MFRC522 RFID driver (bundled, not yet used) |
| `music/`, `imgs/` | Backing track, sound effects, UI graphics, and QR print-outs |
| `k.desktop`, `hints.txt` | Pi launcher and practice tips |
| `qr_sample.py`, `recordwav.py`, `patest.py`, `pgtest.py`, `pg_template.py`, `tt.py` | Standalone samples and scratch scripts |

## License

Licensed under the **GNU General Public License v3.0** — see [LICENSE](LICENSE). The project bundles third-party code under compatible licenses, each keeping its original header: the AudioLazy example code in `audio_dsp_sample.py` and `audio_play_sample.py` (GPL-3.0, © Danilo de Jesus da Silva Bellini) and the MFRC522 RFID driver `MFRC522V2.py` (LGPL-3.0, © Mario Gomez).
