import librosa
import pydub
from utils.array_manipulation import concatenate_arrays

class Pydub_AudioChunkMerger:
    """AudioChunkMerger concatenates audio files together and saves them to a
    single wav file.
    """

    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate

    def create_audio_segments(self, audio_file_paths):
        """Concatenate audio files in a single audio file.

        :param audio_file_paths: (list of str) List of audio files to
            concatenate together

        :return: (np.ndarray) Concatenated audio time series
        """

        audio_segments = []
        for file in audio_file_paths:
            audio_segment = pydub.AudioSegment.from_file(file, format="wav")
            audio_segments.append(audio_segment)

        return audio_segments
    
    def fade_tracks(self, remix, audio_segments, transition_beats):
        
        beat_selector = remix.beat_selector
        beats = remix._beats

        faded_audio_segments = []

        curr_beat_num = 0
        while len(beats) >= 2:
            curr_beat = beats[0]
            next_beat = beats[1]
            if curr_beat.track != next_beat.track:

                transition_beat_num = transition_beats.pop(0)

                next_transition_beat_num = self._get_next_transition(audio_segments, transition_beats)

                fade_beat_num = transition_beat_num + int((next_transition_beat_num - transition_beat_num)/1.5)

                num_trans_beats = fade_beat_num - curr_beat_num
                if num_trans_beats < 1:
                    continue

                fade_out_beat = beats.pop(0)

                fade_out_audio_segment = self._get_fade_out_audio_segments(beat_selector, fade_out_beat, num_trans_beats)
                fade_out_audio_segments_merged = self.merge_faded_audio_segments(fade_out_audio_segment, "out")

                fade_in_audio_segment = self._get_fade_in_audio_segments(beats, num_trans_beats)
                fade_in_audio_segments_merged = self.merge_faded_audio_segments(fade_in_audio_segment, "in")

                faded_audio_segments = self._crossfade_audio_segments(faded_audio_segments, fade_in_audio_segments_merged, fade_out_audio_segments_merged)

                curr_beat_num = curr_beat_num + num_trans_beats

            else:

                self._append_new_audio_segment(faded_audio_segments, beats)
                curr_beat_num = curr_beat_num + 1

        return faded_audio_segments

    def _crossfade_audio_segments(self, faded_audio_segments, fade_in_audio_segments_merged, fade_out_audio_segments_merged):

        fade_out_audio_segments_merged.fade(to_gain=-120, from_gain=-1, start=0, end=len(fade_out_audio_segments_merged), duration=None)
        fade_in_audio_segments_merged.fade(to_gain=-1, from_gain=-120, start=0, end=len(fade_in_audio_segments_merged), duration=None)
        overlay = fade_in_audio_segments_merged.overlay(fade_out_audio_segments_merged)
        faded_audio_segments.append(overlay)
        return faded_audio_segments


    def _append_new_audio_segment(self, faded_audio_segments, beats):
        faded_beat = beats.pop(0)
        faded_beat_audio_segment = self._convert_to_audio_segment(faded_beat)
        faded_audio_segments.append(faded_beat_audio_segment)
        print(faded_beat.file_path + " added!")
        return faded_audio_segments

    def _convert_to_audio_segment(self, beat):
        return pydub.AudioSegment.from_file(beat.file_path, format="wav") 

    def _get_fade_in_audio_segments(self, beats, num_trans_beats):
        print("Fading In")
        fade_in_audio_segments = []
        for beat_num in range(0, num_trans_beats):
            if beats:
                fade_in_beat = beats.pop(0)
                fade_in_audio_segments.append(self._convert_to_audio_segment(fade_in_beat))
                print(fade_in_beat.file_path + " added")
            else:
                break
        return fade_in_audio_segments

    def _get_fade_out_audio_segments(self, beat_selector, fade_out_beat, num_trans_beats):
        print("fadeing out")
        fade_out_beats = []
        fade_out_beats.append(fade_out_beat)

        fade_audio_segments = []

        first_audio_segment = self._convert_to_audio_segment(fade_out_beat)
        fade_audio_segments.append(first_audio_segment)
        print(fade_out_beat.file_path + " added")

        for fade_beat_num in range(0, num_trans_beats-1):
            fade_next_beat = beat_selector._get_next_beat_in_track_if_possible_or_random(fade_out_beats[-1], random=False)
            if fade_next_beat:
                fade_out_beats.append(fade_next_beat)
                fade_audio_segments.append(pydub.AudioSegment.from_file(fade_next_beat.file_path, format="wav"))
                print(fade_next_beat.file_path + " added")
            else:
                break

        return fade_audio_segments

    def _get_next_transition(self, audio_segments, transition_beats):
        if transition_beats:
            next_transition = transition_beats[0]
        else:
            next_transition = len(audio_segments)
        return next_transition

    def merge_audio_segments(self, audio_segments):
        concat_segments = audio_segments.pop(0)
        for segment in audio_segments:
            concat_segments = concat_segments + segment
        return concat_segments
    
    def merge_faded_audio_segments(self, audio_segments, type):
        concat_segments = audio_segments.pop(0)
        for segment in audio_segments:
            concat_segments = concat_segments + segment
        return concat_segments

    def load_audio_file(self, audio_file_path):
        return librosa.load(audio_file_path, sr=self.sample_rate)[0]

