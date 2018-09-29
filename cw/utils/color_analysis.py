from numpy.matlib import repmat
import cv2
import matplotlib.pyplot as plt
import numpy as np
#
# Pass the path to an image to this script to visualize the dominant colors in
# the image. See the viz() method for additional options.
#

CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 1.0) # consider 1.0; may want lower?
FLAGS = cv2.KMEANS_RANDOM_CENTERS
K_MAX = 12
DEBUG = False

class ImageAnalyzer(object):
    def __init__(self, image_path):
        self.image_path = image_path
        self._image_data = None
        self._pixels = None
        self._cluster_data = []
        self._average_color = None

    @property
    def image_data(self):
        if self._image_data is None:
            self._image_data = cv2.imread(self.image_path)
        return self._image_data

    @property
    def pixels(self):
        if self._pixels is None:
            arr = np.float32(self.image_data) # a 3d ndarray
            self._pixels = arr.reshape((-1, 3))
        return self._pixels

    @property
    def average_color(self):
        # useless
        if self._average_color is None:
            self._average_color = [self.image_data[:, :, i].mean()
                                    for i in range(self.image_data.shape[-1])]
        return self._average_color

    @property
    def cluster_data(self):
        # TODO: Use multiprocessing!
        # https://www.linuxjournal.com/content/multiprocessing-python
        # runs through the image K_MAX times...can take a while!
        if not self._cluster_data:
            for k in range(1, K_MAX+1):
                compactness, labels, centroids = self._k_means(k)
                self._cluster_data.append((k, compactness, labels, centroids))
        return self._cluster_data

    def dominant_colors(self, n_colors=None):
        # See: https://docs.opencv.org/3.4.2/d1/d5c/tutorial_py_kmeans_opencv.html
        if n_colors is None:
            n_colors, _, labels, centroids = self._best_k_means_from_cluster_data()
        else:
            _, labels, centroids = self._k_means(n_colors)

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
        # return [(palette[f[0]].tolist(), int(f[1])) for f in freq_sorted]
        return [(palette[f[0]], f[1]) for f in freq_sorted]

    def viz(self, n_colors=None, height=100, width=400, weighted=True, debug=DEBUG):
        # See: https://stackoverflow.com/a/12890573/714478
        colors = self.dominant_colors(n_colors)
        image = np.zeros((height, width, 3), np.uint8)
        if weighted:
            pixels = ImageAnalyzer._viz_weighted(image, colors, width, debug)
        else:
            pixels = ImageAnalyzer._viz_unweighted(image, colors, width, debug)
        return pixels

    def dominant_colors_list(self, n_colors=None):
        return self._dominant_colors_list(n_colors=n_colors)

    def show_histogram(self):
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([self.image_data],[i],None,[256],[0,256])
            plt.plot(histr,color = col)
            plt.xlim([0,256])
        plt.show()

    def _best_k_means_from_cluster_data(self):
        best_k = self._find_best_k()
        return list(filter(lambda d: d[0] == best_k, self.cluster_data))[0]

    def show_elbow(self):
        ks = [e[0] for e in self.cluster_data]
        dist = [e[1] for e in self.cluster_data]
        plt.plot(ks, dist, 'bo-')
        plt.plot((ks[0], ks[-1]), (dist[0], dist[-1]), 'r--')
        best = self._best_k_means_from_cluster_data()
        plt.plot((best[0]), (best[1]), 'gx', markersize=12, mew=4)
        plt.xlabel('k')
        plt.ylabel('distortion')
        plt.title('elbow showing the optimal k')
        plt.show()

    def _dominant_colors_list(self, n_colors=None):
        colors = self.dominant_colors(n_colors=n_colors)
        total_pixels = sum([t[1] for t in colors])
        return [ImageAnalyzer._format_color_for_json(c, total_pixels) for c in colors]

    def _k_means(self, k):
        # returns (compactness, labels, centroids)
        return cv2.kmeans(self.pixels, k, None, CRITERIA, 10, FLAGS)

    def _find_best_k(self, debug=False):
        # kd_data is [(k, dist, ...), (k, dist, ...), ...]
        # See: https://en.wikipedia.org/wiki/Vector_projection
        # and: https://stackoverflow.com/a/37121355/714478
        dist_curve = [e[1] for e in self.cluster_data]
        n_points = len(self.cluster_data)
        all_coords = np.vstack((range(n_points), dist_curve)).T
        first_point = all_coords[0]
        line_vec = all_coords[-1] - first_point
        line_vec_norm = line_vec / np.sqrt(np.sum(line_vec**2))
        vec_from_first = all_coords - first_point
        scalar_prod = np.sum(vec_from_first * repmat(line_vec_norm, n_points, 1), axis=1)
        vec_from_first_parallel = np.outer(scalar_prod, line_vec_norm)
        vec_to_line = vec_from_first - vec_from_first_parallel
        dist_to_line = np.sqrt(np.sum(vec_to_line ** 2, axis=1))
        index_of_best_point = np.argmax(dist_to_line)
        best_k = self.cluster_data[index_of_best_point][0]
        if debug:
            print(f'Distortion curve: {dist_curve}')
            print(f'All coords: {all_coords}')
            print(f'First point: {first_point}')
            print(f'Line vector: {line_vec}')
            print(f'Line vector normalized: {line_vec_norm}')
            print(f'Vector from first: {vec_from_first}')
            print(f'Scalar product: {scalar_prod}')
            print(f'Vector from first parallel: {vec_from_first_parallel}')
            print(f'Vector to line: {vec_to_line}')
            print(f'Distance to line: {dist_to_line}')
            print(f'Index of best K: {index_of_best_point}')
            print(f'Best K: {best_k}')
        return best_k

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
    def _viz_weighted(image, colors, width, debug=DEBUG):
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
    def _viz_unweighted(image, colors, width, debug=DEBUG):
        section_width = 1/len(colors)
        for i in range(len(colors)):
            offset = int(i*section_width*width)
            if debug:
                print(f'BGR: {colors[i][0]}, Offset: {offset}')
            image[:, offset:width] = colors[i][0]
        return image

if __name__ == '__main__':
#     from cv2 import imwrite
    image_path = '/Users/jstroop/workspace/colorweight/samples/01_in.jpg'
    ia = ImageAnalyzer(image_path)
    # Best K elbow graph:
    ia.show_elbow()
#     # Dominant Color Image:
#     # imwrite('/tmp/out.png', ia.viz())
#     # List structure for JSON:
#     # print(ia.list())
#     # Histogram:
#     ia.show_histogram()
