# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 16:21:24 2020

@author: Anirudh Raghavan
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import cross_val_score, cross_val_predict
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve


# Description of data

sec_data = pd.read_csv("sec_fin_1.csv")


features = pd.read_csv("sec_fin_features.csv")
labels = pd.read_csv("sec_fin_1.csv")

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)


y_train = y_train.to_numpy()
y_train = y_train.ravel()

y_test = y_test.to_numpy()
y_test = y_test.ravel()

def check_nan(y_train):
    if np.any(np.isnan(y_train)):

        test =np.array(np.where(np.isnan(y_train)))

        tot = sum(y_train == 0) + sum(y_train == 1)
        a = sum(y_train == 0)/tot
        b = sum(y_train == 1)/tot
        if a >= b:
            val = 0
        else:
            val = 1
        
        for ind in test:    
            y_train[ind] = val
            
        return y_train

y_train = check_nan(y_train)
y_test = check_nan(y_test)

#######################################################################################

# Let us first understand the structure of our training labels

tot = sum(y_train == 0) + sum(y_train == 1)
neg = sum(y_train == 0)/tot
pos = sum(y_train == 1)/tot
        
neg
pos

# MODEL BUILDING

#Create a Gaussian Classifier
gnb = GaussianNB()

#Train the model using the training sets
gnb.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = gnb.predict(X_test)

# In order to measure the performance of our classifer, we shall use a cross
# validation performance score

cross_val_score(gnb, X_train, y_train, cv=5, scoring="recall")

# Build Confusion Matrix

confusion_matrix(y_test, y_pred)
precision_score(y_test, y_pred)
recall_score(y_test, y_pred)

y_scores = cross_val_predict(gnb, X_train, y_train, cv=3,
                             method="predict_proba")

fpr, tpr, thresholds = roc_curve(y_train, y_scores[:,1])

def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0, 1], [0, 1], 'k--') # Dashed diagonal
    [...] # Add axis labels and grid

plot_roc_curve(fpr, tpr)
plt.show()

###############################################################################

# Logistic Regression

log_reg = LogisticRegression(random_state=0, max_iter = 1000)

log_reg.fit(X_train, y_train)

cross_val_score(log_reg, X_train, y_train, cv=5, scoring="accuracy")

y_scores = cross_val_predict(log_reg, X_train, y_train, cv=3,
                             method="predict_proba")

fpr, tpr, thresholds = roc_curve(y_train, y_scores[:,1])

def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0, 1], [0, 1], 'k--') # Dashed diagonal
    [...] # Add axis labels and grid

plot_roc_curve(fpr, tpr)
plt.show()

##############################################################################

# Decision Tree





