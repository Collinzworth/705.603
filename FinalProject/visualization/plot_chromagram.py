import librosa
import matplotlib.pyplot as plt
import numpy as np

def plot_chromagram(chroma, S):
    
    fig, ax = plt.subplots(figsize=(20, 10), nrows=2, sharex=True)

    img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=ax[0])

    fig.colorbar(img, ax=[ax[0]])

    ax[0].label_outer()

    img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
    fig.colorbar(img, ax=[ax[1]])\
