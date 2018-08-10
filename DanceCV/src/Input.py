# -*- coding: utf-8 -*-

import cv2
import cv2.cv as cv
import numpy
import pygame
import Constants



class Input():
    def __init__(self, debug = False):
        
        self.capture = cv2.VideoCapture(0)
        if self.capture.isOpened():         # Checks the stream
            self.frameSize = (int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)),
                               int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)))        
        Constants.SCREEN_HEIGHT = self.frameSize[0]
        Constants.SCREEN_WIDTH = self.frameSize[1]
        self.bsmog = []
        self.bgAdapt = []

        history = 100 
        nGauss = 20 
        bgThresh = 0.2
        noise = 7
        
        for i in range(0,4):
            #self.bsmog.append(cv2.BackgroundSubtractorMOG())
            self.bsmog.append(cv2.BackgroundSubtractorMOG(history,nGauss,bgThresh,noise))
            self.bgAdapt.append(Constants.BG_ADAPT)
        
        self.debug = debug
        
        self.debugWindow0 = "Debug Window 0"
        self.debugWindow1 = "Debug Window 1"
        self.debugWindow2 = "Debug Window 2"
        self.debugWindow3 = "Debug Window 3"
        self.debugWindow4 = "Debug Window 4"
        self.debugWindow5 = "Debug Window 5"
        
        if self.debug:
            cv2.namedWindow(self.debugWindow0)
            cv2.namedWindow(self.debugWindow1)
            cv2.namedWindow(self.debugWindow2)
            cv2.namedWindow(self.debugWindow3)
            cv2.namedWindow(self.debugWindow4)
            cv2.namedWindow(self.debugWindow5)
        
        result, self.currentFrame = self.capture.read()        
        self.currentFrame = cv2.flip(self.currentFrame, 1)
        self.previousState = []
        self.currentState = []
        for i in range(0,4):
            self.saveBackground(self.currentFrame, i)
            self.previousState.append(False)
            self.currentState.append(False)
        self.t = False
        
        
    def getFrameSize(self):
        return self.frameSize
    
    def adapt(self, matrix):
        for n in range(0,4):
            if matrix[n]:
                self.bgAdapt[n] = Constants.BG_ADAPT
            else:
                self.bgAdapt[n] = 0
    
    def saveBackground(self, frame, n):
        frame = cv2.cvtColor(frame, 6)   
        frame = cv2.GaussianBlur(frame,(7,7),0)
        if n == 0:
            self.background0 = frame[0:Constants.CAPTURE_REGION, 0:Constants.CAPTURE_REGION]
        if n == 1:
            self.background1 = frame[0:Constants.CAPTURE_REGION, Constants.SCREEN_WIDTH-Constants.CAPTURE_REGION:Constants.SCREEN_WIDTH]
        if n == 2:
            self.background2 = frame[Constants.SCREEN_HEIGHT-Constants.CAPTURE_REGION:Constants.SCREEN_HEIGHT, 0:Constants.CAPTURE_REGION]
        if n == 3:
            self.background3 = frame[Constants.SCREEN_HEIGHT-Constants.CAPTURE_REGION:Constants.SCREEN_HEIGHT, Constants.SCREEN_WIDTH-Constants.CAPTURE_REGION:Constants.SCREEN_WIDTH]
            
            
    def checkDifference(self, roi, n):
        roi = cv2.cvtColor(roi, 6)   
        roi = cv2.GaussianBlur(roi,(7,7),0)
        result = self.bsmog[n].apply(roi, None, self.bgAdapt[n])

            
        if self.debug:
            if n == 0:          
                cv2.imshow(self.debugWindow0, result)
            if n == 1:
                cv2.imshow(self.debugWindow1, result)
            if n == 2:
                cv2.imshow(self.debugWindow2, result)
            if n == 3:
                cv2.imshow(self.debugWindow3, result)

            
            
        number = cv2.countNonZero(result)
        
        if number > Constants.ACTIVE_THRESHOLD:
            return True
        return False
    
    def isActive(self, n):
        frame = self.currentFrame
        if n == 0:          
            return self.checkDifference(frame[0:Constants.CAPTURE_REGION, 0:Constants.CAPTURE_REGION],0)
        if n == 1:
            return self.checkDifference(frame[0:Constants.CAPTURE_REGION, Constants.SCREEN_WIDTH-Constants.CAPTURE_REGION:Constants.SCREEN_WIDTH],1)
        if n == 2:
            return self.checkDifference(frame[Constants.SCREEN_HEIGHT-Constants.CAPTURE_REGION:Constants.SCREEN_HEIGHT, 0:Constants.CAPTURE_REGION],2)
        if n == 3:
            return self.checkDifference(frame[Constants.SCREEN_HEIGHT-Constants.CAPTURE_REGION:Constants.SCREEN_HEIGHT, Constants.SCREEN_WIDTH-Constants.CAPTURE_REGION:Constants.SCREEN_WIDTH],3)
    
    def updateState(self):
        for n in range(0,4):
            self.previousState[n] = self.currentState[n]
            self.currentState[n] = self.isActive(n)
    
    def toggled(self, n):
        return self.currentState[n] and not self.previousState[n]
    
    def getCurrentFrame(self):
        return self.currentFrame
    
    def getCurrentFrameAsImage(self):
        im = numpy.array(self.currentFrame)
        im = cv.fromarray(im)
        cv.CvtColor(im, im, cv.CV_BGR2RGB)
        pgImg = pygame.image.frombuffer(im.tostring(), cv.GetSize(im), "RGB")
        return pgImg
    
    def run(self):
        result, self.currentFrame = self.capture.read()        
        self.currentFrame = cv2.flip(self.currentFrame, 1)
        self.updateState()
        cv2.waitKey(1)
            
    
    
    
