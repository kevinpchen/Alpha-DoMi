import pygame as pygame
import pyaudio
import struct

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# SETTINGS
size = (256, 256)
chunk = 1024
stepsize = 1
filter_255 = False
filter_2 = True

max_fps = 100
width_of_col = 1
scale = 1
skip_under = 0

# Init
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("AV")
done = False
clock = pygame.time.Clock()


class AudioStream():
    def __init__(self, device_index, device_channels=1, inp=True, outp=True, chunksize=1024):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=device_channels,
            rate=44100,
            input=inp,
            output=outp,
            # as_loopback=True,
            input_device_index=device_index,  # 0 laptop ,1 loopback , 3 fejes
            frames_per_buffer=chunksize
        )


recordStream = AudioStream(1, 1, True, True, chunk)
playbackStream = AudioStream(12, 1, False, True, chunk)


# USE THIS TO GET THE DEVICE INDEXES
# for i in range(p.get_device_count()):
#    print(f'{i} {p.get_device_info_by_index(i)["name"]}')

def draw(data):
    global size, stepsize
    pygame.draw.line(screen, WHITE, (0, size[1] // 2), (size[0], size[1] // 2), 1)

    x = 0
    for i in range(len(data) // stepsize):
        if i % 2 == 0 and filter_2:
            # x += 1
            continue

        if x > size[0]:
            continue

        if data[i * stepsize] >= 255 and filter_255:
            continue

        if data[i * stepsize] < skip_under:
            continue

        if data[i * stepsize] > 127:
            pygame.draw.line(screen, WHITE, (x, size[1] // 2), (x, size[1] - data[i * stepsize] * scale + 127),
                             width_of_col)
        else:
            pygame.draw.line(screen, WHITE, (x, size[1] // 2), (x, -data[i * stepsize] * scale + 127), width_of_col)
        x += 1


def main():
    global done, max_fps, chunk, screen, scale, clock
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # read data
        temp = recordStream.stream.read(chunk)
        playbackStream.stream.write(temp)
        data = struct.unpack(f"{str(2 * chunk)}B", temp)

        # clear screen
        screen.fill(BLACK)

        # draw new screen
        draw(data)

        # display new screen
        pygame.display.flip()

        # display fps
        pygame.display.set_caption(f"Audio-visualisation {int(clock.get_fps()) + 1}fps")

        # tick the clock
        clock.tick(max_fps)

    pygame.quit()
    return


if __name__ == "__main__":
    main()