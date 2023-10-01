# Natural Language Processing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('stopwords')

class Sentiment():
    def __init__(self):
        self.modelLearn = False
        self.stats = 0
        self.stopwords = False
        
    def _cleanup(self, dataset):

        corpus = []
        num_lines = len(dataset)
        all_stopwords = stopwords.words('english')

        for i in range(0, num_lines):

            # Get words only using regex in re
            line = dataset["Review"].iloc[i]
            line_words = re.findall("[A-Za-z']+", line)

            # Make all lower case
            line_words_lower = [None]*len(line_words)
            for index, word in enumerate(line_words):
                line_words_lower[index] = word.lower()

            # Split into an array of strings necessary to remove stop words
            line_stopwords = []
            for index, word in enumerate(line_words):
                if word in all_stopwords:
                    line_stopwords.append(word)

            influence_stopwords = ["no", "not", "did", "didn't", "only", "above", "had", "hadn't"]
            all_stopwords_adjusted = [stop_word for stop_word in all_stopwords if i not in influence_stopwords]

            # Add back in words that may influence the sentiment such as 'not'
            # Split into an array of strings necessary to remove stop words
            line_words_no_stop_words = [word for word in line_words if word not in all_stopwords_adjusted]

            # Stem the words and filter out stopwords
            stemmer = PorterStemmer()
            porter_stemmed = [stemmer.stem(word) for word in line_words_no_stop_words]

            # Turn back into a string
            review = " ".join(porter_stemmed) 

            # Append the string to the total
            corpus.append(review)

        return corpus

    def model_learn(self):

        # Importing the dataset
        dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

        corpus = self._cleanup(dataset)

        # Creating the Bag of Words model
        from sklearn.feature_extraction.text import CountVectorizer

        # fit to an array using fit_transform
        vectorizer = CountVectorizer()
        self.vectorizer = vectorizer
        
        corpus_vect = vectorizer.fit_transform(corpus)
        corpus_vect_arr = corpus_vect.toarray()

        # Set the label (1 for good, 0 for bad)
        labels = dataset["Liked"]

        # Creating the Bag of Words model
        from sklearn.feature_extraction.text import CountVectorizer

        # Splitting the dataset into the Training set and Test set
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(corpus_vect_arr, labels, test_size = 0.20, random_state = 0)

        # Training the Naive Bayes model on the Training set
        from sklearn.naive_bayes import GaussianNB
        self.classifier = GaussianNB()
        self.classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = self.classifier.predict(X_test)

        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix, accuracy_score
        cm = confusion_matrix(y_test, y_pred)
        
        self.stats =  accuracy_score(y_test, y_pred)
        self.modelLearn = True

    def model_infer(self, captureString):
        
        if(self.modelLearn != True):
            self.model_learn()

        # Build 1 entry dictionary similar to Reviews structure with Review:String    
        input_string_dict = {"Review": [captureString]}
        
        # Convert into a dataframe
        datapoint = pd.DataFrame.from_dict(input_string_dict)

        # Cleanup the dataframe
        clean_data = self._cleanup(datapoint)

        # Transform the datafame to an array using transform
        vectorizer = self.vectorizer
        vectorized_data = vectorizer.transform(clean_data)
        vectorized_data_array = vectorized_data.toarray()

        # Use classifier to predict the value
        label_pred = self.classifier.predict(vectorized_data_array)

        return label_pred > 0
    
    def model_stats(self):
        if(self.modelLearn == False):
            self.model_learn()
        return str(self.stats)

if __name__ == '__main__':
        m = Sentiment()
        m.model_learn()
        result = m.model_infer("bad terrible stinks horrible")
        if( result > 0):
            print("Good")
        else:
            print("Bad")
        result = m.model_infer("fantastic wonderful super good")
        if( result > 0):
            print("Good")
        else:
            print("Bad")
        print( m.model_stats())
