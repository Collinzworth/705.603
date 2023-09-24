# Assignment 4 Readme

In this assignment data related to car's ads vs how long the ads sat are analyzed in order to predict the length of time until a car is purchased. Various data transformations are demonstrated. Unwanted columns are dropped, ordinal data is encoded, categorical data is one-hot encoded, and finally numeric features are standardized in order to allow scaling between features.

Docker Hub Link:
https://hub.docker.com/repository/docker/collinzworth/705.603/general  
Contains working docker image of the model's service.

Contains files:

*carfactors.py* - Contains the program to create the model, infer inputs, and score the model.  
*carfactors_service.py* - Allows the model to run as a web service.  
*cars.csv* - Training data used to train the model.  
*carfactors.ipynb* - Notebook for showing model outputs and running the service with links. Commentary on the model's performance and methods of improvement are discussed at the end.  


### Issues

If an error "object has no attribute 'get_feature_names_out'" is experienced, find/replace *get_feature_names_out* to *get_feature_names* in carsfactors.py. Conflicting versions of sklearn between development environment and container environment are causing this slight difference in functionality. 
