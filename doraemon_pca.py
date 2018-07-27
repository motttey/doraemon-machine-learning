import os
import numpy as np
from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
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

    X_pca = decomposition.TruncatedSVD(n_components=2).fit_transform(X_vec)
    # print(X_pca)

    x = []
    y = []
    for point in X_pca:
        x.append(point[0])
        y.append(point[1])

    fig,ax = plt.subplots(figsize=(12,8))
    ax.set_xlabel('')
    ax.set_ylabel('')

    scatterplot = ax.scatter(x,y)

    # プロットの上に画像を描画
    for i in range(len(X_pca)):
        aimg = X_train[i]
        img = OffsetImage(aimg, zoom=1, cmap="gist_gray")
        img.image.axes = ax
        annotate = AnnotationBbox(img, X_pca[i], xybox=(-10, 10), xycoords="data", boxcoords="offset points", pad=0.3)
        ax.add_artist(annotate)

    plt.xlabel('PC 1')
    plt.ylabel('PC 2')
    plt.legend(loc='lower left')
    plt.show()
