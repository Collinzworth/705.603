# Multiple Linear Regression

# Importing the libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class carsfactors:

    def __init__(self):
        self.modelLearn = False
        self.stats = 0

    def model_learn(self):

        # Importing the dataset into a pandas dataframe
        car_info_df = pd.read_csv('cars.csv')

        # Remove Unwanted Columns - 'manufacturer_name', 'model_name', 'engine_fuel','engine_has_gas', 'engine_type', 'engine_capacity','has_warranty', 'is_exchangeable', 'state', 'location_region', drivetrain',  'number_of_photos','up_counter', 'feature_0', 'feature_1','feature_2', 'feature_3', 'feature_4', 'feature_5', 'feature_6', 'feature_7'
        unwanted_columns = ['manufacturer_name', 'model_name', 'engine_fuel','engine_has_gas', 'engine_type', 'engine_capacity','has_warranty', 'is_exchangeable', 'state', 'location_region', 'drivetrain',  'number_of_photos','up_counter', 'feature_0', 'feature_1','feature_2', 'feature_3', 'feature_4', 'feature_5', 'feature_6', 'feature_7', "feature_8", "feature_9"]
        car_info_df_dropped = car_info_df.drop(labels=unwanted_columns, axis=1)
        
        # Seperate X and y (features and label)  The last feature "duration_listed" is the label (y)
        # Seperate X vs Y
        car_info_df_label = car_info_df_dropped.iloc[:,[-1]]
        car_info_df_features = car_info_df_dropped.drop(car_info_df_label.columns, axis = 1)

        # Do the ordinal Encoder for car type to reflect that some cars are bigger than others.  
        # This is the order 'universal','hatchback', 'cabriolet','coupe','sedan','liftback', 'suv', 'minivan', 'van','pickup', 'minibus','limousine'
        # make sure this is the entire set by using unique()
        # create a seperate dataframe for the ordinal number - so you must strip it out and save the column
        # make sure to save the OrdinalEncoder for future encoding due to inference
    
        body_type_order = ['universal','hatchback', 'cabriolet','coupe','sedan','liftback', 'suv', 'minivan', 'van','pickup', 'minibus','limousine']
        body_type_vals = car_info_df["body_type"].unique()
        if sorted(body_type_order) == sorted(body_type_vals):
            print("All values are contained in body type column")
        else:
            print("Different number of attributes in data than ranked list")

        body_type_rankings = [[i, body_type] for body_type, i in enumerate(body_type_order)]
        body_types_encoded = OrdinalEncoder()
        body_types_encoded.fit(body_type_rankings)
        self.body_types_encoded = body_types_encoded

        numpy_col_vals = car_info_df["body_type"].to_numpy().reshape(-1, 1)
        transformed_body_types =  body_types_encoded.fit_transform(numpy_col_vals)

        car_info_df_body_encoded = pd.DataFrame(transformed_body_types, columns=["body_type_transformed"])

        # Do onehotencoder for Transmission only - again you need to make a new dataframe with just the encoding of the transmission
        # save the OneHotEncoder to use for future encoding of transmission due to inference

        transmission_encoder = OneHotEncoder()
        transmission_encoder.fit(car_info_df["transmission"].to_numpy().reshape(-1, 1))
        encoded_trans_values = transmission_encoder.fit_transform(car_info_df[['transmission']]).toarray()
        self.transmission_encoder = transmission_encoder
    
        car_info_df_trans_encoded = pd.DataFrame(encoded_trans_values, columns=transmission_encoder.get_feature_names())

        # Do onehotencoder for Color
        # Save the OneHotEncoder to use for future encoding of color for inference
        color_encoder = OneHotEncoder()
        encoded_color_values = color_encoder.fit_transform(car_info_df[['color']]).toarray()
        car_info_df_color_encoded = pd.DataFrame(encoded_color_values, columns=color_encoder.get_feature_names())
        self.color_encoder = color_encoder

        # the all three together endocdings into 1 data frame (need 2 steps with "concatenate")
        # add the ordinal and transmission then add color
        transformed_dfs = [car_info_df_body_encoded, car_info_df_trans_encoded, car_info_df_color_encoded]
        transformed_col_df = pd.concat(transformed_dfs, axis=1)

        # then dd to original data set
        total_df = pd.concat([car_info_df_features, transformed_col_df], axis=1)

        # delete the columns that are substituted by ordinal and onehot - delete the text columns for color, transmission, and car type 
        preprocessed_features_df = total_df.drop(["body_type", "transmission", "color"], axis=1)

        # Splitting the dataset into the Training set and Test set - use trian_test_split
        test__perc = .20      # 20% for test split
        feature_train, feature_test, label_train, label_test = train_test_split(preprocessed_features_df, car_info_df_label, test_size= test__perc)

        # Feature Scaling - required due to different orders of magnitude across the features
        # make sure to save the scaler for future use in inference

        feature_info = {}
        feature_bt_xform_info = {}
        feature_odometer_info = {}
        feature_year_info = {}
        feature_price_info = {}

        feature_bt_xform_info["mean"] = feature_train["body_type_transformed"].mean()
        feature_bt_xform_info["std"] = feature_train["body_type_transformed"].std()
        feature_info["bt_xform"] = feature_bt_xform_info

        feature_odometer_info["mean"] = feature_train["odometer_value"].mean()
        feature_odometer_info["std"] = feature_train["odometer_value"].std()
        feature_info["odometer"] = feature_odometer_info

        feature_year_info["mean"] = feature_train["year_produced"].mean()
        feature_year_info["std"] = feature_train["year_produced"].std()
        feature_info["year"] = feature_year_info

        feature_price_info["mean"] = feature_train["price_usd"].mean()
        feature_price_info["std"] = feature_train["price_usd"].std()
        feature_info["price"] = feature_price_info

        # scale feature train inputs
        feature_train.loc[:, "body_transformed_scaled"] = (feature_train["body_type_transformed"]-feature_bt_xform_info["mean"])/feature_bt_xform_info["std"] 
        feature_train.loc[:, "odometer_value_scaled"] = (feature_train["odometer_value"]-feature_odometer_info["mean"])/feature_odometer_info["std"]
        feature_train.loc[:, "year_produced_scaled"] = (feature_train["year_produced"]-feature_year_info["mean"])/feature_year_info["std"]
        feature_train.loc[:, "price_usd_scaled"] = (feature_train["price_usd"]-feature_price_info["mean"])/feature_price_info["std"]

        # scale feature test inputs with train mean/std from training set
        feature_test.loc[:, "body_transformed_scaled"] = (feature_test["body_type_transformed"]-feature_bt_xform_info["mean"])/feature_bt_xform_info["std"] 
        feature_test.loc[:, "odometer_value_scaled"] = (feature_test["odometer_value"]-feature_odometer_info["mean"])/feature_odometer_info["std"]
        feature_test.loc[:, "year_produced_scaled"] = (feature_test["year_produced"]-feature_year_info["mean"])/feature_year_info["std"]
        feature_test.loc[:, "price_usd_scaled"] = (feature_test["price_usd"]-feature_price_info["mean"])/feature_price_info["std"]

        feature_train = feature_train.drop(["odometer_value", "year_produced", "price_usd", "body_type_transformed"], axis=1)
        feature_test = feature_test.drop(["odometer_value", "year_produced", "price_usd", "body_type_transformed"], axis=1)

        self.feature_info = feature_info

        # Training the Multiple Linear Regression model on the Training set
        regressor = LinearRegression()
        self.regressor = regressor

        regressor.fit(feature_train, label_train)
        
        self.stats = regressor.score(feature_train, label_train)
        self.modelLearn = True

        return

    # this demonstrates how you have to convert these values using the encoders and scalers above
    def model_infer(self, transmission, color, odometer, year, bodytype, price):

        if(self.modelLearn == False):
            self.model_learn()

        body_types_encoded = self.body_types_encoded
        transmission_encoder = self.transmission_encoder
        color_encoder = self.color_encoder 
        feature_info = self.feature_info 
        regressor = self.regressor

        # convert the body type into a numpy array that holds the correct encoding
        body_type_array = np.array([bodytype]).reshape(-1, 1)
        carTypeTest = body_types_encoded.transform(body_type_array)
        car_type_info = feature_info["bt_xform"]

        # Scale encoded body type
        carTypeTest = (carTypeTest - car_type_info["mean"])/car_type_info["std"]

        # convert the transmission into a numpy array with the correct encoding
        trans_array = np.array([transmission]).reshape(-1, 1)
        carHotTransmissionTest = transmission_encoder.transform(trans_array).toarray()

        # conver the color into a numpy array with the correct encoding
        color_array = np.array([color]).reshape(-1, 1)
        carHotColorTest = color_encoder.transform(color_array).toarray()

        # add the three above
        total = np.concatenate((carTypeTest, carHotTransmissionTest), axis=1)
        total = np.concatenate((total, carHotColorTest), axis=1)

        # Standarize odometer, year, and price
        odometer_info = feature_info["odometer"]
        odometer_scaled = (odometer - odometer_info["mean"])/odometer_info["std"]

        year_info = feature_info["year"]
        year_scaled = (year - year_info["mean"])/year_info["std"]

        price_info = feature_info["price"]
        price_scaled = (price - price_info["mean"])/price_info["std"]

        # build a complete test array and then predict
        othercolumns = np.array([[odometer_scaled, year_scaled, price_scaled]])
        totaltotal = np.concatenate((total, othercolumns), axis=1)

        # determine prediction
        y_pred = regressor.predict(totaltotal)
        return y_pred[0][0]

    def model_stats(self):
        if(self.modelLearn == False):
            self.model_learn()
        return str(self.stats)
