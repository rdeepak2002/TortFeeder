import os
import cv2
from base_camera import BaseCamera


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

        # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        while True:
            # read current frame
            _, img = camera.read()


            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect the faces
            # faces = face_cascade.detectMultiScale(gray, 1.4, 4)
            # Draw the rectangle around each face
            # for (x, y, w, h) in faces:
            #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
