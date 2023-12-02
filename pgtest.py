import pygame.midi
import time

pygame.mixer.init()  # 初始化，用于放音乐
success_sound = pygame.mixer.Sound(r".\music\sfx_point.wav")  # 加载音频文件
success_sound.set_volume(0.8)  # 加载的音量大小
pygame.mixer.music.load(r".\music\canon.mid")    # 加载音频文件
pygame.mixer.music.set_volume(0.9)  # 加载时声音大小
sound_great = pygame.mixer.Sound(r".\music\great.wav")  # 加载音频文件
sound_great.set_volume(0.8)  # 加载的音量大小
sound_bad = pygame.mixer.Sound(r".\music\bad.wav")  # 加载音频文件
sound_bad.set_volume(0.8)  # 加载的音量大小

pygame.mixer.music.play()  # 常规播放
success_sound.play()  # 循环播放
sound_bad.play()
#sound_great.play()

time.sleep(30)
print("finished.....")