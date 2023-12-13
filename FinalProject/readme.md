# AI Music Mixer
Author: Aaron Collinsworth

Inspired from the infinite remixer, some additional features and testing were added on to test a K-nearest neighbor search of various beats of different songs. With the different beats, additional songs could be formed via different combinations. The result is a new mix of existing songs with similar characteristics. The infinite remixer github and youtube channel is linked below:

https://www.youtube.com/watch?v=zHdn0QgZPGY
https://github.com/musikalkemist/infiniteremixer

The final report is located in *automatic_music_mixer.ipynb*. The *code_demonstration.ipynb* notebook will walk through how the code works and explain how to run it yourself. ffmpeg might be required in order to create faded tracks. This can be downloaded here:

[https://www.ffmpeg.org/download.html[Uploading remix_generator.py…]()](https://www.ffmpeg.org/download.html)

With the executable in the top level directory this should allow the saving of audio files.

## File & Directory Overview

Notebooks:

**automatic_music_mixer.ipynb:** main notebook for final report. 

**code_demonstration.ipynb:** walks through the codes functionality and gives examples.

**pca_dimensionality_reduction.ipynb:** notebook showing process on how pca components were chosen.

**results_discussion.ipynb:** notebook presenting results and data analysis of project.

Files:

**segment_all_songs.py:** entry point python code used to segment a batch of tracks into beats.

**dataset_generator.py:** entry point python code used to generate dataset from segmented tracks. Models are also generated within the class contained in the file.

**remix_generator.py:** take the models and user input and creates a mix.

**remix_generator_service.py:** runs the remix generator as a service.

**write_processed_files.py:** Writes the segmented tracks to a txt and json file used by the dataset generator.

**requirements.txt:** library installations required.

Directories:

**code_demonstration:** Contains demonstration code that is used in the *code_demonstration.ipynb* and subdirectories containing a small subsample of songs that can be segmented and models/remixes generated.

**segmentation:** contains classes to segment tracks into individaul beat files.

**data:** contains the classes and code used to generate the dataset from the track lists.

**search:** contains classes to generate KNN model.

**remix:** contains classes to generate output mix from the models.

**utils:** contains utillity functions.

**visualization:** contains plotting functions.

**generated_models:** folder used to store generated models.

**generated_outputs:** folder used to store generated mix outputs.

**notebook_example_outputs:** example outputs used in notebooks.



