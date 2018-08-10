import cv2
import dlib
from threading import Thread
import numpy as np


class webcam():

    def __init__(self):
        self.cap=cv2.VideoCapture(0)
        self.frame=self.cap.read()[1]
        # self.face = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.centerX = 50
        self.centerY = 50
        self.hmax = 20
        # Create the tracker we will use
        self.tracker = dlib.correlation_tracker()
        self.tracking_face = 0
    def rect_to_bb(self, rect):

        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y
        return (x, y, w, h)

    def update(self):

        while True:
            ret, img = self.cap.read()
            if ret == False:
                break
            # tracking

            self.frame = img
            baseImage = img

            if not self.tracking_face:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                rects = self.detector(gray, 1)
                max_area = 0
                xmax = 0
                ymax = 0
                wmax = 0
                hmax = 0
                for (i, rect) in enumerate(rects):
                    (x, y, w, h) = self.rect_to_bb(rect)

                    if w * h > max_area:
                        xmax = x
                        ymax = y
                        wmax = w
                        hmax = h
                        max_area = wmax * hmax
                if max_area > 0:
                    self.tracker.start_track(baseImage,
                                        dlib.rectangle(x - 10, y - 20, x + w + 10, y + h + 20))

                    self.tracking_face = 1

                self.centerX  = xmax +  wmax/2
                self.centerY =  ymax +  hmax/ 2
                self.hmax = hmax
                cv2.rectangle(img, (xmax, ymax), (xmax + wmax, ymax + hmax), (0, 255, 0), 1)

            if self.tracking_face:
                trackingQuality = self.tracker.update(baseImage)
                if trackingQuality >= 1.2:
                    tracked_position = self.tracker.get_position()
                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())
                    cv2.rectangle(img, (t_x, t_y), (t_x + t_w, t_y + t_h), (0,255,0), 1)
                    self.centerX = t_x + t_w / 2
                    self.centerY = t_y + t_h / 2
                    self.hmax = t_h
                else:
                    self.tracking_face = 0
            self.frame =  baseImage

            #

            # cv2.imshow("video thred", img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    def thread_webcam(self):
        Thread(None,self.update).start()
    def get_currentFrame(self):
        return self.frame
    def get_currentPos(self):
        return self.centerX,self.centerY,self.hmax
