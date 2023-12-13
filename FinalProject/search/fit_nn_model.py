from sklearn.neighbors import NearestNeighbors
from utils.io import load_from_pickle, save_to_pickle

def fit_nearest_neighbors(dataset_file, model_filepath):

    dataset = load_from_pickle(dataset_file)

    nearest_neighbour = NearestNeighbors()
    nearest_neighbour.fit(dataset)

    print("Created nearest neighbor")
    save_to_pickle(model_filepath, nearest_neighbour)
    print(f"Saved nearest neighbor model to {model_filepath}")


if __name__ == "__main__":
    fit_nearest_neighbors()