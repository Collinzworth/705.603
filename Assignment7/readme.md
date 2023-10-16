# Assignment 7 Readme

In this assignment, time series data from carotid and illiac readings are used to predict the age group of patients.

Docker Hub Link:
https://hub.docker.com/repository/docker/collinzworth/705.603/general  
Contains working docker image of the model's service under tag 705.603:assignment7_1

Contains files:

*time_series_processing_Service.py* - web service to classify age groups based on carotid and illiac readings. 

*time_series_processing.py* - class containing methods to perform random forest prediction on time series data. 

*TimeSeriesProcessing.ipynb* - notebook demonstrating time series preprocessing manipulation and the inference. Interpolation, filtering, and scaling are performed on the training data before training the random forest model.


### Issues

None to report
