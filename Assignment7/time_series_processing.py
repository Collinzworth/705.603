# Time Series Processing

# Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from scipy.ndimage import gaussian_filter1d

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

from scipy import interpolate

def eliminate_noise(data, sigma=1):
    for column in data.columns:
        no_noise = gaussian_filter1d(data[column], sigma)
        data[column] = no_noise
    return data

def standardize_features(data, trained_data=pd.DataFrame()):

    if not trained_data.empty:
        stat_data = trained_data
    else:
        stat_data = data

    for column in data.columns:
        data[column] = (data[column] - stat_data[column].mean())/stat_data[column].std()

    return data


# def inference_interpolate(data, trained_data, int_df_size=100):

#     input_data_index = data.index[0]
#     int_start_row = (input_data_index - int_df_size)
#     if int_start_row < 0:
#         int_start_row = 0   
#     int_end_row = input_data_index - 1
#     int_df = trained_data[int_start_row:int_end_row]
#     data = pd.concat([int_df, data])
    
#     interpolated_data = data.astype(float).interpolate(method="polynomial", order=3, limit_direction='both', limit_area = None)    
#     #interpolated_data = interpolated_data.interpolate(method="linear", limit_direction='both', limit_area = None)

#     interpolated_datapoint = interpolated_data.loc[interpolated_data.index == input_data_index]
#     print(interpolated_datapoint.isnull().sum(axis=0))
#     return interpolated_datapoint



# def apply_interpolation2(x_array, data_column, row, column):

#     if np.isnan(row[column]):
#         index = row.name
#         data_column_array = np.array(data_column)
#         interpolated_value = np.interp(index, x_array, data_column_array)
#         data_column_array[index] = interpolated_value
    
#     return

# def interpolate_columns2(data, trained_data):

#     if not trained_data.empty:
#         input_data_index = data.index[0]

#         data = pd.concat([trained_data, data])

#     x_array = np.array(data.index)


#     for column in data.columns:

#         data_column = data[column]

#         null_df = data[data[column] == np.nan]

#         null_df.apply(lambda row: apply_interpolation(x_array, data_column, row, column))

#         #interpolated_value = np.interp(2.5, x_array, data_column_array)

#         # interpolated_array = interpolate.CubicSpline(x_array, data_column_array, axis=0, extrapolate=True)

#         # data[column] = interpolated_array

#         # data[column] = data[column].astype(float).interpolate(method="linear", limit_direction='both')
#         # data[column] = data[column].astype(float).interpolate(method='spline', order=2)  

#     if not trained_data.empty:
#         data = data.loc[data.index == input_data_index]

#     return data


# def interpolate_columns(data, trained_data, int_df_size=200):

#     # If no trained data is passed, use inference interpolation
#     if not trained_data.empty:
#         return inference_interpolate(data, trained_data, int_df_size)

#     # For training data interpolation, interpolate with spline in chunks of int_df_size
#     interp_dfs = []
#     for int_start_row in range(0, len(data), int_df_size):
#         int_end_row = int_start_row + int_df_size
#         if int_end_row > len(data):
#             int_df = data[int_start_row:len(data)]
#         else:
#             int_df = data[int_start_row:int_end_row]
        
#         interpolated_df = int_df.astype(float).interpolate(method="polynomial", order=3, limit_direction='both', limit_area = None)
#         # interpolated_df = int_df.astype(float).interpolate(method="linear", limit_direction='both', limit_area = None)
        
#         print(interpolated_df.isnull().sum(axis=0))
#         interp_dfs.append(interpolated_df)

#     inter_dataframe = pd.concat(interp_dfs, axis=0)


    # data.interpolate(method='spline', order=2, inplace=True)  
    # for column in data.columns:
    #     data_column = data[column]
    #     interpolate_df = pd.concat([data_column.shift])

    #     data[column] = data[column].astype(float).interpolate(method="linear", limit_direction='both')
    #     data[column] = data[column].astype(float).interpolate(method='spline', order=2)  

   # return inter_dataframe


def interpolate_columns(data, trained_data):

    if not trained_data.empty:
        input_data_index = data.index[0]
        data = pd.concat([trained_data, data])

   #data.interpolate(method='spline', order=2, inplace=True)  
    for column in data.columns:
        data[column] = data[column].astype(float).interpolate(method="linear", limit_direction='both')

    if not trained_data.empty:
        data = data.loc[data.index == input_data_index]


    return data


class CombinedCardiacPressure():
   
    def __init__(self):
        self.modelLearn = False
        self.stats = 0


    def _cleanup(self, data, trained_data=pd.DataFrame()):

        # interpolate data
        data = interpolate_columns(data, trained_data)

        # filter noise
        data = eliminate_noise(data, self.sigma)

        return data

    def model_learn(self, sigma=3):
        
        # Set filter standard deviation
        self.sigma = sigma

        # Importing the dataset
        carotid_df = pd.read_csv(os.getcwd() + "/data/carotid_pressure.csv", index_col=0)
        illiac_df = pd.read_csv(os.getcwd() + "/data/illiac_pressure.csv", index_col=0)

        # Set up X input and y target
        y = carotid_df[carotid_df.columns[-1]]
        X_carotid = carotid_df.drop(labels=["target"], axis=1)
        X_illiac = illiac_df.drop(labels=["target"], axis=1)

        # Interpolate, filter, and standardize data
        X_carotid_cleaned = self._cleanup(X_carotid)
        X_illiac_cleaned = self._cleanup(X_illiac)

        self.X_carotid = X_carotid_cleaned
        self.X_illiac = X_illiac_cleaned

        # Scale features with standardizing
        X_carotid_preprocessed = standardize_features(X_carotid_cleaned)
        X_illiac_preprocessed = standardize_features(X_illiac_cleaned)

        # Combine Carotid and Illiac inputs
        X = pd.concat([X_carotid_preprocessed, X_illiac_preprocessed], axis=1)

        # Splitting the dataset into the Training set and Test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

        # Training the Random Forest Classifier on the set
        self.classifier = RandomForestClassifier()
        self.classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = self.classifier.predict(X_test)

        # Making the Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        self.cm = cm
    
        self.stats = accuracy_score(y_test, y_pred)
        self.modelLearn = True

        return
        
    def model_infer(self, carotid_filename, illiac_filename):
        
        if(self.modelLearn != True):
            self.model_learn()

        carotid_df = pd.read_csv(carotid_filename, index_col=0)
        illiac_df = pd.read_csv(illiac_filename, index_col=0)

        # Interpolate, filter, and standardize data
        carotid_clean= self._cleanup(carotid_df, self.X_carotid)
        carotid_preprocessed = standardize_features(carotid_clean, self.X_carotid)

        illiac_clean = self._cleanup(illiac_df, self.X_illiac)
        illiac_preprocessed = standardize_features(illiac_clean, self.X_illiac)

        # Combine Carotid and Illiac inputs
        dataOne = pd.concat([carotid_preprocessed, illiac_preprocessed], axis=1)

        # Use classifier to predict the value
        y_pred = self.classifier.predict(dataOne)

        return y_pred
    
    def model_stats(self):
        if(self.modelLearn == False):
            self.model_learn()
        return str(self.stats)




class CarotidPressure():

    def __init__(self):
        self.modelLearn = False
        self.stats = 0


    def _cleanup(self, data, trained_data=pd.DataFrame()):

        # interpolate data
        data = interpolate_columns(data, trained_data)

        # filter noise
        data = eliminate_noise(data, self.sigma)

        return data

    def model_learn(self, sigma=3):
        
        # Set filter standard deviation
        self.sigma = sigma

        # Importing the dataset
        carotid_df = pd.read_csv(os.getcwd() + "/data/carotid_pressure.csv", index_col=0)

        # Set up X input and y target
        y = carotid_df[carotid_df.columns[-1]]
        X_carotid = carotid_df.drop(labels=["target"], axis=1)

        # Interpolate, filter, and standardize data
        X_carotid_cleaned = self._cleanup(X_carotid)

        self.X_carotid = X_carotid_cleaned

        # Scale features with standardizing
        X_carotid_preprocessed = standardize_features(X_carotid_cleaned)

        # Combine Carotid inputs
        X = X_carotid_preprocessed

        # Splitting the dataset into the Training set and Test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

        # Training the Random Forest Classifier on the set
        self.classifier = RandomForestClassifier()
        self.classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = self.classifier.predict(X_test)

        # Making the Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        self.cm = cm
    
        self.stats = accuracy_score(y_test, y_pred)
        self.modelLearn = True

        return
        
    def model_infer(self, carotid_filename):
        
        if(self.modelLearn != True):
            self.model_learn()

        carotid_df = pd.read_csv(carotid_filename, index_col=0)

        # Interpolate, filter, and standardize data
        carotid_cleaned = self._cleanup(carotid_df, self.X_carotid)
        carotid_preprocessed = standardize_features(carotid_cleaned, self.X_carotid)

        dataOne = carotid_preprocessed

        # Use classifier to predict the value
        y_pred = self.classifier.predict(dataOne)

        return y_pred
    
    def model_stats(self):
        if(self.modelLearn == False):
            self.model_learn()
        return str(self.stats)





class IlliacPressure():

    def __init__(self):
        self.modelLearn = False
        self.stats = 0


    def _cleanup(self, data, trained_data=pd.DataFrame()):

        # interpolate data
        data = interpolate_columns(data, trained_data)

        # filter noise
        data = eliminate_noise(data, self.sigma)

        return data

    def model_learn(self, sigma=3):
        
        # Set filter standard deviation
        self.sigma = sigma

        # Importing the dataset
        illiac_df = pd.read_csv(os.getcwd() + "/data/illiac_pressure.csv", index_col=0)

        # Set up X input and y target
        y = illiac_df[illiac_df.columns[-1]]
        X_illiac = illiac_df.drop(labels=["target"], axis=1)

        # Interpolate, filter, and standardize data
        X_illiac_cleaned = self._cleanup(X_illiac)

        self.X_illiac = X_illiac_cleaned

        # Scale features with standardizing
        X_illiac_preprocessed = standardize_features(X_illiac_cleaned)

        # Combine Carotid and Illiac inputs
        X = X_illiac_preprocessed

        # Splitting the dataset into the Training set and Test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

        # Training the Random Forest Classifier on the set
        self.classifier = RandomForestClassifier()
        self.classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = self.classifier.predict(X_test)

        # Making the Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        self.cm = cm
    
        self.stats = accuracy_score(y_test, y_pred)
        self.modelLearn = True

        return
        
    def model_infer(self, illiac_filename):
 
        if(self.modelLearn != True):
            self.model_learn()
    
        illiac_df = pd.read_csv(illiac_filename, index_col=0)

        # Interpolate, filter, and standardize data
        illiac_preprocessed = self._cleanup(illiac_df, self.X_illiac)

        X_illiac_preprocessed = standardize_features(illiac_preprocessed, self.X_illiac)

        # Combine Carotid and Illiac inputs
        dataOne = X_illiac_preprocessed

        # Use classifier to predict the value
        y_pred = self.classifier.predict(dataOne)

        return y_pred
    
    def model_stats(self):
        if(self.modelLearn == False):
            self.model_learn()
        return str(self.stats)




if __name__ == '__main__':
        # m = CarotidPressure()
        # m = IlliacPressure()
        m = CombinedCardiacPressure()

        m.model_learn(sigma=3)

        # result = m.model_infer(pd.read_csv('data/carotid_pressure_test_1.csv', index_col=0))
        # print(result)

        # result = m.model_infer(pd.read_csv('data/carotid_pressure_test_2.csv', index_col=0))
        # print(result)

        # result = m.model_infer(pd.read_csv('data/carotid_pressure_test_3.csv', index_col=0))
        # print(result)

        # result = m.model_infer(pd.read_csv('data/carotid_pressure_test_4.csv', index_col=0))
        # print(result)
            
        # print(m.stats)


        result = m.model_infer('data/carotid_pressure_test_1.csv', 'data/illiac_pressure_test_1.csv')
        print(result)

        result = m.model_infer('data/carotid_pressure_test_2.csv', 'data/illiac_pressure_test_2.csv')
        print(result)
        result = m.model_infer('data/carotid_pressure_test_3.csv', 'data/illiac_pressure_test_3.csv')
        print(result)

        result = m.model_infer('data/carotid_pressure_test_4.csv', 'data/illiac_pressure_test_4.csv')
        print(result)
            
        print(m.stats)

