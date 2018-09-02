# https://pythonprogramminglanguage.com/kmeans-elbow-method/
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html

import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = '/Users/jstroop/workspace/colorweight/samples/01_in.jpg'

CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 1.0)
FLAGS = cv2.KMEANS_RANDOM_CENTERS

def cluster(pixels, k):
     return cv2.kmeans(pixels, k, None, CRITERIA, 10, FLAGS)

image_data = cv2.imread(image_path)
arr = np.float32(image_data) # a 3d ndarray
pixels = arr.reshape((-1, 3))

data = []

for k in range(1, 16):
    compactness, labels, centroids = cluster(pixels, k)
    data.append((k, compactness))


ks = [e[0] for e in data]
dist = [e[1] for e in data]
plt.plot(ks, dist, 'bo-')
plt.plot((ks[0], ks[-1]), (dist[0], dist[-1]), 'r--')
plt.xlabel = 'K values'
plt.ylabel = 'Distortions'
plt.show()

# TODO: use this to find the label: https://stackoverflow.com/a/37121355/714478
