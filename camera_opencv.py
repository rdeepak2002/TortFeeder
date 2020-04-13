import os
import cv2
from base_camera import BaseCamera
from datetime import datetime

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        # Cascade for detecting faces (disabled due to system limitations)
        # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        while True:
            # read current frame
            _, img = camera.read()

            # font
            font = cv2.FONT_HERSHEY_SIMPLEX

            # org
            org = (50, 50)

            # fontScale
            fontScale = 1

            # Blue color in BGR
            color = (255, 255, 255)

            # Line thickness of 2 px
            thickness = 2

            # Get date and time
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            # Using cv2.putText() method
            img = cv2.putText(img, dt_string, org, font, fontScale, color, thickness, cv2.LINE_AA)

            # Detect faces and draw rectangle around each face (disabled due to system limitations)
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # faces = face_cascade.detectMultiScale(gray, 1.4, 4)
            # for (x, y, w, h) in faces:
            #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
