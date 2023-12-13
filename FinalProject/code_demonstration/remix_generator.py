import os
from utils.io import load_from_pickle, write_wav
from remix.pydub_audiochunkmerger import Pydub_AudioChunkMerger
from remix.audiochunkmerger import AudioChunkMerger
from remix.featureretriever import FeatureRetriever
from search.nnsearch import NNSearch
from remix.beatselector import BeatSelector
from remix.remixer import Remixer

SAMPLE_RATE = 22050

# change these paths to run the script with your data
MAPPING_PATH = os.getcwd() + "\\code_demonstration\\dataset\\mapping.pkl"
FEATURES_PATH = os.getcwd() + "\\code_demonstration\\dataset\\pca_dataset.pkl"
NEAREST_NEIGHBOUR_PATH = os.getcwd() + "\\code_demonstration\\models\\knn_pca_model.pkl"


# SAVE_PATH = os.getcwd() + "\\code_demonstration\\outputs"
# FILENAME = os.getcwd() + "\\code_demonstration\\knn_pca_model\\sound_example.wav"

# jump_rate = 0.1
# num_beats = 50
# faded = True


class remix_generator():
    def __init__(self):
        self.jump_rate = None
        self.num_beats = None
        self.faded = None

    def generate_remix(self, file_name, jump_rate, num_beats, faded):

        self.jump_rate = jump_rate
        self.num_beats = num_beats
        self.faded = faded

        file_path = os.path.join(SAVE_PATH, file_name)

        remixer, chunk_merger = self._create_objects()
        remix = remixer.generate_remix()

        if faded:
            audio_segments = chunk_merger.create_audio_segments(remix.file_paths)
            faded_audio_segments = chunk_merger.fade_tracks(remix, audio_segments, remix.transition_beats)
            concatenated_audio_segments = chunk_merger.merge_audio_segments(faded_audio_segments)
            concatenated_audio_segments.export(file_path, format="wav")
        else:
            audio_remix = chunk_merger.concatenate(remix.file_paths)
            write_wav(file_path, audio_remix, SAMPLE_RATE)
            print(f"Saved new remix to {SAMPLE_RATE}")

        print(f"Generated remix with {self.num_beats} beats")


    def _create_objects(self):

        beats_file_paths = load_from_pickle(MAPPING_PATH)
        features = load_from_pickle(FEATURES_PATH)
        nearest_neighbour_model = load_from_pickle(NEAREST_NEIGHBOUR_PATH)

        chunk_merger = self._choose_chunk_merger()

        feature_retriever = FeatureRetriever()
        feature_retriever.mapping = beats_file_paths
        feature_retriever.features = features

        # Create Nearest Neighbor Model
        nn_search = NNSearch()
        nn_search.mapping = beats_file_paths
        nn_search.model = nearest_neighbour_model

        # Create Beat Selector
        beat_selector = BeatSelector(self.jump_rate)
        beat_selector.nn_search = nn_search
        beat_selector.feature_retriever = feature_retriever
        beat_selector.beat_file_paths = beats_file_paths

        # Create Remixer
        remixer = Remixer(self.num_beats)
        remixer.beat_selector = beat_selector

        return remixer, chunk_merger

    def _choose_chunk_merger(self):
        # Create Chunk Merger
        if self.faded:
            chunk_merger = Pydub_AudioChunkMerger()
        else:
            chunk_merger = AudioChunkMerger()
        return chunk_merger

if __name__ == "__main__":
    remix_generator = remix_generator()
    remix_generator.generate_remix(FILENAME, jump_rate, num_beats, faded)