import cv2 as cv
import numpy as np
import math
import random
import time
import tkinter as tk



def compare_by_angles(center, point, point1, point2):
    if getAngle(center, point) >= getAngle(center, point1) and getAngle(center, point) <= getAngle(center, point2):
        return True
    return False


def getAngle(center, point):
    angle = math.degrees(math.atan2(point[1] - center[1], point[0] - center[0]))
    if angle < 0:
        return 360 + angle
    return angle


def sortInCircularOrder(points, center):
    t = []
    l = points
    if getAngle((center[0], center[1]), l[1]) > getAngle((center[0], center[1]), l[0]):
        t.append(l[0])
        t.append(l[1])
    else:
        t.append(l[1])
        t.append(l[0])
    for pt in l[2:]:
        if getAngle(center, pt) <= getAngle(center, t[0]):
            t.insert(0, pt)
        elif getAngle(center, pt) >= getAngle(center, t[len(t) - 1]):
            t.append(pt)
        else:
            for (p, q) in zip(t, t[1::]):
                if compare_by_angles(center, pt, p, q):
                    t.insert(t.index(p) + 1, pt)
                    break
    return t


def getCircularPoints(greyImage, radius):
    height, width = greyImage.shape[:2]

    xc = width // 2
    yc = height // 2

    center = (xc, yc)

    mask = np.zeros_like(greyImage)
    cv.circle(mask, center, radius, (255, 255, 255), -1)

    cv.imshow('mask', mask)

    circularGreyImage = cv.bitwise_and(greyImage, mask)

    cv.imshow('circularGreyImage', circularGreyImage)

    circle = np.zeros_like(greyImage)
    cv.circle(circle, center, radius, (255, 255, 255), 1)

    cv.imshow('circle', circle)

    whitePixels = np.where(circle == 255)

    unOrderedCircularPoints = [[x, y] for (x, y) in zip(whitePixels[0], whitePixels[1])]

    print(len(unOrderedCircularPoints))

    orderedCircularPoints = sortInCircularOrder(unOrderedCircularPoints, center)

    print(len(orderedCircularPoints))

    return orderedCircularPoints


def getPoints(black):
    p = []
    linepoints = np.where(black == 255)
    for (px, py) in zip(linepoints[0], linepoints[1]):
        p.append([px, py])

    return p


def writeChordPointsToFile(orderedCircularPoints, black, file):
    with open(file, 'w') as filehandle:
        for init in orderedCircularPoints:
            for term in orderedCircularPoints:
                if init == term:
                    continue
                cv.line(black, (init[1], init[0]), (term[1], term[0]), (255, 255, 255), 1)
                filehandle.write('%s\n' % getPoints(black))
                cv.line(black, (init[1], init[0]), (term[1], term[0]), (0, 0, 0), 1)


def readChordPointsFromFile(file):
    chords = []
    pattern = re.compile(r'\[\d+\, \d+\]')
    with open(file, 'r') as filehandle:
        for line in filehandle:
            l = pattern.findall(line)
            t = [x.strip('][').split(',') for x in l]
            j = [[int(p[0]), int(p[1])] for p in t]
            chords.append(j)
    return chords


def selectRandomPoint(unOrderedCircularPoints):
    rand = random.randrange(len(unOrderedCircularPoints))
    return unOrderedCircularPoints[rand], rand


def getwhite(black, invertedGreyImage):
    sum = 0
    linePoints = np.where(black == 255)
    s = [invertedGreyImage[x, y] for (x, y) in zip(linePoints[0], linePoints[1])]
    for m in s:
        sum = sum + m
    return sum // len(linePoints[0])


def maxValue(point, init, black, invertedGreyImage):
    cv.line(black, (init[1], init[0]), (point[1], point[0]), (255, 255, 255), 1)
    average = getwhite(black, invertedGreyImage)
    cv.line(black, (init[1], init[0]), (point[1], point[0]), (0, 0, 0), 1)
    return average


def Half(HalfPoints, init, invertedGreyImage):
    black = np.zeros_like(invertedGreyImage)
    p = [maxValue(point, init, black, invertedGreyImage) if init != point else 0 for point in HalfPoints]
    return HalfPoints[p.index(max(p))]


if __name__ == "__main__":

    imagePath = "C:/Users/Arpitha/Downloads/pic.jpg"
    greyImage = cv.imread(imagePath, 0)
    cv.imshow('greyImage0', greyImage)
    greyImage = cv.resize(greyImage, (0, 0), fx=0.5, fy=0.5)
    cv.imshow('greyImage', greyImage)
    invertedGreyImage = cv.bitwise_not(greyImage)
    cv.imshow('invertedGrey', invertedGreyImage)
    height, width = greyImage.shape[:2]
    black = np.zeros_like(invertedGreyImage)
    string = np.zeros_like(invertedGreyImage)
    string.fill(255)

    radius = min(height, width) // 2 - 3
    xc = width // 2
    yc = height // 2
    center = (xc, yc)

    orderedPoints = getCircularPoints(greyImage, radius)
    total=len(orderedPoints)

    orderedCircularPoints = orderedPoints[::5]
    circularPoints = orderedPoints[::5]
    

    lenn = len(orderedCircularPoints)
    print(lenn)

    #    writeChordPointsToFile(orderedCircularPoints,black,'lines.txt')


    i = 0

    while (1):
        if i == 312:
            break
        print(i)
        i = i + 1
        if len(circularPoints) == 0:
            circularPoints = orderedCircularPoints[::]
        init, index = selectRandomPoint(circularPoints)
       
        end = Half(orderedCircularPoints, init, invertedGreyImage)
        cv.line(invertedGreyImage, (init[1], init[0]), (end[1], end[0]), (0, 0, 0), 1)
        cv.line(string, (init[1], init[0]), (end[1], end[0]), (30, 30, 30), 1)
        circularPoints.remove(init)

    invertedGreyImage = cv.resize(invertedGreyImage, (0, 0), fx=1, fy=1)
    string = cv.resize(string, (0, 0), fx=1, fy=1)
    cv.imshow('invertedGreyImage', invertedGreyImage)
    cv.imshow('stringArt', string)
    

