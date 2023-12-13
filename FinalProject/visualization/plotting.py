import librosa
import matplotlib.pyplot as plt

import librosa
import matplotlib.pyplot as plt

# from utils.io import load_from_pickle
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import numpy as np

import librosa
import matplotlib.pyplot as plt
import numpy as np




def plot_chromagram(signal, sr):

    S = np.abs(librosa.stft(signal))
    chroma = librosa.feature.chroma_stft(y=signal, sr=sr)

    fig, ax = plt.subplots(figsize=(20, 10), nrows=2, sharex=True)
    img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=ax[0])
    fig.colorbar(img, ax=[ax[0]])
    ax[0].label_outer()
    img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
    fig.colorbar(img, ax=[ax[1]])




def plot_mfcc(signal, sr, num_mfcc):
    
    S = np.abs(librosa.stft(signal))
    mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=num_mfcc)

    fig, ax = plt.subplots(figsize=(20, 10), nrows=2, sharex=True)
    img = librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
                                x_axis='time', y_axis='mel', fmax=8000,
                                ax=ax[0])

    fig.colorbar(img, ax=[ax[0]])
    ax[0].set(title='Mel spectrogram')
    ax[0].label_outer()
    img = librosa.display.specshow(mfccs, x_axis='time', ax=ax[1])
    fig.colorbar(img, ax=[ax[1]])
    ax[1].set(title='MFCC')


def plot_tempo(signal, sr):

    tempogram = librosa.feature.tempogram(y=signal, sr=sr)
    tgr = librosa.feature.tempogram_ratio(tg=tempogram, sr=sr)
    fig, ax = plt.subplots(figsize=(20, 10), nrows=2, sharex=True)

    tempo_img = librosa.display.specshow(tempogram, x_axis='time', y_axis='tempo', ax=ax[0])
    temporat_img = librosa.display.specshow(tgr, x_axis='time', ax=ax[1])

    ax[0].label_outer()
    ax[0].set(title="Tempogram")
    ax[1].set(title="Tempogram ratio")

    fig.colorbar(tempo_img, ax=[ax[0]])
    fig.colorbar(temporat_img, ax=[ax[1]])

    plt.savefig("Tempo.png")
    plt.show()

    return


# def plot_pca(num_components, filepath):

#     dataset = load_from_pickle(filepath)

#     pca = PCA(n_components=num_components)
#     pca.fit(dataset)

#     score = pca.score(dataset, y=None)

#     plt.plot(np.cumsum(pca.explained_variance_ratio_))
#     plt.xlabel('Number of Components')
#     plt.ylabel('Explained Variance')
#     plt.savefig('elbow_plot.png', dpi=100)
#     plt.show()
