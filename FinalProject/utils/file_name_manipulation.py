import os
import taglib


def extract_artist_name(filename):
    """ Extract artist from input file name

    :param filename: (str) Filename in the format {Artist}-{album}-{song#}-{song_name}

    :return (str) Artist name
    """
    filename_data = filename.split("-")
    return filename_data[0]

def extract_album_name(filename):
    """ Extract album from input file name

    :param filename: (str) Filename in the format {Artist}-{album}-{song#}-{song_name}

    :return (str) Album name
    """
    filename_data = filename.split("-")
    return filename_data[1]

def extract_song_name(filename):
    """ Extract song from input file name

    :param filename: (str) Filename in the format {Artist}-{album}-{song#}-{song_name}

    :return (str) Song name
    """
    filename_data = filename.split("-")
    return filename_data[3]


def remove_non_wave_ext(file):
    """ Remove non .wav extensions from file

    :param filename: (str) Filename in the format {Artist}-{album}-{song#}-{song_name}.{ext}

    :return (str) Filename without extension
    """
    # Remove non wav extensions
    if "wav" not in get_file_format(file):
        filename = get_file_name(file)
    return filename

def get_file_name(file):
    """ Retrieves filename from file by splitting the extension out

    :param filename: (str) Filename in the format Artist}-{album}-{song#}-{song_name}.{ext}

    :return (str) Filename without extension
    """
    filename = file.split(".")[0]
    return filename


def get_file_format(file):
    """ Retrieves file extension from file by splitting the extension out

    :param filename: (str) Filename in the format Artist}-{album}-{song#}-{song_name}.{ext}

    :return (str) File extension
    """
    file_format = file.split(".")[1]
    return file_format


def set_song_metadata(filepath, filename):
    """ Writes song meta data to file
    
    :param filepath: (str) Full file path and file name to open file
    :param filename: (str) Filename in the format Artist}-{album}-{song#}-{song_name}.{ext}

    :return None
    """
    with taglib.File(filepath, save_on_exit=True) as song:
        song.tags["ARTIST"] = extract_artist_name(filename)
        song.tags["ALBUM"] = extract_album_name(filename)
        song.tags["TITLE"] = extract_song_name(filename)
    return
