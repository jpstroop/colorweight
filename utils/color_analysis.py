
from scipy.stats import itemfreq
import cv2
import matplotlib.pyplot as plt
import numpy

class ImageAnalyzer(object):
    def __init__(self, image_path):
        self.image_path = image_path
        self._image_data = None
        self._average_color = None

    @property
    def image_data(self):
        if self._image_data is None:
            self._image_data = cv2.imread(self.image_path)
        return self._image_data

    @property
    def average_color(self):
        if self._average_color is None:
            self._average_color = [self.image_data[:, :, i].mean()
                                    for i in range(self.image_data.shape[-1])]
        return self._average_color

    def dominant_colors(self, n_colors=5):
        # See: https://stackoverflow.com/a/43111221/714478
        pixels = numpy.float32(self.image_data).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        palette = numpy.uint8(centroids) # This might be all we need
        # quantized = palette[labels.flatten()].reshape(self.image_data.shape)
        # return palette[numpy.argmax(itemfreq(labels)[:, -1])]
        return palette

        # return palette
        # TODO: above doesn't seem to be working quite right

    def viz(self, n_colors=5, height=100, width=200):
        # See: https://stackoverflow.com/a/12890573/714478
        colors = self.dominant_colors(n_colors)
        image = numpy.zeros((height, width, 3), numpy.uint8)
        d = 1/len(colors)
        for i in range(len(colors)):
            print(str(int(i*d*width)) + " : " + str(colors[i]))
            image[:, int(i*d*width):width] = colors[i]
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# TODO: should be a param arg
IMAGE_PATH = '/Users/jstroop/workspace/colorfun/images/0093.jpg'
if __name__ == '__main__':
    analyzer = ImageAnalyzer(IMAGE_PATH)
    analyzer.viz(10, 200, 500)
