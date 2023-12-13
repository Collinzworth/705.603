
import os
from utils.processed_file_tracker import sample_processed_file, get_subset_file_list, write_all_segmented_files
from utils.io import check_if_directory_exists
from data.datapipelinebuilder import Data_Pipeline_Builder
from sklearn.decomposition import PCA

from search.fit_nn_model import fit_nearest_neighbors

from utils.io import load_from_pickle, save_to_pickle

SEGMENT_DIR = os.getcwd() + "/music/segmented_files"
MODEL_DIR = os.getcwd() + "/generated_models/"
MAPPING_INPUT = os.getcwd() + "/generated_models/mapping.pkl"

PROCESSED_JSON = os.getcwd() + "/music/Segmented_Files.json"
PROCESSED_FILE = os.getcwd() + "/music/Segmented_FIles.txt"

DATASET_FILE = "dataset.pkl"
PCA_DATASET_FILE = "pca_dataset.pkl"

EXCLUSIONS = ["KISS", "Hendrix", "Cardi", "Bring Me the", "Limp", "Rob Zombie", "System of a Down", "Bob Marley"]

class generate_dataset():

    """
        Provides methods and tools to generate the dataset and file mapping file from either a directory where segments were made or from another mapping file.
        The class can generate the dataset, perform PCA, and fit a nearest neighbor model on the generated datasets.

    """

    def __init__(self, num_samples):

        feature_list = ["chromagram", "mfcc", "tempo_ratio"]

        self.segment_dir = SEGMENT_DIR
        write_all_segmented_files(SEGMENT_DIR)  
    
        self.file_list = self.make_file_list(num_samples)
        self.feature_list = feature_list

        # self.mapping_input = mapping_input
        self.data_pipeline = None

        check_if_directory_exists(MODEL_DIR)
        self.model_dir = MODEL_DIR


    def make_file_list(self, num_samples):

        # if mapping_input:
        #     return load_from_pickle(mapping_input)

        # # Load preselected songs from a mapping file or sample a new one
        # user_selection = input("Load mapping file y/n?: ")
        # if user_selection == "y":
        #     mapping_input = input("Input mapping file full path: ")
        #     file_list = load_from_pickle(mapping_input)
        # elif user_selection == "n":
        #     num_samples = input("Input number of songs to sample from segment directory: ")
        try:
            num_samples = int(num_samples)
        except:
            if num_samples == "all":
                pass
            else:
                print("Non integer user input entered")
                quit()


        file_list = sample_processed_file(num_samples, EXCLUSIONS)
        # if num_samples != 'all':
        file_list = get_subset_file_list(file_list)
        self._print_sampled_songs(file_list)
        # else:
        #     print("Invalid file selection")
        #     quit()

        return file_list

    def _print_sampled_songs(self, file_list):
        for file in file_list:
            print(file + " selected for sample!")
        return

    def create_dataset(self):

        pipeline_builder = Data_Pipeline_Builder(self.feature_list, self.segment_dir, self.model_dir, self.file_list)
        pipeline_builder.create_data_pipeline()

        data_pipeline = pipeline_builder.dataset_pipeline
        data_pipeline.process()

        self.data_pipeline = data_pipeline
        self.dataset = data_pipeline.dataset

    def fit_nn(self, model_name):
        """
        Fits nearest neighbor model on the generated dataset and pickles to a file.

        :params model_name (str): file name to pickle model to.
        """
        dataset_file = os.path.join(self.model_dir, DATASET_FILE)
        model_file = os.path.join(self.model_dir, model_name)
        fit_nearest_neighbors(dataset_file, model_file)



    def create_pca_dataset(self, n_components):
        """
        Performs principal component analysis on the dataset and pickles a new dataset.

        :params n_components (int): number of components to reduce dimensions to.
        """
        pca = PCA(n_components=n_components)
        pca_dataset = pca.fit_transform(self.dataset)

        self.pca_dataset = pca_dataset
        self.pca_filepath = os.path.join(self.model_dir, PCA_DATASET_FILE)
        
        save_to_pickle(self.pca_filepath, pca_dataset)
        print("PCA Dataset saved to " +  self.pca_filepath)




if __name__ == "__main__":

    # mfcc - aggregates to row of 13
    # chromagram - aggregates to row of 12
    # tempo_ratio - aggregates to row of 13



    # model_dir = os.getcwd() + "/generated_models/small_subset"
    # segment_dir = "G:\\segmented_songs"
    # "model_dir": model_dir

    # directory_args = {
    #     "segment_dir": segment_dir
    # }

    generated_dataset = generate_dataset(num_samples=3)
    generated_dataset.create_dataset()

    generated_dataset.fit_nn("nn_model.pkl")

    generated_dataset.create_pca_dataset(20)

    generated_dataset.fit_nn("pca_nn_model.pkl")