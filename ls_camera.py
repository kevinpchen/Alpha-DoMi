from picamera import PiCamera
from io import BytesIO
from cv2 import cv2
import time
import _thread

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
        self.camera = PiCamera()

    def start(self):
        self.running = True
        self.detecting = True
        _thread.start_new_thread(self.motion_detect, ())

    def startDetect(self):
        self.detecting = True

    def stop(self):
        self.detecting = False

    def imgCapture(self):

        # camera.rotation = 180
        # Make the camera preview see-through by setting an alpha level:
        # camera.start_preview(alpha=200)
        self.camera.capture('/home/pi/Desktop/image.jpg')
        # my_stream = BytesIO()
        # camera = PiCamera()
        # camera.start_preview()
        # # Camera warm-up time
        # camera.capture(my_stream, 'jpeg')
        # image_data = my_stream.getvalue()

        #self.camera.start_preview()

        #self.camera.stop_preview()

    def qrDecode(self, musics):
        t = time.time()
        m = ''
        try:
            capture = cv2.VideoCapture(0)

            while ((time.time() - t) < CAP_DURATION):
                # 获取一帧
                ret, frame = capture.read()
                # 将这帧转换为灰度图
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result = pyzbar.decode(gray)  # 解析二维码
                # print(result)
                isFound = False
                for d in result:
                    s = d.data.decode('utf-8')
                    print(s)
                    if s in musics:
                        m = s
                        isFound = True
                cv2.imshow('Capture', gray)
                if cv2.waitKey(1) == ord('q'):
                    break
                if isFound:
                    break

            cv2.destroyAllWindows()
            capture.release()
        except:
            pass
        return m

    def motion_detect(self):
        while self.running:
            if self.detecting:
                pass


if __name__ == '__main__':
    lsCamera = LsCamera()
    lsCamera.start()
    time.sleep(3.0)
    lsCamera.stop()