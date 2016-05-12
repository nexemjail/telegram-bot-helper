import pandas
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import os
from service_metadata import db_credentials


PATH = 'classifier/knn'

def repare_data():
    pass


def learn():
    knn = KNeighborsClassifier()
    # knn.fit()
    joblib.dump(knn, os.path.join(PATH, 'knn_classifier.jbl'))


def classify(vector):

    knn = joblib.load(os.path.join(PATH,'knn_classifier.jbl'))
    print(knn)

    # knn.predict()
    pass


if __name__ == '__main__':
    learn()
    classify(None)


