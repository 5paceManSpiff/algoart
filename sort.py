import numpy as np
import cv2
import math
import colorsys
import sys

def show(name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)

def tohsl(data):
    return colorsys.rgb_to_hls(data[2], data[1], data[0])

level = float(sys.argv[2])

imgname = sys.argv[1]
img = cv2.imread('in/' + imgname, -1)

for y in range(img.shape[0]):
    print('{0:.0%}'.format(float(y)/img.shape[0]) + ' complete')
    for x in range(img.shape[1]):
        if y != 0:
            if tohsl(img[y, x])[1] - tohsl(img[y-1, x])[1] > level:
                img[y, x] = img[y-1, x]

show('firstpass')
print 'level : ' + str(level)
print 'file : ' + imgname

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('out/' + imgname ,img)
    cv2.destroyAllWindows()
