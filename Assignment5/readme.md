# Assignment 5 Readme

In this assignment reviews are processed into a Naive Bayes classification model to detect the sentiment of an input review. Input data from previous reviews is labeled as positive or negative. The reviews are cleaned up by removing stopwords and stemming the reviews with a Porter stemmer. A count vectorizer is used in sci-kit learn to transform the cleaned corpus and train the Naive Bayes classifier. The project contains the python file to train and infer the model along with a webservice to run the model in a browser. A jupyter notebook exploring the model and explaining the results is also included.

Docker Hub Link:
https://hub.docker.com/repository/docker/collinzworth/705.603/general  
Contains working docker image of the model's service under tag 705.603:assignment5_1

Contains files:

*natural_language_processing.py* - Contains the program to create the model, infer inputs, and score the model.  
*natural_language_processing_service.py* - Allows the model to run as a web service.  
*Restaurant_Reviews.tsv* - Training data used to train the model.  
*NLPProcessing.ipynb* - Notebook for showing model outputs and running the service with links. Commentary on the model's performance and methods of improvement are discussed at the end.  
*Car_Service_Notebook* - Notebook for exploring functionality within carfactors.py. Demo output is shown. (not required for assignment)


### Issues

None to report
