import utils.file_name_manipulation as fnm
import utils.processed_file_tracker as pft
import os

SAVE_DIR = os.path.join(os.getcwd(), "code_demonstration")

def generate_processed_files():

    # Avoid processing previously processed files
    pft.write_all_segmented_files(SAVE_DIR)

    print("Processed file created")


if __name__ == "__main__":
    generate_processed_files()