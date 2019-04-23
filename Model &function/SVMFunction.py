from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score, make_scorer
from sklearn.preprocessing import StandardScaler
from scipy import stats
import numpy as np
import pandas as pd
import math
import os
from sklearn.svm import SVR
import pickle



def predict_calories(model_name, scale_name, features):
    # model_name: name of the trained Gradient Boosted Regressor model, e.g.: 'calorie_predictor_GBR.model'
    # scale_name: name of file containing variable to scale features
    # features: 1 x 11 features as numpy array, e.g.: np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]) where the numbers are feature values

    # Loads the model saved in model_name. Runs the model using given feature vector. Returns the predicted calories.

    # loading model
    with open(model_name, 'rb') as f:
        calorie_model = pickle.load(f)

    # loading scaler
    with open(scale_name, 'rb') as f:
        X_scaler = pickle.load(f)

    assert np.shape(features)[0] == 11 # make sure number of features is correct

    features = features[np.newaxis, :]
    features = X_scaler.transform(features)


    return calorie_model.predict(features)
