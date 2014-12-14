import numpy as np
import cv2
import math
import colorsys
import sys
import copy
import os
import glob

frames = []

def show(name, img):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)

def tohsl(data):
    return colorsys.rgb_to_hls(data[2], data[1], data[0])

def checkdown(img, y, x):
    if abs(tohsl(img[y, x])[2] - tohsl(img[y-1, x])[2]) < level:
        return True
    return False

def checkright(img, y, x):
    if abs(tohsl(img[y, x])[2] - tohsl(img[y, x-1])[2]) < level:
        return True
    return False

def down(img):
    for y in range(img.shape[0]):
        frames.append(copy.deepcopy(img))
        for x in range(img.shape[1]):
            if y != 0:
                if checkdown(img, y, x):
                    img[y, x] = img[y-1, x]

        print('{0:.0%}'.format(float(y)/img.shape[0]) + ' complete')
    print 'done with down pass'

def right(img):
    for x in range(img.shape[1]):
        frames.append(copy.deepcopy(img))
        for y in range(img.shape[0]):
            if x != 0:
                if checkright(img, y, x):
                    img[y, x] = img[y, x-1]

        print('{0:.0%}'.format(float(x)/img.shape[1]) + ' complete')
    print 'done with right pass'

level = float(sys.argv[2])
imgname = sys.argv[1]
img = cv2.imread('in/' + imgname, -1)
right(img)
down(img)
right(img)
down(img)

files = glob.glob('out/*')
for file in files:
    os.remove(file)

for i in range(len(frames)):
    cv2.imwrite('out/%d.jpg' % (i), frames[i])
    print 'writing frame ' + str(i) + ' of ' + str(len(frames))

print 'level : ' + str(level)
print 'file : ' + imgname
