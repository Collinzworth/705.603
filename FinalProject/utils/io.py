import os
import pickle
import librosa
import soundfile as sf


def load(path, sr):
    """Load an audio file as a floating point time series.

    :param path: (str) Path to the input file
    :param sr: (int) Sample rate

    :return (np.ndarray) Audio signal
    """
    return librosa.load(path, sr=sr)[0]


def save_to_pickle(save_path, data):
    """Serialize data to pickle file.

    :param save_path: (str) Path where to store data
    :param data: (Python object) Object to store
    """
    with open(save_path, "wb") as file:
        pickle.dump(data, file)


def load_from_pickle(load_path):
    """Deserialize data from pickle file.

    :param load_path: (str) Path of file to load

    :return: (Python obj) Deserialised data
    """
    with open(load_path, "rb") as file:
        data = pickle.load(file)
    return data


def write_wav(path, signal, sr):
    """Write a time series to wav.

    :param path: (str) Path of file to be saved
    :param signal: (np.ndarray) Time series to be saved
    :param sr: (int) Sample rate
    """
    sf.write(path, signal, sr, subtype="PCM_24")



def remove_file(file):
    # Try to delete the file.
    try:
        os.remove(file)
        print(file + " removed!")
    except OSError as e:
        # If it fails, inform the user.
        print("Error: %s - %s." % (e.filename, e.strerror))
        pass

def load_processed_files(filepath):
    segmented_files = []
    with open(filepath, "wb") as file:
        segmented_files = [filename for filename in file]
    return segmented_files

def check_if_directory_exists(directory):
    """
    Checks if directory exists. If it doesn't it creates it.

    :param directory (str): directory to check or create. 
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

# Used to change directory for already created mapping files
def adjust_mapping_file(MAPPING_FILE):
    
    pkl_data = load_from_pickle(MAPPING_FILE)

    for row in pkl_data:
        row = row.replace("/mnt/d/Creating_AI_Systems/Final_Project_Versions/1/final_project", os.getcwd())

    save_to_pickle("pickle_check.pkl", pkl_data)
    