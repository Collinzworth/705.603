import librosa
import matplotlib.pyplot as plt

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