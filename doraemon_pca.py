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

def show2DPlot(projected_array, image_array, method_name):
    x = []
    y = []
    for point in projected_array:
        x.append(point[0])
        y.append(point[1])

    fig,ax = plt.subplots(figsize=(12,8))
    ax.set_xlabel('')
    ax.set_ylabel('')

    scatterplot = ax.scatter(x,y)

    for i in range(len(projected_array)):
        aimg = image_array[i]
        img = OffsetImage(aimg, zoom=1, cmap="gist_gray")
        img.image.axes = ax
        annotate = AnnotationBbox(img, projected_array[i], xybox=(-10, 10), xycoords="data", boxcoords="offset points", pad=0.3)
        ax.add_artist(annotate)

    plt.xlabel(method_name + ' 1')
    plt.ylabel(method_name + ' 2')
    plt.legend(loc='lower left')
    # plt.show()

    plt.savefig('output' + method_name + '.png')

if __name__ == "__main__":

    X_train = []
    X_vec = []

    files = glob.glob('./dd/g/1g' + '/*.png')
    for img in files:
        image = np.array(Image.open(img).resize((28,28)))
        X_vec.append(np.ravel(image))
        X_train.append(image)

    X_pca = decomposition.TruncatedSVD(n_components=2).fit_transform(X_vec)
    X_mds = manifold.MDS(n_components=2, dissimilarity="euclidean", random_state=3).fit_transform(X_vec)
    X_tsne = manifold.TSNE(n_components=2, perplexity=50, n_iter=500, verbose=3, random_state=1).fit_transform(X_vec)

    show2DPlot(X_pca, X_train, 'PCA')
    show2DPlot(X_mds, X_train, 'MDS')
    show2DPlot(X_tsne, X_train, 't-SNE')
