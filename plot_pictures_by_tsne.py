# -*- Coding: utf-8 -*-
import cv2
import pathlib
import numpy as np
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import codecs
import json

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def show2DPlot(projected_array, path_list):
    x = []
    y = []
    for point in projected_array:
        x.append(point[0])
        y.append(point[1])

    fig,ax = plt.subplots(figsize=(12,8))
    ax.set_xlabel('')
    ax.set_ylabel('')

    scatterplot = ax.scatter(x,y)

    for i in range(len(path_list)):
        img = OffsetImage(plt.imread(str(path_list[i]),0), zoom=0.1)
        img.image.axes = ax
        annotate = AnnotationBbox(img, projected_array[i], xybox=(-10, 10), xycoords='data', boxcoords='offset points', pad=0.3)
        ax.add_artist(annotate)

    plt.xlabel('Axis-1')
    plt.ylabel('Axis-2')
    plt.legend(loc='lower left')
    # plt.show()

    plt.savefig('output_tsne_col.png')

def main():
    target_dir = './pixiv_images/'
    path = pathlib.Path(target_dir).glob('*.png')

    f = codecs.open('output.json', 'r', 'utf-8')
    json_load = json.load(f)

    path_list = [pathlib.Path(target_dir + str(p['id']) + '.png') for p in json_load]

    # リサイズ, 配列に格納
    images = np.concatenate([cv2.resize(cv2.imread(str(p)),(100,100)).flatten().reshape(1,-1) for p in path_list], axis=0)

    # t-SNE適用
    tsne = TSNE(n_components=3)
    images_embedded = tsne.fit_transform(images)
    print(images_embedded)

    for i in range(len(json_load)):
        json_load[i]['tsne-X'] = images_embedded[i][0].astype(float)
        json_load[i]['tsne-Y'] = images_embedded[i][1].astype(float)
        json_load[i]['tsne-Z'] = images_embedded[i][2].astype(float)

    f = codecs.open('output2.json', 'w', 'utf-8')
    json.dump(json_load, f, ensure_ascii=False)
    
    # show2DPlot(images_embedded, path_list)
    return

if __name__ == '__main__':
    main()
