from segmentation.segmentextractor import SegmentExtractor
from code_demonstration.write_processed_files import generate_processed_files

default_sr = 22050

def main():

    input_dir = "/mnt/d/Creating_AI_Systems/music/small_subset"
    output_dir = "/mnt/d/Creating_AI_Systems/music/segmented_subset"

    seg_extractor = SegmentExtractor(default_sr)
    seg_extractor.create_and_save_segments(input_dir, output_dir)
    generate_processed_files()


if __name__ == '__main__':
    main()