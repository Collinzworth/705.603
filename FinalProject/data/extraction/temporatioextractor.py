import librosa

from data.extraction.extractor import Extractor

class TempoRatioExtractor(Extractor):
    """Concrete Extractor that extracts tempogram ratio from signal"""

    def __init__(self, frame_size=1024, hop_length=512, num_coefficients=13):
        super().__init__("tempo_ratio")
        self.frame_size = frame_size
        self.hop_length = hop_length
        self.num_coefficients = num_coefficients

    def extract(self, signal, sample_rate):
        """Extract tempogram ratio from time series using librosa.

        :param signal: (np.ndarray) Audio time series
        :param sr: (int) Sample rate

        :return: (np.ndarray) tempo
        """

        tempo_ratio = librosa.feature.tempogram_ratio(y=signal,
                                                        hop_length=self.hop_length,
                                                        sr=sample_rate)
                

        return tempo_ratio