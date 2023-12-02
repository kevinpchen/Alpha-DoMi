# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
import os.path
from mido_lib import *
import time
from ls_camera_mock import *
from audio_dsp_sample import *
import random

# from qr_sample import *

SCREEN_SIZE = (1024, 580)
# 存放音乐文件的位置
MUSIC_PATH = "music"
FONT_NAME = 'simsunnsimsun'
NOTE_FONT_SIZE = 80
musics = ['canon.mid']
HINT_VISIBLE = False

NOTE_POSITION =(200, 200)
HINT_POSITION = (100, 200)
HINT_COLOR = (100, 0, 100)
HINT_FONT_SIZE = 80

great_time = 0


def get_music(path):
    # 从文件夹来读取所有的音乐文件
    raw_filenames = os.listdir(path)

    music_files = []
    for filename in raw_filenames:
        if filename.lower().endswith('.mid'):
            music_files.append(os.path.join(MUSIC_PATH, filename))
    print(music_files)
    return sorted(music_files)

pygame.font.get_fonts()
class HintsView(object):
    hints = []
    last_render = 0
    render_intervel = 10
    curr_message = ''
    font_hint = None

    def __init__(self):
        self.init()
        self.font_hint = pygame.font.SysFont('microhei', HINT_FONT_SIZE , False)

    def init(self):
        self.hints.clear()
        with open("./hints.txt", 'r') as fin:
            for x in fin.readlines():
                self.hints.append(x)

    def render(self, surface):

        if time.time() - self.last_render > self.render_intervel:
            hint_index = int(random.random() * len(self.hints))
            if hint_index > len(self.hints):
                hint_index = len(self.hints) - 1
            if hint_index < 0:
                hint_index = 0
            self.curr_message = self.hints[hint_index]
            self.last_render = time.time()
            print('change-hint-message---------')

        lb_hints = self.font_hint.render(self.curr_message, True, HINT_COLOR)
        surface.blit(lb_hints, HINT_POSITION)


class Button(object):
    """这个类是一个按钮，具有自我渲染和判断是否被按上的功能"""

    def __init__(self, image_filename, position):
        self.position = position
        self.image = pygame.image.load(image_filename)

    def render(self, surface):
        x, y = self.position
        w, h = self.image.get_size()
        x -= w / 2
        y -= h / 2
        surface.blit(self.image, (x, y))

    def is_over(self, point):
        # 如果point在自身范围内，返回True
        point_x, point_y = point
        x, y = self.position
        w, h = self.image.get_size()
        x -= w / 2
        y -= h / 2

        in_x = x <= point_x < x + w
        in_y = y <= point_y < y + h
        return in_x and in_y


class SuccessView(object):
    """这个类是一个按钮，具有自我渲染和判断是否被按上的功能"""

    def __init__(self, image_filename, position):
        self.position = position
        self.image = pygame.image.load(image_filename)
        self.is_visible = False
        self.end_time = 0
        self.duration = 0.5
        self.flash_intervel_ms = 200  # 闪烁的时间间隔

    def render(self, surface, curr_time):
        # print(self.end_time,curr_time)
        if not self.is_visible:
            return
        if curr_time > self.end_time:
            self.is_visible = False
            return
        # 根据时间和状态来决定是否闪烁。
        if (curr_time * 1000 // self.flash_intervel_ms) % 2 == 1:
            return
        x, y = self.position
        w, h = self.image.get_size()
        x -= w / 2
        y -= h / 2
        surface.blit(self.image, (x, y))

    def flash(self, dur):
        self.end_time = dur + self.duration
        self.is_visible = True

    def is_over(self, point):
        # 如果point在自身范围内，返回True
        point_x, point_y = point
        x, y = self.position
        w, h = self.image.get_size()
        x -= w / 2
        y -= h / 2

        in_x = x <= point_x < x + w
        in_y = y <= point_y < y + h
        return in_x and in_y


class NoteView(object):
    """这个类是一个按钮，具有自我渲染和判断是否被按上的功能"""

    def __init__(self, notes=None, position=NOTE_POSITION):
        self.position = position
        self.notes = notes

    def render(self, surface, duration):
        if self.notes is None:
            return
        x, y = self.position

        font = pygame.font.SysFont(FONT_NAME, NOTE_FONT_SIZE, False)
        curr_notes = self.notes.get_curr_notes(duration)
        for idx, note in enumerate(curr_notes):
            font_surface = font.render(str(note.note_name), True, (0, 250, 0))
            surface.blit(font_surface, (x + idx * NOTE_FONT_SIZE * 2, y))
        near_notes = self.notes.get_nearby_notes(duration)
        for idx, note in enumerate(near_notes):
            if idx > 4:
                break
            font_surface = font.render(str(note.note_name), True, (100, 0, 100))
            surface.blit(font_surface, (x + idx * NOTE_FONT_SIZE * 2, y + NOTE_FONT_SIZE + 10))

    def reload_note(self, notes):
        self.notes = notes


class ScoreView(object):
    """这个类是一个按钮，具有自我渲染和判断是否被按上的功能"""

    def __init__(self, ):
        pass

    def render(self, surface, scores):
        font = pygame.font.SysFont(FONT_NAME, 60, False)

        score_surface_success = font.render(str(scores[0]), True, (20, 250, 20))
        surface.blit(score_surface_success, (SCREEN_SIZE[0] - 3 * 90, 30))

        score_surface_all = font.render(str(scores[1]), True, (20, 20, 250))
        surface.blit(score_surface_all, (SCREEN_SIZE[0] - 2 * 90, 30))

        # score_surface_fail = font.render(str(scores[2]), True, (250, 20, 20))
        # surface.blit(score_surface_fail, (SCREEN_SIZE[0] - 1 * 90, 30))


def run():
    #
    pygame.mixer.pre_init(44100, 16, 2, 1024 * 4)
    pygame.init()
    pygame.mixer.music.set_volume(1)
    sound_success = pygame.mixer.Sound(r".\music\sfx_point.wav")  # 加载音频文件
    sound_success.set_volume(0.8)  # 加载的音量大小
    sound_great = pygame.mixer.Sound(r".\music\great.wav")  # 加载音频文件
    sound_great.set_volume(0.8)  # 加载的音量大小
    sound_bad = pygame.mixer.Sound(r".\music\bad.wav")  # 加载音频文件
    sound_bad.set_volume(0.8)  # 加载的音量大小

    close = False
    screen = pygame.display.set_mode(SCREEN_SIZE, 0)

    background = pygame.image.load('./imgs/bg.png')
    screen.blit(background, (0, 0))  # 对齐的坐标

    # font = pygame.font.SysFont("default_font", 50, False)
    # 为了显示中文，我这里使用了这个字体，具体自己机器上的中文字体请自己查询
    # 详见本系列第四部分：//eyehere.net/2011/python-pygame-novice-professional-4/
    font = pygame.font.SysFont(FONT_NAME, 50, False)
    font_count_down = pygame.font.SysFont(FONT_NAME, 200, False)

    # ----初始化最下方按钮----
    x = 300
    y = 500
    button_width = 150
    buttons = {}
    #    buttons["prev"] = Button("./imgs/rew.png", (x, y))
    buttons["camera"] = Button("./imgs/camera.png", (x, y))
    buttons["pause"] = Button("./imgs/pause.png", (x + button_width * 1, y))
    buttons["stop"] = Button("./imgs/stop.png", (x + button_width * 2, y))
    buttons["play"] = Button("./imgs/play.png", (x + button_width * 3, y))
    #    buttons["next"] = Button("./imgs/next.png", (x + button_width * 4, y))

    v_great_img = SuccessView("./imgs/great.png", (500, 150))
    v_score = ScoreView()

    # ----初始音乐列表----
    music_filenames = get_music(MUSIC_PATH)
    if len(music_filenames) == 0:
        print("No music files found in ", MUSIC_PATH)
        return
    # ----显示音乐文件名----
    white = (255, 255, 255)
    label_surfaces = []
    # 一系列的文件名render
    for filename in music_filenames:
        txt = os.path.split(filename)[-1]
        print("Track:", txt)
        # 这是简体中文Windows下的文件编码，根据自己系统情况请酌情更改
        #        txt = txt.split('.')[0].decode('gb2312')
        surface = font.render(txt, True, (100, 0, 100))
        label_surfaces.append(surface)

    # 读取并准备播放当前音频
    current_track = 0
    max_tracks = len(music_filenames)
    pygame.mixer.music.load(music_filenames[current_track])

    clock = pygame.time.Clock()
    playing = False
    paused = False
    mid = None

    TRACK_END = USEREVENT + 1
    pygame.mixer.music.set_endevent(TRACK_END)

    scores = [0, 0, 0, 0]

    v_notes = NoteView()
    v_hints = HintsView()

    timer = time.time()
    dur = 0
    counting = False
    count_down_max = 6

    while True:
        button_pressed = None

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                exit
                close = True

            if event.type == MOUSEBUTTONDOWN:

                # 判断哪个按钮被按下
                for button_name, button in buttons.items():
                    if button.is_over(event.pos):
                        print(button_name, "pressed")
                        button_pressed = button_name
                        break

            if event.type == TRACK_END:
                # 如果一曲播放结束，就“模拟”按下"next"
                button_pressed = "next"
                # 播放结束，评分
                if scores[1] > 0:
                    sc = int((scores[0] / scores[1]) * 100)
                    if sc > 50:
                        sound_great.play()
                    else:
                        sound_bad.play()

        if close:
            break

        if button_pressed is not None:

            if button_pressed == "next":
                current_track = (current_track + 1) % max_tracks
                pygame.mixer.music.load(music_filenames[current_track])
                if playing:
                    pygame.mixer.music.play()

            elif button_pressed == "prev":

                # prev的处理方法：
                # 已经播放超过3秒，从头开始，否则就播放上一曲
                if pygame.mixer.music.get_pos() > 3000:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play()
                else:
                    current_track = (current_track - 1) % max_tracks
                    pygame.mixer.music.load(music_filenames[current_track])
                    if playing:
                        pygame.mixer.music.play()

            elif button_pressed == "pause":
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    pygame.mixer.music.pause()
                    paused = True

            elif button_pressed == "stop":
                pygame.mixer.music.stop()
                playing = False
                timer = time.time()

            elif button_pressed == "camera":
                pygame.mixer.music.stop()
                playing = False
                # curr_music = qrDecode(musics)
                current_track = 0

            elif button_pressed == "play":
                if paused:
                    pygame.mixer.music.unpause()
                    scores = [0, 0, 0, 0]
                    paused = False
                else:
                    if not playing:
                        mid = IvyMidi()
                        mid.open()
                        v_notes.reload_note(mid)
                        v_great_img.end_time = 0
                        pygame.mixer.music.load(music_filenames[current_track])
                        pitches = iter(midi_pitch_from_mic(100))
                        playing = True

                        timer = time.time()
                        counting = True
                        scores = [0, 0, 0, 0]

        screen.fill(white)
        screen.blit(background, (0, 0))  # 对齐的坐标

        # 写一下当前歌名
        label = label_surfaces[current_track]
        w, h = label.get_size()
        screen_w = SCREEN_SIZE[0]
        screen.blit(label, ((screen_w - w) / 2, 420))

        # scores = [all, correct, fail, curr_score]
        v_score.render(screen, scores)
        # 画所有按钮
        for button in buttons.values():
            button.render(screen)

        # 画提示文字。非播放和倒计时状态运行
        if not playing and not counting and HINT_VISIBLE:
            v_hints.render(screen)

        if playing and not (mid is None) and dur > mid.end_timeing:
            pygame.mixer.music.stop()
            dur = 0
            playing = False

        # 主体
        if counting:
            cd = int(count_down_max - (time.time() - timer))
            if cd < 1:
                pygame.mixer.music.play()
                counting = False
            else:
                lb_count_down = font_count_down.render(str(cd), True, (100, 0, 100))
                screen.blit(lb_count_down, (400, 200))

        elif playing and not (mid is None):
            dur = pygame.mixer.music.get_pos() / 1000
            print(dur)
            # 接收当前录音设备收集到的音符
            note = 30
            try:
                note = next(pitches)
            except:
                pass
            if note < 35 or note > 80:
                continue
            note = int(note)

            n_surface = font.render(str(note), True, (100, 0, 100))
            screen.blit(n_surface, (10, 10))

            print(note)
            scores[1] = len(mid.ivy_notes)
            # 获取当前正在播放的音符
            cnotes = mid.get_curr_notes(dur)

            for mid_note in cnotes:
                if mid_note.score > 0:
                    continue
                # for n in notes:
                if mid_note.compare(note, dur) > 0:
                    mid_note.score = 1
                    # 匹配了
                    print('ok=', note)
                    v_great_img.flash(dur)
                    scores[0] = scores[0] + 1
                    sound_success.play()
                    break
            v_notes.render(screen, dur)

        v_great_img.render(screen, dur)
        # 帧率
        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    run()
