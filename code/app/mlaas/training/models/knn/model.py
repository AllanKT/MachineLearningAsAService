import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from imblearn.under_sampling import RandomUnderSampler
from sklearn import preprocessing
from sklearn.svm import SVC # "Support vector classifier"
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.neighbors import KNeighborsClassifier

import time
import datetime
import os
import sys

from training.models.graph import Graph


class KNN():
    def __init__(self):
        self.graph = Graph('KNN')
        self.gs_knn = GridSearchCV(KNeighborsClassifier(), self.parameters)
        self.best_params = {}

    @property
    def parameters(self):
        return {
            'n_neighbors': np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            'metric': ['minkowski', 'euclidean']
        }

    def train(self, X_train, y_train, X_test, y_test):
        start = time.time()
        self.gs_knn = self.gs_knn.fit(X_train, y_train)
        print("Time run KNN: ", time.time() - start)
        self.best_parameters

        error = self.error(X_train, y_train, X_test, y_test)
        path = self.graph.hist_dashed(error, 'Error Rate K Value', 'K Value', 'Mean Error', (12, 6), 1, 10)
        params = self.best_params
        return f"""<h3>K Vizinhos mais Próximos</h3>
        <p>A ideia principal do <b>K Vizinhos mais Próximos</b> é determinar o rótulo de classificação de uma amostra baseado nas amostras vizinhas advindas de um conjunto de treinamento.</p>
        <p>A variável k representa a quatidade de vizinhos mais próximos que serão utilizados para averiguar de qual classe a nova amostra pertence.</p>
        <p>O melhor valor de K encontrado foi <i>{params['n_neighbors']}</i> utilizando a métrica <i>{params['metric']}</i>.</p>""", path

    @property
    def best_parameters(self):
        self.best_params = self.gs_knn.best_params_

    def error(self, X_train, y_train, X_test, y_test):
        error = []

        for i in range(1, 10):  
            knn = KNeighborsClassifier(n_neighbors=i)
            knn.fit(X_train, y_train)
            pred_i = knn.predict(X_test)
            error.append(np.mean(pred_i != y_test))
        return error

    def fit(self, X_train, y_train):
        params = self.best_params
        classifier = KNeighborsClassifier(n_neighbors=params['n_neighbors'], metric=params['metric'])
        classifier.fit(X_train, y_train)
        return classifier

    def accuracy(self, classifier, y_test, X_test):
        y_pred = classifier.predict(X_test)
        return accuracy_score(y_test, y_pred), y_pred
