import time


MOTION_DEFAULT = ''
MOTION_SAD = 'sad'
MOTION_HAPPY = 'happy'
CAP_DURATION = 10

class LsCamera(object):
    camera = None

    motion = ''

    running = False
    detecting = False

    def __init__(self):
        pass

    def start(self):
        pass

    def startDetect(self):
        pass

    def stop(self):
        pass

    def imgCapture(self):
        pass

    def qrDecode(self, musics):
        return "canon.mid"

    def motion_detect(self):
        pass


if __name__ == '__main__':
    lsCamera = LsCamera()
    lsCamera.start()
    time.sleep(3.0)
    lsCamera.stop()