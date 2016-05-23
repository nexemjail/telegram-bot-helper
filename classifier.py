import pandas
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import os
from service_metadata import db_credentials
import numpy as np
from utils.db_connection import get_portraits, get_universities

PATH = 'classifier/knn'


def learn():
    portraits, university_map_ids = get_portraits()
    knn = KNeighborsClassifier()
    knn.fit(portraits, university_map_ids)
    joblib.dump(knn, os.path.join(PATH, 'knn_classifier.jbl'))


def classify(vector):
    universities = get_universities()
    knn = joblib.load(os.path.join(PATH, 'knn_classifier.jbl'))
    prediction = knn.predict(vector)[0]
    return universities[prediction]

if __name__ == '__main__':
    # learn()
    print(classify(np.array([0.5]*52)))


