from cv2 import cv2
from pyzbar import pyzbar
import time

CAP_DURATION = 10

def qrDecode(musics):
    t = time.time()
    m = ''
    try:
        capture = cv2.VideoCapture(0)

        while((time.time() - t) < CAP_DURATION):
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


def qrDecodeTest():
    capture = cv2.VideoCapture(0)

    while (True):
        # 获取一帧
        ret, frame = capture.read()
        # 将这帧转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = pyzbar.decode(gray)  # 解析二维码
        # print(result)
        for d in result:
            print(d.data.decode('utf-8'))

        cv2.imshow('Capture', gray)
        if cv2.waitKey(1) == ord('q'):
            break
    capture.release()
qrDecode('aaa')
#qrDecodeTest()
# [Decoded(data=b'http://weixin.qq.com/r/yzvcxDfESWo2rXOn927Z', type='QRCODE', rect=Rect(left=327, top=172, width=193, height=193), polygon=[Point(x=327, y=176), Point(x=328, y=363), Point(x=520, y=365), Point(x=517, y=172)])]
# [Decoded(data=b'http://weixin.qq.com/r/yzvcxDfESWo2rXOn927Z', type='QRCODE', rect=Rect(left=327, top=172, width=193, height=193), polygon=[Point(x=327, y=177), Point(x=328, y=363), Point(x=520, y=365), Point(x=517, y=172)])]
