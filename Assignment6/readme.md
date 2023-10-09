# Assignment 6 Readme

In this assignment, images are processed with opencv and object detection is performed. "Assignment6.ipynb" contains loops to alter the input image through scaling, rotation, and noise insertion in order to plot the object detections confidence in chosen object vs the change in parameter. 

Docker Hub Link:
https://hub.docker.com/repository/docker/collinzworth/705.603/general  
Contains working docker image of the model's service under tag 705.603:assignment6_1

Contains files:

*objectDetectionService.py* - web service to classify objects in images and give confidence.  
*Object_Detection.py* - class containing methods to perform object detection.  
*Assignment6.ipynb* - notebook demonstrating opencv image manipulation and the object detection class. Scaling, rotation, and noise factors are plotted against the image classifiers confidence in it's estimate.  
*coco.names* - names file required for model. Lists objects that can be detected.  
*yolov3.weights* - weights for model.  

Additionally, the model will need to be downloaded. Download "yolov3.weights" from:  
https://pjreddie.com/media/files/yolov3.weights


### Issues

None to report
