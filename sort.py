import numpy as np
import cv2
import math
import colorsys
import sys
import copy
import os
import shutil
from PIL import Image

def show(name, img):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)

def tohsl(data):
    return colorsys.rgb_to_hls(data[2], data[1], data[0])

def checkdown(img, y, x, level):
    if abs(tohsl(img[y, x])[2] - tohsl(img[y-1, x])[2]) < level:
        return True
    return False

def checkright(img, y, x, level):
    if abs(tohsl(img[y, x])[2] - tohsl(img[y, x-1])[2]) < level:
        return True
    return False

def down(img, frames, level):
    for y in range(img.shape[0]):
        frames.append(copy.deepcopy(img))
        for x in range(img.shape[1]):
            if y != 0:
                if checkdown(img, y, x, level):
                    img[y, x] = img[y-1, x]

        print('{0:.0%}'.format(float(y)/img.shape[0]) + ' complete')
    print 'done with down pass'

def right(img, frames, level):
    for x in range(img.shape[1]):
        frames.append(copy.deepcopy(img))
        for y in range(img.shape[0]):
            if x != 0:
                if checkright(img, y, x, level):
                    img[y, x] = img[y, x-1]

        print('{0:.0%}'.format(float(x)/img.shape[1]) + ' complete')
    print 'done with right pass'

def sort(imgname, output):
    frames = []
    level = float(sys.argv[3])
    img = cv2.imread(imgname, -1)
    right(img, frames, level)

    shutil.rmtree('out')
    os.mkdir('out')

    os.mkdir('out/' + output)
    for i in range(len(frames)):
        cv2.imwrite('out/%s/%d.jpg' % (output, i), frames[i])
        print 'writing frame ' + str(i) + ' of ' + str(len(frames))

    vidlength = 5
    outrate = 30
    inrate = len(frames)/vidlength
    os.system('ffmpeg -framerate %d -i out/%s/%%d.jpg -c:v libx264 -r %d -pix_fmt yuv420p out/%s.mp4' % (inrate, output, outrate, output))
    os.system('ffmpeg -i out/%s.mp4 -vcodec libvpx -acodec libvorbis out/%s.webm' % (output, output))
    os.remove('out/%s.mp4' % output)
    return len(frames)

def concatenate(paths):
    images = map(Image.open, paths)
    w = sum(i.size[0] for i in images)
    mh = max(i.size[1] for i in images)

    result = Image.new("RGBA", (w, mh))

    x = 0
    for i in images:
        result.paste(i, (x, 0))
        x += i.size[0]

    return result

result = concatenate([sys.argv[1], sys.argv[2]])
result.save('out/two.jpg')
sort('out/two.jpg', 'two')
