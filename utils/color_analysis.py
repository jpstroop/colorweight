import cv2
import matplotlib.pyplot as plt
import numpy as np

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
        arr = np.float32(self.image_data) # a 3d ndarray
        pixels = arr.reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)

        # https://docs.opencv.org/3.4.2/d1/d5c/tutorial_py_kmeans_opencv.html
        # "Labels will have the same size as that of test data where each data
        # will be labelled as '0','1','2' etc. depending on their centroids."
        # "labels" are indicies of centroids, and in our case the centroids
        # are colors expressed as [B,G,R].

        # How often does each unique label occur?
        #    returns (array(labels), array(frequency))
        label_freq = np.unique(labels, return_counts=True)

        # Zip the two arrays above into a list: [(label, freq),]
        label_freq_pairs = zip(label_freq[0], label_freq[1])

        # Sort the pairs by frequency, descending
        freq_sorted = sorted(label_freq_pairs, key=lambda t: t[1], reverse=True)

        # Convert the members of the centroids to ints
        palette = np.uint8(centroids)

        # Replace the labels with the value from the palette/centroids
        # giving us: [([B,G,R], freq), ([B,G,R], freq), ...]
        pallet_by_freq = [(palette[f[0]], f[1]) for f in freq_sorted]

        return pallet_by_freq

        # WORKS-ish###################
        # pixels = np.float32(self.image_data).reshape((-1, 3))
        # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        # flags = cv2.KMEANS_RANDOM_CENTERS
        # _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        # palette = np.uint8(centroids) # This might be all we need
        # # quantized = palette[labels.flatten()].reshape(self.image_data.shape)
        # # return palette[np.argmax(itemfreq(labels)[:, -1])]
        # return palette
        ################################

        # return palette
        # TODO: above doesn't seem to be working quite right

    def viz(self, n_colors=5, height=100, width=200):
        # See: https://stackoverflow.com/a/12890573/714478
        colors = self.dominant_colors(n_colors)
        image = np.zeros((height, width, 3), np.uint8)
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
    print(analyzer.dominant_colors())
