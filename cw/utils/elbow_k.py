# https://pythonprogramminglanguage.com/kmeans-elbow-method/
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html

import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.matlib import repmat

image_path = '/Users/jstroop/workspace/colorweight/samples/01_in.jpg'

CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 1.0) # consider 1.0; may want lower?
FLAGS = cv2.KMEANS_RANDOM_CENTERS

K_MAX = 16 # higher (16?) for real use

image_data = cv2.imread(image_path)
arr = np.float32(image_data) # a 3d ndarray
pixels = arr.reshape((-1, 3))

def gen_data():
    data = []
    for k in range(1, K_MAX+1):
        compactness, labels, centroids = cv2.kmeans(pixels, k, None, CRITERIA, 10, FLAGS)
        data.append((k, compactness))
    return data

def show_elbow(kd_data):
    ks = [e[0] for e in kd_data]
    dist = [e[1] for e in kd_data]
    plt.plot(ks, dist, 'bo-')
    plt.plot((ks[0], ks[-1]), (dist[0], dist[-1]), 'r--')
    best = find_best_k(kd_data)
    plt.plot((best[0]), (best[1]), 'gx', markersize=12, mew=4)
    plt.xlabel('k')
    plt.ylabel('distortion')
    plt.title('elbow showing the optimal k')
    plt.show()

def find_best_k(kd_data, debug=False):
    # kd_data is [(k, dist), (k, dist), ...]
    # See: https://en.wikipedia.org/wiki/Vector_projection
    # and: https://stackoverflow.com/a/37121355/714478
    dist_curve = [e[1] for e in kd_data]
    n_points = len(dist_curve) # TODO: use Ks instead
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
    return kd_data[index_of_best_point]

kd_data = [
    (1, 5367333014.24297),
    (2, 2426019016.0840645),
    (3, 1414663818.9231436),
    (4, 887659077.4440181),
    (5, 653222613.6217169),
    (6, 544465899.0054665),
    (7, 449343973.6645793),
    (8, 375759862.3675634),
    (9, 326419459.7951351),
    (10, 295985194.268401),
    (11, 273129710.4291423),
    (12, 250031524.84741667),
    (13, 235171775.23590362),
    (14, 217344434.72723606),
    (15, 204413441.83494195),
    (16, 190263982.8895071)
]

show_elbow(kd_data)
