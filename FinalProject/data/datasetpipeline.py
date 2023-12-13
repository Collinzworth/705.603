import os

from utils.io import save_to_pickle


class DatasetPipeline:
    """DatasetPipeline is an end-to-end pipeline responsible to generate
    and store embeddings for a group of audio files. It provides a pipeline
    that's responsible for:
        1- extracting features from audio files
        2- performing statistical aggregation on the features to make
           embeddings time independent
        3- merging multiple feature types for each track
        5- creating mappings and dataset from merged features
        6- storing the mappings and dataset to disk
    """

    def __init__(self, dir, save_dir, file_list):

        """Generate embeddings for all audio files in a directory and
        store relative array dataset and mappings.

        :param dir: (str) Path to directory with audio files
        :param save_dir: (str) Path to directory where to save mappings and
            dataset
        """

        self.dir = dir
        self.file_list = file_list
        self.save_dir = save_dir
    
        self.batch_extractor = None
        self.multi_track_batch_aggregator = None
        self.feature_merger = None
        self.data_preparer = None


    def process(self):

        tracks_features = self._extract_features()

        tracks_aggregations = self.multi_track_batch_aggregator.aggregate(tracks_features)
        print("Performed statistical aggregation of features")

        tracks_merged_features = self.feature_merger.merge(tracks_aggregations)

        self.mapping, self.dataset = self.data_preparer.prepare_mapping_and_dataset(tracks_merged_features)
        self._normalize_dataset()
        print("Prepared mapping and dataset")

        mapping_path = self._save_data(self.save_dir, self.mapping, "mapping")
        print(f"Saved mapping to {mapping_path}")

        dataset_path = self._save_data(self.save_dir, self.dataset, "dataset")
        print(f"Saved dataset to {dataset_path}")

    def _save_data(self, save_dir, data, data_type):
        save_path = os.path.join(save_dir, f"{data_type}.pkl")
        save_to_pickle(save_path, data)
        return save_path


    def _extract_features(self):
        if self.file_list:
            tracks_features = self.batch_extractor.extract_from_file_list(self.file_list)
        else:
            tracks_features = self.batch_extractor.extract(self.dir)
        print("Extracted features")
        return tracks_features
    
    def _normalize_dataset(self):
        dataset_norm = (self.dataset - self.dataset.min(0)) / self.dataset.ptp(0)
        self.dataset = dataset_norm
        return