from cv2 import imwrite
from os import listdir
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import realpath
from sys import path

# This is necessary so that we can execute this file AND use it as a module.
# Importing relative to this directory as opposed to ../cw feels wrong)
path.append(abspath(dirname(dirname(realpath(__file__)))))

from cw.models import Image
from cw.models import ImageSet
from cw.utils.color_analysis import ImageAnalyzer

set = ImageSet([])
dir = '/Users/jstroop/workspace/colorweight/images/ga'
image_list = sorted(filter(lambda p: p.endswith('.jpg'), listdir(dir)))
data_path = join(dir, 'data.json')

for im in image_list:
    set = ImageSet.from_file(data_path)
    print(im)
    image_path = join(dir, im)
    palette_image_path = join(dir, im.replace('.jpg', '.png'))
    ia = ImageAnalyzer(image_path)
    colors = ia.dominant_colors_list()
    imwrite(palette_image_path, ia.viz())
    image = Image(colors, palette_image_path, image_path)
    set.append(image)
    set.save(data_path)
