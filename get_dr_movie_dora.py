# -*- Coding: utf-8 -*-
import cv2
import pathlib
import numpy as np
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
import codecs
import json

import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Noto Sans CJK JP']

def remove_duplicate(movie_json):
    titles = ['STAND BY ME ドラえもん 2'] # SBM2はレビューがないので除去する
    temp = []
    for movie in movie_json:
        if movie['title'] not in titles:
            temp.append(movie)
            titles.append(movie['title'])
    return temp

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

    for i, txt in enumerate(path_list):
        ax.annotate(txt, (x[i], y[i]))

    plt.show()
    return

def splited_title(title):
    splited = title.split('\u3000')
    return splited[1] if len(splited) > 1 else title

def main():
    f = codecs.open('dora_movies.json', 'r', 'utf-8')
    movie_json = remove_duplicate(json.load(f))

    title_list = [ splited_title(movie['title']) for movie in movie_json ]
    target_data = []
    for movie in movie_json:
        values_array = [value for key, value in movie['rate'].items()]
        target_data.append(values_array)

    # t-SNE適用
    # tsne = TSNE(n_components=2)
    # embedded_data = tsne.fit_transform(target_data)

    # UMAP適用
    mapper = umap.UMAP(random_state=0)
    embedded_data = mapper.fit_transform(target_data)

    # PCA適用
    # pca = PCA(n_components=2)
    # embedded_data = pca.fit_transform(target_data)

    print(title_list)

    show2DPlot(embedded_data, title_list)

if __name__ == '__main__':
    main()
