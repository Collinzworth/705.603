import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 
from wandb import Classes
from scipy import ndimage
from copy import deepcopy

class ObjectDetection():
    
    def  __init__(self):
        
        # load yolo
        net = cv.dnn.readNet("yolov3.weights", "yolov3.cfg") # note weights to too big for github must save within readme
        self.net = net
        self.ln = net.getLayerNames()

        classes = []
        with open("coco.names", 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        layer_name = net.getLayerNames()
        output_layer = [layer_name[i - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        self.output_layer = output_layer
        self.classes = classes
        self.colors = colors

        return
   
    def read_image(self, img_filename):
        img = cv.imread(img_filename)
        return img

    def modify_and_plot_objects(self, img_filename):

        img = cv.imread(img_filename)

        scale_plot_params = []
        print("Scaling")
        for scale_factor in range(1, 200, 10):
            scaled_image = self.scale_image(img, scale_factor)
            detections = self.determine_object(scaled_image)
            scale_plot_params = self.add_labels_confidence(scale_plot_params, scale_factor, detections)
            self.print_classes(detections)
    
        self.plot_results(scale_plot_params, "Scale Factor")

        rotation_plot_params = []
        print("Rotating")
        for rotation_factor in range(0, 180, 10):
            rotated_image = self.rotate_image(img, rotation_factor)
            detections = self.determine_object(rotated_image)
            rotation_plot_params = self.add_labels_confidence(rotation_plot_params, rotation_factor, detections)
            self.print_classes(detections)

        self.plot_results(rotation_plot_params, "Rotation Factor")
        
        noise_plot_params = []
        print("Inserting Noise")
        for noise in range(0, 60, 5):
            noise_factor = noise/10
            noisy_image = self.add_speckle_noise(img, noise_factor)
            detections = self.determine_object(noisy_image)
            noise_plot_params = self.add_labels_confidence(noise_plot_params, noise_factor, detections)
            self.print_classes(detections)
            if not detections:
                break
        
        self.plot_results(noise_plot_params, "Speckle Noise Factor")

        return

    def plot_results(self, object_plot_params, plot_label):
        
        line_thicc = 2
        fig, ax = plt.subplots()
        for i, object in enumerate(object_plot_params):

            pred_class = object[0]
            line_label = "Detection " + str(i) + ": " + str(pred_class)
    
            x_vals = []
            y_vals = []
            for vals in object[1:len(object)]:
                x_vals.append(vals[0])
                y_vals.append(vals[1])
            
            x_val_arr = np.array(x_vals)
            y_val_arr = np.array(y_vals)

            plt.title(plot_label)
            plt.xlabel(plot_label)
            plt.ylabel("confidence")
            plt.plot(x_val_arr, y_val_arr, label=line_label, linewidth=line_thicc)
            plt.legend()

            line_thicc = line_thicc + 1

        plt.savefig(plot_label)
        plt.show()

        return
    
    def add_labels_confidence(self, object_plot_params, modify_factor, detections):
        for i, detection in enumerate(detections):
            try:
                if detection[0] == object_plot_params[i][0]:
                    object_plot_params[i].append([modify_factor, detection[1]])
                else:
                    object_plot_params.append([detection[0], [modify_factor, detection[1]]])
            except:
                object_plot_params.append([detection[0], [modify_factor, detection[1]]])

        return object_plot_params



    def print_classes(self, detections):
        classes = self.classes
        for i, detection in enumerate(detections):
            label = detection[0]
            print(f'Object {str(i)}: {label} with confidence of {detection[1]:.2f}')
        return
    
    
    def scale_image(self, img, scale_factor):

        new_width = int(img.shape[1]*scale_factor/100)
        new_height = int(img.shape[0]*scale_factor/100)
        new_dim = (new_width, new_height)

        img_resized = cv.resize(img, new_dim)  # Add code to resize

        return img_resized

    def rotate_image(self, img, rotation_factor):
        return ndimage.rotate(img, rotation_factor)

    def add_speckle_noise(self, img, noise_factor):
        gauss = np.random.normal(0, noise_factor, img.shape)  # add code to add speckle noise
        gauss = gauss.reshape(img.shape[0], img.shape[1], img.shape[2]).astype('uint8')
        speckle_img = img + img*gauss
        return speckle_img


    def determine_object(self, img):

        height, width, _ = img.shape

        net = self.net
        output_layer = self.output_layer
        classes = self.classes
        colors = self.colors

        #note - 0.00392 = 1/250   416 is a standard square for yolo
        resized = cv.resize(img, (224, 224))
        blob = cv.dnn.blobFromImage(resized, scalefactor=0.00392, size=(224, 224), swapRB=True)  # Fill in other fields to create image compatible with cv

        #detect objects
        net.setInput(blob)
        outs = net.forward(output_layer)

        # Showing Information on the screen
        class_ids = []
        confidences = []
        boxes = []
        detections = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detection
                    center_x = int(detection[0] *  width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Reactangle Cordinate
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        detections = []
        font = cv.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                detections.append((label, confidences[i]))
                color = colors[i]
                cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv.putText(img, label, (x, y + 30), font, 3, color, 3)

        return detections