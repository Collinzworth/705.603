import os

from utils.io import load, write_wav, remove_file

import utils.file_name_manipulation as fnm
import utils.processed_file_tracker as pft 

from segmentation.beattracker import estimate_beats
from segmentation.trackcutter import cut

class SegmentExtractor:
    """SegmentExtractor is responsible to divide songs into beats and save
    the corresponding signals as audio files.
    """

    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self._audio_format = "wav"
        self._input_file_formats = ["wav", "flac", "mp3"]

    def create_and_save_segments(self, dir, save_dir):
        """Performs the following steps for each audio file in a
        directory:
            1- load audio file
            2- extract beat locations
            3- segment signal into as many chunks as beats we have
            4- save audio segments to wav

        :param dir: (str) Directory containing audio files to be preprocessed
        :param save_dir: (str) Directory where to save segments
        """

        for root, _, files in os.walk(dir):
            for file in files:
                if pft.check_processed_file(file):
                    continue
                if fnm.get_file_format(file) in self._input_file_formats:
                    try:
                        print("Processing " + file)
                        self._create_and_save_segments_for_file(file, root, save_dir)
                        print("Processed " + file)
                    except Exception as e:
                        print(e)
                        print("Cannot process " + file + " :(")
                        # remove_file(os.path.join(root, file))
                        pass
        
    def _create_and_save_segments_for_file(self, file, root, save_dir):
        
        orig_file_path = os.path.join(root, file)
        
        signal = load(orig_file_path, self.sample_rate)
        beat_events = estimate_beats(signal, self.sample_rate)

        segments = cut(signal, beat_events)
        self._write_segments_to_wav(file, save_dir, segments)


    def _write_segments_to_wav(self, file, save_dir, segments):
        
        filename = fnm.remove_non_wave_ext(file)

        for segment_number, segment in enumerate(segments):
            save_path = self._generate_save_path(filename, save_dir, segment_number)
            write_wav(save_path, segment, self.sample_rate)
            fnm.set_song_metadata(save_path, filename)

    def _generate_save_path(self, file, save_dir, segment_number):
        file_name = f"{file}_{segment_number}.{self._audio_format}"
        save_path = os.path.join(save_dir, file_name)
        return save_path


