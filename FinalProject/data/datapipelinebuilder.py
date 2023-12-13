from data.datasetpipeline import DatasetPipeline
from data.extraction.batchextractor import BatchExtractor

# Feature Extractors
from data.extraction.chromogramextractor import ChromogramExtractor
from data.extraction.mfccextractor import MFCCExtractor
from data.extraction.tempoextractor import TempoExtractor
from data.extraction.temporatioextractor import TempoRatioExtractor
from data.extraction.rmsextractor import RMSExtractor

# Aggregators
from data.aggregation.flatbatchaggregator import FlatBatchAggregator
from data.aggregation.meanaggregator import MeanAggregator
from data.aggregation.multitrackbatchaggregator import MultiTrackBatchAggregator
from data.featuremerger import FeatureMerger
from data.datapreparer import DataPreparer

class Data_Pipeline_Builder():
    """
        Class creates the extractors, aggregators, and finally the data pipeline.
    """
    def __init__(self, feature_names, segment_dir, save_dir, file_list):
        self.feature_names = feature_names
        self.save_dir = save_dir
        self.segment_dir = segment_dir
        self.file_list = file_list

    def create_data_pipeline(self):

        """
        
        """

        batch_extractor = self._create_extractors()

        batch_aggregator = FlatBatchAggregator()
        mean_aggregator = MeanAggregator(1)
        batch_aggregator.add_aggregator(mean_aggregator)

        mtba = MultiTrackBatchAggregator()
        mtba.batch_aggregator = batch_aggregator

        feature_merger = FeatureMerger()
        data_preparer = DataPreparer()

        # Construct Pipeline
        dataset_pipeline = DatasetPipeline(self.segment_dir, self.save_dir, self.file_list)

        # Construct extractors and aggregators
        dataset_pipeline.batch_extractor = batch_extractor
        dataset_pipeline.multi_track_batch_aggregator = mtba
        dataset_pipeline.feature_merger = feature_merger
        dataset_pipeline.data_preparer = data_preparer
        dataset_pipeline.file_list = self.file_list

        self.dataset_pipeline = dataset_pipeline



    def _create_extractors(self):

        batch_extractor = BatchExtractor()

        # Add feature extractors
        if "chromagram" in self.feature_names:
            chromogram_extractor = ChromogramExtractor()
            batch_extractor.add_extractor(chromogram_extractor)

        if "mfcc" in self.feature_names:
            mfcc_extractor = MFCCExtractor()
            batch_extractor.add_extractor(mfcc_extractor)

        if "tempogram" in self.feature_names:
            tempo_extractor = TempoExtractor()
            batch_extractor.add_extractor(tempo_extractor)

        if "tempo_ratio" in self.feature_names:
            tempo_ratio_extractor = TempoRatioExtractor()
            batch_extractor.add_extractor(tempo_ratio_extractor)

        if "rms" in self.feature_names:
            rms_extractor = RMSExtractor()
            batch_extractor.add_extractor(rms_extractor)
        
        return batch_extractor