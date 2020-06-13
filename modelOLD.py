import numpy as numpy
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

def load_data():
    dataset = pd.read_csv('hiring.csv')
    dataset['experience'] = dataset['experience'].fillna(0)
    dataset['test_score'] = dataset['test_score'].fillna(dataset['test_score'].mean())

    X = dataset.iloc[:, :3]

    X['experience'] = X['experience'].apply(lambda x: convert_to_int(x))
    y = dataset.iloc[:,-1]

    return X, y

def train_regressor(X, y):
    regressor = LinearRegression()
    regressor.fit(X, y)
    pickle.dump(regressor, open('model.pkl', 'wb'))

def convert_to_int(word):
    word_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7,
                 'eight':8, 'nine':9, 'ten':10, 'eleven':11, 'twelve':12, 'zero':0, 0:0}
    return word_dict[word]

if __name__ == "__main__":
    X, y = load_data()

    train_regressor(X, y)