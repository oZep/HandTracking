import cv2
import mediapipe as mp
import time
import math
import HandTrackingModule as htm

# sort my closeness to next landmark
# key: 0 value: closest to zero
# POI - points of interest
HAND_SIGNS = {
    'a': [{'POI': [2,8,5,4,6,10,9,13,15,18,17,19,20], 'ORT': 0}, {'0': 1, '1': 0, '2': 8, '8': 2, '3': 4, '4': 3, '5': 7, '7': 5, '6': 10, '10': 6, '9': 11, '11': 9, '12': 16, '16': 12, '13': 15, '15': 13, '14': 18, '18': 14, '17': 19, '19': 17, '20': -1, '-1': 20}],
    'b': [{'POI': [4,13,7,6,8,11,10,14,12,16,15,20,17,18,19,-1], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 13, '13': 4, '5': 9, '9': 5, '6': 7, '7': 6, '8': 11, '11': 8, '10': 14, '14': 10, '12': 16, '16': 12, '15': 20, '20': 15, '17': 18, '18': 17, '19': -1, '-1': 19}],
    'c': [{'POI': [4,8,12,16,20,17,13,18,-1], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 12, '12': 4, '5': 9, '9': 5, '6': 19, '19': 6, '7': 20, '20': 7, '8': 16, '16': 8, '10': 14, '14': 10, '11': 15, '15': 11, '13': 17, '17': 13, '18': -1, '-1': 18}],
    'd': [{'POI': [4,12,5,9,7,6,10,8,11,15,19,13,18,14,20,17,-1], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 12, '12': 4, '5': 9, '9': 5, '6': 7, '7': 6, '8': 10, '10': 8, '11': 15, '15': 11, '13': 19, '19': 13, '14': 18, '18': 14, '16': 20, '20': 16, '17': -1, '-1': 17}],
    'e': [{'POI': [0,1,2,3,4,16,5,8,6,7,9], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 16, '16': 4, '5': 8, '8': 5, '6': 7, '7': 6, '9': 12, '12': 9, '10': 14, '14': 10, '11': 15, '15': 11, '13': 20, '20': 13, '17': 19, '19': 17, '18': -1, '-1': 18}],
    'f': [{'POI': [0,1,2,3,4,7,5,8,6,10,9,13,11,12,14,19,15,20,16,18,-1], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 8, '8': 4, '5': 9, '9': 5, '6': 7, '7': 6, '10': 14, '14': 10, '11': 12, '12': 11, '13': 17, '17': 13, '15': 20, '20': 15, '16': 19, '19': 16, '18': -1, '-1': 18}],
    'g': [{'POI': [0,16,1,12,2,3,4,5,6,7,8,9,10,14,11,15,13,18,17,19,-1], 'ORT': 0}, {'0': 16, '16': 0, '1': 12, '12': 1, '2': 3, '3': 2, '4': 5, '5': 4, '6': 7, '7': 6, '8': 9, '9': 8, '10': 14, '14': 10, '11': 15, '15': 11, '13': 18, '18': 13, '17': 19, '19': 17, '20': -1, '-1': 20}],
    'h': [{'POI': [0,1,2,3,4,9,5,6,7,8,20,16], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 9, '9': 4, '5': 6, '6': 5, '7': 8, '8': 7, '10': 11, '11': 10, '12': 14, '14': 12, '13': 15, '15': 13, '16': 20, '20': 16, '17': 19, '19': 17, '18': -1, '-1': 18}],
    'i': [{'POI': [1,2,3,5,7,9,11,13,15,17,19,20,-1], 'ORT': 0}, {'0': 1, '1': 0, '2': 8, '8': 2, '3': 5, '5': 3, '4': 9, '9': 4, '6': 10, '10': 6, '7': 12, '12': 7, '11': 15, '15': 11, '13': 17, '17': 13, '14': 18, '18': 14, '16': 19, '19': 16, '20': -1, '-1': 20}],
    'j': [{'POI': [1,2,3,5,7,9,11,13,15,17,19,20], 'ORT': 1}, {'0': 15, '15': 0, '1': 4, '4': 1, '2': 3, '3': 2, '5': 9, '9': 5, '6': 7, '7': 6, '8': 12, '12': 8, '10': 14, '14': 10, '11': 16, '16': 11, '13': 17, '17': 13, '18': 19, '19': 18, '20': -1, '-1': 20}],
    'k': [{'POI': [1,3,5,7,9,11,15,17,19,20,-1], 'ORT': 0}, {'0': 1, '1': 0, '2': 5, '5': 2, '3': 9, '9': 3, '4': 14, '14': 4, '6': 7, '7': 6, '8': 11, '11': 8, '10': 12, '12': 10, '13': 15, '15': 13, '16': 20, '20': 16, '17': 19, '19': 17, '18': -1, '-1': 18}],
    'l': [{'POI': [1,3,5,7,9,11,13,15,17,19,20,-1], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 5, '5': 4, '6': 7, '7': 6, '8': 10, '10': 8, '9': 11, '11': 9, '12': 16, '16': 12, '13': 14, '14': 13, '15': 20, '20': 15, '17': 19, '19': 17, '18': -1, '-1': 18}],
    'm': [{'POI': [0,20,1,2,3,15,4,9,5,11,6,10,7,8,12,16,13,14,17,19.-1], 'ORT': 0}, {'0': 20, '20': 0, '1': 2, '2': 1, '3': 15, '15': 3, '4': 9, '9': 4, '5': 11, '11': 5, '6': 10, '10': 6, '7': 8, '8': 7, '12': 16, '16': 12, '13': 18, '18': 13, '14': 17, '17': 14, '19': -1, '-1': 19}],
    'n': [{'POI': [0,1,2,3,4,5,6,7,8,9,10,12,15,13,14,15,16,17,18,19,20,-1], 'ORT': 0}, {'0': 1, '1': 0, '2': 8, '8': 2, '3': 5, '5': 3, '4': 10, '10': 4, '6': 7, '7': 6, '9': 11, '11': 9, '12': 15, '15': 12, '13': 19, '19': 13, '14': 18, '18': 14, '16': 20, '20': 16, '17': -1, '-1': 17}],
    'o': [{'POI': [14,15,16,17,18,19,20], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 8, '8': 4, '5': 9, '9': 5, '6': 19, '19': 6, '7': 12, '12': 7, '10': 14, '14': 10, '11': 15, '15': 11, '13': 17, '17': 13, '16': 20, '20': 16, '18': -1, '-1': 18}],
    'p': [{'POI': [14,16,17,18,19,20,-1,0,2,4,18,9,5,7,8], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 16, '16': 4, '5': 9, '9': 5, '6': 14, '14': 6, '7': 8, '8': 7, '10': 18, '18': 10, '11': 15, '15': 11, '12': 20, '20': 12, '13': 17, '17': 13, '19': -1, '-1': 19}],
    'q': [{'POI': [10,11,14,15,16,18,19,20,-1], 'ORT': 0}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 11, '11': 4, '5': 20, '20': 5, '6': 10, '10': 6, '7': 8, '8': 7, '9': 13, '13': 9, '12': 15, '15': 12, '14': 18, '18': 14, '16': 19, '19': 16, '17': -1, '-1': 17}],
    'r': [{'POI': [0,1,2,3,4,5,6,7,8,9,10,12,15,13,14,15,16,17,18,19,20,-1]}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 14, '14': 4, '5': 9, '9': 5, '6': 10, '10': 6, '7': 11, '11': 7, '8': 12, '12': 8, '13': 18, '18': 13, '15': 16, '16': 15, '17': 19, '19': 17, '20': -1, '-1': 20}],
    's': [{'POI': [4,8,12,16,20,0,10]}, {'0': 1, '1': 0, '2': 8, '8': 2, '3': 7, '7': 3, '4': 10, '10': 4, '5': 11, '11': 5, '6': 9, '9': 6, '12': 15, '15': 12, '13': 18, '18': 13, '14': 17, '17': 14, '16': 19, '19': 16, '20': -1, '-1': 20}],
    't': [{'POI': [4,8,12,16,20,0,10]}, {'0': 1, '1': 0, '2': 8, '8': 2, '3': 5, '5': 3, '4': 10, '10': 4, '6': 7, '7': 6, '9': 11, '11': 9, '12': 15, '15': 12, '13': 18, '18': 13, '14': 19, '19': 14, '16': 20, '20': 16, '17': -1, '-1': 17}],
    'u': [{'POI': [0,1,2,3,4,5,6,7,8,9,10,12,15,13,14,15,16,17,18,19,20,-1]}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 15, '15': 4, '5': 9, '9': 5, '6': 7, '7': 6, '8': 11, '11': 8, '10': 14, '14': 10, '12': 13, '13': 12, '16': 19, '19': 16, '17': 18, '18': 17, '20': -1, '-1': 20}],
    'v': [{'POI': [0,1,2,3,4,5,6,7,8,9,10,12,15,13,14,15,16,17,18,19,20,-1]}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 9, '9': 4, '5': 15, '15': 5, '6': 7, '7': 6, '8': 11, '11': 8, '10': 14, '14': 10, '12': 13, '13': 12, '16': 19, '19': 16, '17': 18, '18': 17, '20': -1, '-1': 20}],
    'w': [{'POI': [0,1,2,3,4,5,6,7,8,9,10,12,15,13,14,15,16,17,18,19,20,-1]}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 13, '13': 4, '5': 9, '9': 5, '6': 7, '7': 6, '8': 12, '12': 8, '10': 11, '11': 10, '14': 15, '15': 14, '16': 18, '18': 16, '17': 19, '19': 17, '20': -1, '-1': 20}],
    'x': [{'POI': [0,1,2,3,4,5,6,7,8,9,10,12,15,13,14,15,16,17,18,19,20,-1]}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 5, '5': 4, '6': 7, '7': 6, '8': 10, '10': 8, '9': 11, '11': 9, '12': 16, '16': 12, '13': 14, '14': 13, '15': 20, '20': 15, '17': 18, '18': 17, '19': -1, '-1': 19}],
    'z': [{'POI': [0,1,2,3,4,5,6,7,8,9,10,12,15,13,14,15,16,17,18,19,20,-1]}, {'0': 1, '1': 0, '2': 3, '3': 2, '4': 5, '5': 4, '6': 10, '10': 6, '7': 8, '8': 7, '9': 11, '11': 9, '12': 16, '16': 12, '13': 15, '15': 13, '14': 18, '18': 14, '17': 19, '19': 17, '20': -1, '-1': 20}]
    }

# what do i quantify as being close
class ASLDecoder:
    def __init__(self, numHands=2):
        '''
        :param numHands: int
        '''
        self.numHands = numHands

    def distanceBetween(self, p1, p2):
        '''
        :param p1: List of pos
        :param p2: List of pos
        :return: distance
        '''
        dx = math.pow(p1[0] - p2[0], 2)
        dy = math.pow(p1[1] -p2[1], 2)
        dis = math.sqrt(dx + dy)
        return dis

    def findNextLandmark(self, landmarks):
        '''
        :param landmarks: List of all landmarks
        :return: an ordered dic with the value: landmark, key: closest neighbor
        '''
        distanceMap = {} # to optamize


        # given a matrix with [landmark id, cx, cy]
        for i in (range(len(landmarks))):
            if str(i) not in distanceMap.keys():
                minDis = 10000  # impossible to get
                key = -1
                for j in (range(len(landmarks))):
                    if i != j and str(j) not in distanceMap.keys():  # if already located then shortest pair found
                        dis = self.distanceBetween(landmarks[i][1:], landmarks[j][1:])
                        if dis < minDis:
                            minDis = dis
                            key = j
                distanceMap[str(i)] = key # add the location of it's miminum landmark to the dictionary
                distanceMap[str(key)] = i

        # max complexity: O(q*p) where q = 21 and p = 21, 441 passes
        # will optamized to take half as less passes through skipping previously mapped characters
        return distanceMap

    def getSign(self, landmarks):
        ORT = 0
        if len(landmarks) == 20:
            if landmarks[20][2] > landmarks[12][2]:
                ORT = 0
            else:
                ORT = 1
        closestLandmark = self.findNextLandmark(landmarks)
        for option, key in enumerate(list(HAND_SIGNS.keys())):
            check = len(HAND_SIGNS[key][0]['POI'])
            cashed = 0
            for POI in HAND_SIGNS[key][0]['POI']: # compare points of interest
                if closestLandmark.get(str(POI)) == HAND_SIGNS[key][1].get(str(POI)):
                    cashed += 1
            if cashed == check and HAND_SIGNS[key][0]['ORT'] == ORT:
                return key

        # -- testing decoder
        #return -1
        # -- finding landmarks
        return closestLandmark
