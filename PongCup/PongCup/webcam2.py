import cv2
import dlib
from threading import Thread
import numpy as np


class webcam():

    def __init__(self):
        self.cap2=cv2.VideoCapture(2)
        self.frame2=self.cap2.read()[1]
        # self.face = cv2.VideoCapture(0)
        self.detector2 = dlib.get_frontal_face_detector()
        self.centerX2 = 50
        self.centerY2 = 50
        self.hmax2 = 20
        # Create the tracker we will use
        self.tracker2 = dlib.correlation_tracker()
        self.tracking_face2 = 0
    def rect_to_bb(self, rect):

        x2 = rect.left()
        y2 = rect.top()
        w2 = rect.right() - x2
        h2 = rect.bottom() - y2
        return (x2, y2, w2, h2)

    def update(self):

        while True:
            ret2, img2 = self.cap2.read()
            if ret2 == False:
                break
            # tracking

            self.frame = img2
            baseImage2 = img2

            if not self.tracking_face2:
                gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                rects2 = self.detector2(gray2, 1)
                max_area2 = 0
                xmax2 = 0
                ymax2 = 0
                wmax2 = 0
                hmax2 = 0
                for (i, rect) in enumerate(rects2):
                    (x2, y2, w2, h2) = self.rect_to_bb(rect)

                    if w2 * h2 > max_area2:
                        xmax2 = x2
                        ymax2 = y2
                        wmax2 = w2
                        hmax2 = h2
                        max_area2 = wmax2 * hmax2
                if max_area2 > 0:
                    self.tracker2.start_track(baseImage2,
                                        dlib.rectangle(x2 - 10, y2 - 20, x2 + w2 + 10, y2 + h2 + 20))

                    self.tracking_face2 = 1

                self.centerX2  = xmax2 +  wmax2/2
                self.centerY2 =  ymax2 +  hmax2/ 2
                self.hmax2 = hmax2
                cv2.rectangle(img2, (xmax2, ymax2), (xmax2 + wmax2, ymax2 + hmax2), (0, 255, 0), 1)

            if self.tracking_face2:
                trackingQuality2 = self.tracker2.update(baseImage2)
                if trackingQuality2 >= 1.2:
                    tracked_position2 = self.tracker2.get_position()
                    t_x2 = int(tracked_position2.left())
                    t_y2 = int(tracked_position2.top())
                    t_w2 = int(tracked_position2.width())
                    t_h2 = int(tracked_position2.height())
                    cv2.rectangle(img2, (t_x2, t_y2), (t_x2 + t_w2, t_y2 + t_h2), (0,255,0), 1)
                    self.centerX2 = t_x2 + t_w2 / 2
                    self.centerY2 = t_y2 + t_h2 / 2
                    self.hmax2 = t_h2
                else:
                    self.tracking_face2 = 0
            self.frame2 =  baseImage2

            #

            # cv2.imshow("video thred", img)
            key2 = cv2.waitKey(1)
            if key2 == ord('q'):
                break

    def thread_webcam2(self):
        Thread(None,self.update).start()
    def get_currentFrame2(self):
        return self.frame2
    def get_currentPos2(self):
        return self.centerX2,self.centerY2,self.hmax2
