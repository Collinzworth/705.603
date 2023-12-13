import utils.file_name_manipulation as fnm
import utils.processed_file_tracker as pft
import os

def main():
    save_dir = os.path.join(os.getcwd(), "code_demonstration\\music")

    # Avoid processing previously processed files
    pft.write_all_segmented_files(save_dir)

    print("Processed file created")


if __name__ == "__main__":
    main()