# -*- coding: utf-8 -*-
"""DecisionTree.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19eDNpJ0--Y3zL-Yi9dAIZ7mc6HTKe99_
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import f1_score, confusion_matrix

# Function to train a decision tree with hyperparameter tuning using GridSearchCV
def train_decision_tree(X_train, y_train, X_test, y_test):
    dt = DecisionTreeClassifier(random_state=42)
    param_grid = {'max_depth': [None, 10, 20, 30],
                  'min_samples_split': [2, 5, 10],
                  'min_samples_leaf': [1, 2, 4]}
    grid_search = GridSearchCV(dt, param_grid, cv=5, scoring='accuracy', n_jobs=4)
    grid_search.fit(X_train, y_train)
    y_pred = grid_search.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    return accuracy, grid_search.best_estimator_

# Function to calculate F1 score
def f1_accuracy(model, x_test, y_test):
    y_pred = model.predict(x_test)
    return f1_score(y_test, y_pred)

# Function to generate a confusion matrix and save it as an image
def confusionMat(model, x_test, y_test, storeFile):
    y_pred = model.predict(x_test)
    arr = confusion_matrix(y_test, y_pred)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(arr)
    plt.title('Confusion matrix of the classifier')
    fig.colorbar(cax)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    
    for (i, j), z in np.ndenumerate(arr):
        ax.text(j, i, z, ha='center', va='center')
    
    with open(storeFile, 'wb') as file:
        fig.savefig(storeFile, format='png')
        print(f'Confusion Matrix Stored at {storeFile}!')

# Load data from the specified CSV
x_train = pd.read_csv("x_train.csv")
x_test = pd.read_csv("x_test.csv")
y_train = pd.read_csv("y_train.csv").squeeze()
y_test = pd.read_csv("y_test.csv").squeeze()

# Train Decision Tree and print accuracy
accuracy, dt_model = train_decision_tree(x_train, y_train, x_test, y_test)
print("Accuracy:", accuracy)

# Calculate and print F1 score
f1_acc = f1_accuracy(dt_model, x_test, y_test)
print("F1 Score:", f1_acc)

# Generate confusion matrix and save it as an image
confusionMat(dt_model, x_test, y_test, "./results/dt_confusion_matrix.png")
