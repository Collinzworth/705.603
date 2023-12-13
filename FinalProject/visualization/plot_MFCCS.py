import librosa
import matplotlib.pyplot as plt
import numpy as np

def plot_mfcc(mfccs, S):

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