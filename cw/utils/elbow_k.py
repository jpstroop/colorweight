# https://pythonprogramminglanguage.com/kmeans-elbow-method/
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html

import cv2
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt

image_path = '/Users/jstroop/workspace/colorweight/samples/01_in.jpg'

CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 1.0) # consider 1.0; may want lower?
FLAGS = cv2.KMEANS_RANDOM_CENTERS

K_MAX = 16 # higher (16?) for real use

image_data = cv2.imread(image_path)
arr = np.float32(image_data) # a 3d ndarray
pixels = arr.reshape((-1, 3))

data = []

for k in range(1, K_MAX+1):
    compactness, labels, centroids = cv2.kmeans(pixels, k, None, CRITERIA, 10, FLAGS)
    data.append((k, compactness))

def show_elbow(data):
    ks = [e[0] for e in data]
    dist = [e[1] for e in data]
    plt.plot(ks, dist, 'bo-')
    plt.plot((ks[0], ks[-1]), (dist[0], dist[-1]), 'r--')
    plt.xlabel('k')
    plt.ylabel('distortion')
    plt.title('elbow showing the optimal k')
    plt.show()

def find_best_k_index(dist_curve, debug=False):
    # See: https://en.wikipedia.org/wiki/Vector_projection
    # and: https://stackoverflow.com/a/37121355/714478
    n_points = len(dist_curve) # could this be the ks instead?
    all_coords = np.vstack((range(n_points), dist_curve)).T
    np.array([range(n_points), dist_curve])
    first_point = all_coords[0]
    line_vector = all_coords[-1] - first_point
    line_vector_norm = line_vector / np.sqrt(np.sum(line_vector**2))
    vector_from_first = all_coords - first_point
    scalar_prod = np.sum(vector_from_first * np.matlib.repmat(line_vector_norm, n_points, 1), axis=1)
    vector_from_first_parallel = np.outer(scalar_prod, line_vector_norm)
    vector_to_line = vector_from_first - vector_from_first_parallel
    dist_to_line = np.sqrt(np.sum(vector_to_line ** 2, axis=1))
    index_of_best_point = np.argmax(dist_to_line)
    if debug:
        print(f'Distortion curve: {dist_curve}')
        print(f'All coords: {all_coords}')
        print(f'First point: {first_point}')
        print(f'Line vector: {line_vector}')
        print(f'Line vector normalized: {line_vector_norm}')
        print(f'Vector from first: {vector_from_first}')
        print(f'Scalar product: {scalar_prod}')
        print(f'Vector from first parallel: {vector_from_first_parallel}')
        print(f'Vector to line: {vector_to_line}')
        print(f'Distance to line: {dist_to_line}')
        print(f'Index of best K: {index_of_best_point}')
    return index_of_best_point

dist_curve = [e[1] for e in data]
best_k_index = find_best_k_index(dist_curve)
print(f'Best K: {data[best_k_index]}')
