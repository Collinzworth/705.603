import librosa

from data.extraction.extractor import Extractor


class RMSExtractor(Extractor):
    """Concrete Extractor that extracts RMS sequences from signal."""

    def __init__(self, frame_size=1024, hop_length=512, num_coefficients=13):
        super().__init__("rms")
        self.frame_size = frame_size
        self.hop_length = hop_length
        self.num_coefficients = num_coefficients

    def extract(self, signal, sample_rate):
        """Extract RMS from time series using librosa.

        :param signal: (np.ndarray) Audio time series
        :param sr: (int) Sample rate

        :return: (np.ndarray) RMS sequence
        """
        
        # rms, phase = librosa.magphase(librosa.stft(y=signal,
        #                                            n_fft=self.frame_size,
        #                                            hop_length=self.hop_length))


        rms = librosa.feature.rms(y=signal,
                                    hop_length=self.hop_length)
        

        return rms