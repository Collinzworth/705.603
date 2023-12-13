
from utils.io import load_from_pickle
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import numpy as np

import os

def plot_pca(num_components, filepath):

    dataset = load_from_pickle(filepath)

    pca = PCA(n_components=num_components)
    pca.fit(dataset)

    score = pca.score(dataset, y=None)

    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('Number of Components')
    plt.ylabel('Explained Variance')
    plt.savefig('elbow_plot.png', dpi=100)
    plt.show()
