import os
import random
import json
import utils.processed_file_tracker as pft
import utils.file_name_manipulation as fnm

PROCESSED_FILE = os.path.join(os.getcwd(), "code_demonstration\\Segmented_Files.txt")
PROCESSED_JSON = os.path.join(os.getcwd(), "code_demonstration\\Segmented_Files.json")

def write_all_segmented_files(dir):
    """ Retrieves all processed filenames from folder that has been processed.
    
    :param dir: (List[str]) List containing filenames that have been processed.

    :return None
    """
    processed_files = []
    processed_dict = {}
    for root, _, files in os.walk(dir):
        for file in files:
            full_path = os.path.join(root, file)
            file = file.replace("‐", "-")
            filename = fnm.get_file_name(file)
            filename = filename.split("_")[0]
            if filename not in processed_files:
                processed_files.append(filename)

            try:
                processed_dict[filename].append(full_path)
            except:
                processed_dict[filename] = [full_path]
                pass

    write_json(processed_dict)
    pft.write_processed_file(processed_files)

    return processed_files

def write_json(file_dict):

    # Serializing json
    json_object = json.dumps(file_dict, indent=4)
    
    # Writing to sample.json
    with open(PROCESSED_JSON, "w") as outfile:
        outfile.write(json_object)

    return



def write_processed_file(processed_files):

    try:
        with open(PROCESSED_FILE, 'a') as f:
            for processed_file_name in processed_files:
                try:
                    write_data = processed_file_name + "\n"
                    f.write(write_data)
                    print(processed_file_name + " added!")
                except:
                    print(processed_file_name + " cannot be written!")
    except:
        print(PROCESSED_FILE + " cannot be opened")





def check_processed_file(processed_file_name):
    """
    
    Checks if the file has been processed already. If it has it is written the the processed file for referencing. 
    This is to avoid having to process previously processed data on large datasets

    :param processed_file_name: (str) Full path and filename of the audio file that is being checked

    :return (bool): 
    """

    processed_file_name = processed_file_name.replace("‐", "-")    # Replace non-ascii hyphen
    processed_files = get_processed_files()
    processed_file_name = processed_file_name.split(".")[0]        # Remove extension and keep only file name

    if processed_file_name in processed_files:
        return True

    return False


def get_processed_files():
    try:
        with open(PROCESSED_FILE) as file:
            processed_files = [line.strip() for line in file]
        return processed_files
    except:
        # File does not exist
        return []



def sample_processed_file(num_samples, exclusions=None):
    """
    :param processed_file_name: (str) Full path and filename of the audio file that is being checked

    :return (List[string]): 
    """

    processed_files = get_processed_files()
    for file in list(processed_files):
        for exclusion in exclusions:
            if exclusion.lower() in file.lower():
                processed_files.remove(file)

    if num_samples ==  "all":
        return processed_files
    elif isinstance(num_samples, int):
        random_sample = random.sample(processed_files, num_samples)
    else:
        raise ValueError('Number of samples is incorrect. Please specify all or an integer')

    return random_sample

def get_subset_file_list(song_list):

    """
    :param song_list: (List[str]) list of songs that are contained the the subset list

    :return (List[string]): list of paths of the songs contained in the subset list 
    """

    with open(PROCESSED_JSON, 'r') as openfile:
        file_dict = json.load(openfile)

    file_list = []
    for song in song_list:
        song_files = file_dict[song]
        file_list.extend(song_files)

    return file_list