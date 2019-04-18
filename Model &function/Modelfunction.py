from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from scipy import stats
import numpy as np
import pandas as pd
import xgboost as xgb
import math
import os


def predict_calories(model_name, features):
    # model_name: name of the trained xgboost model, e.g.: 'calorie_predictor.model'
    # features: 1 x 11 features as numpy array, e.g.: np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]) where the numbers are feature values

    # Loads the model saved in model_name. Runs the model using given feature vector. Returns the predicted calories.

    # loading model
    mod = xgb.Booster({'nthread':4})
    mod.load_model(model_name)

    assert np.shape(features)[0] == 11 # make sure number of features is correct

    features = features[np.newaxis, :]
    feat = xgb.DMatrix(features)

    return mod.predict(feat)


# Example testing script
model_name = 'calorie_predictor.model'
features = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])

pred_calories = predict_calories(model_name, features)
print('Predicted calories is {}'.format(pred_calories))
