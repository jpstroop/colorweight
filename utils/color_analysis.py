import cv2
import numpy as np
from json import dumps

#
# Pass the path to an image to this script to visualize the dominant colors in
# the image. See the viz() method for additional options.
#
DEFAULT_N_COLORS = 5

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

    def dominant_colors(self, n_colors=DEFAULT_N_COLORS):
        # See: https://docs.opencv.org/3.4.2/d1/d5c/tutorial_py_kmeans_opencv.html
        arr = np.float32(self.image_data) # a 3d ndarray
        pixels = arr.reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)

        # "Labels will have the same size as that of test data where each data
        # will be labelled as '0','1','2' etc. depending on their centroids."
        # i.e. "labels" are indicies of centroids, and in our case the centroids
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
        return [(palette[f[0]], f[1]) for f in freq_sorted]

    def viz(self, n_colors=DEFAULT_N_COLORS, height=100, width=400, weighted=True, debug=False):
        # See: https://stackoverflow.com/a/12890573/714478
        colors = self.dominant_colors(n_colors)
        image = np.zeros((height, width, 3), np.uint8)
        if weighted:
            pixels = ImageAnalyzer._viz_weighted(image, colors, width, debug)
        else:
            pixels = ImageAnalyzer._viz_unweighted(image, colors, width, debug)
        return pixels

    def list(self, n_colors=DEFAULT_N_COLORS):
        return self._dominant_colors_list(n_colors=n_colors)

    def _dominant_colors_list(self, n_colors=DEFAULT_N_COLORS):
        colors = self.dominant_colors(n_colors=n_colors)
        total_pixels = sum([t[1] for t in colors])
        return [ImageAnalyzer._format_color_for_json(c, total_pixels) for c in colors]

    @staticmethod
    def _format_color_for_json(color_entry, total_pixels):
        b, g, r = color_entry[0]
        rgb = list(map(int, [r, g, b])) # reformatted the way most would want
        # Note that the volume is relative to the number of colors requested,
        # and not the total number of colors in the image
        relative_volume = color_entry[1] / total_pixels
        return { 'rgb' : rgb, 'relative_volume' : float(relative_volume) }

    @staticmethod
    def _show(image, label='[Image]'):
        cv2.imshow(label, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def _viz_weighted(image, colors, width, debug=False):
        total_pixels = sum([t[1] for t in colors])
        offset = 0
        for i in range(len(colors)):
            if i == len(colors)-1:
                # Hack because we can be off (by 1, more?) in the last pass
                # because fractions and pixels...
                section_width = width - offset
            else:
                section_width = int(colors[i][1] / total_pixels * width)
            if debug:
                print(f'BGR: {colors[i][0]}, Offset: {section_width}, Section Width: {offest}')
            image[:, offset:width] = colors[i][0]
            offset = offset + section_width
        return image

    @staticmethod
    def _viz_unweighted(image, colors, width, debug=False):
        section_width = 1/len(colors)
        for i in range(len(colors)):
            offset = int(i*section_width*width)
            if debug:
                print(f'BGR: {colors[i][0]}, Offset: {offset}')
            image[:, offset:width] = colors[i][0]
        return image

if __name__ == '__main__':
    # TODO: Cheap CLI, will do more later.
    from os.path import dirname
    from os.path import join
    from os.path import realpath
    from sys import argv
    try:
        image_path = argv[1]
    except IndexError:
        image_path = realpath(join(dirname(realpath(__file__)), '../samples/01_in.jpg'))
    analyzer = ImageAnalyzer(image_path)
    analyzer.json()
