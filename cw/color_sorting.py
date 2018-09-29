from colorsys import rgb_to_hsv
from math import sqrt
from random import random
import cv2
import numpy as np

def viz(colors_rgb, width=1200, height=200):
    image = np.zeros((height, width, 3), np.uint8)
    section_width = 1/len(colors_rgb)
    for i,color_rgb in enumerate(colors_rgb):
        offset = int(i*section_width*width)
        # Remember that in cv2 colors are B G R
        image[:, offset:width] = [int(255.0*c) for c in reversed(color_rgb)]
    cv2.imshow('[Image]: Close with "0"', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def lum(r,g,b):
    return sqrt(.241 * r + .691 * g + .068 * b)

def step(r,g,b, repetitions=1, alternate=False):
    l = lum(r,g,b) #lum
    h,s,v = rgb_to_hsv(r,g,b)
    h2 = int(h * repetitions)
    lum2 = int(l * repetitions)
    v2 = int(v * repetitions)
    if alternate:
        if h2 % 2 == 1: # invert the luminosity of every other segment for smoothness
            v2 = repetitions - v2
            l = repetitions - l
    return (h2, l, v2)

def color_float_to_int(rgb):
    return tuple(int(255.0*c) for c in rgb)

def color_int_to_float(rgb):
    return tuple(c / 255.0 for c in rgb)


if __name__ == '__main__':
    # colors = [[random() for _ in range(3)] for _ in range(1200)]

    from models import ImageSet
    image_set = ImageSet.from_file('/Users/jstroop/workspace/colorweight/images/ga/data.json')
    colors = [color_int_to_float(rgb) for rgb in [i.colors[0].rgb for i in image_set]]

    print(colors)
    # viz(sorted(colors))


    # in colorsys colors are floats between 0-1 (not 0-255)

    # in colorsys colors are floats between 0-1 (not 0-255)
    # lum_sorted = sorted(colors, key=lambda rgb: lum(*rgb))
    # viz(lum_sorted)

    step_sorted = sorted(colors, key=lambda rgb: step(*rgb,8))
    viz(step_sorted)
