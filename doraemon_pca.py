import os
import numpy as np
from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)
import matplotlib.pyplot as plt

from PIL import Image
import argparse
import math
import csv
import json
import glob
import random

if __name__ == "__main__":

    X_train = []
    X_vec = []

    files = glob.glob('./dd/g/1g' + '/*.png')
    for img in files:
        image = np.array(Image.open(img).resize((28,28)))
        X_vec.append(np.ravel(image))
        X_train.append(image)
    print(X_vec)
    markers = X_train
    X_pca = decomposition.TruncatedSVD(n_components=2).fit_transform(X_vec)
    print(X_pca)
    x = []
    y = []
    for point in X_pca:
        x.append(point[0])
        y.append(point[1])

    plt.scatter(x,y)

    plt.xlabel('PC 1')
    plt.ylabel('PC 2')
    plt.legend(loc='lower left')
    plt.show()
