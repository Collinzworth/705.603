
import os
from segmentation.segmentextractor import SegmentExtractor
from code_demonstration.write_processed_files import generate_processed_files

default_sr = 22050

def segmentation():

    input_dir = os.path.join(os.getcwd(), "code_demonstration//music")
    output_dir = os.path.join(os.getcwd(), "code_demonstration//segmented_songs")

    seg_extractor = SegmentExtractor(default_sr)
    seg_extractor.create_and_save_segments(input_dir, output_dir)
    generate_processed_files()



if __name__ == '__main__':
    segmentation()