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


class SVM():
    def __init__(self):
        self.gs_svc = GridSearchCV(SVC(), self.parameters)
        self.best_params = {}

    @property
    def parameters(self):
        return {
            'kernel': ['linear', 'rbf'],
            'C': np.linspace(0.5, 1.0, 5)
        }

    def train(self, X_train, y_train, X_test, y_test):
        start = time.time()
        self.gs_svc = self.gs_svc.fit(X_train, y_train)
        print("Time run SVM: ", time.time() - start)
        self.best_parameters

        return f"""<h3>Máquina de Vetor de Suporte</h3>
        <p>Utilizando a <b>Máquina de Vetor de Suporte</b> plotamos cada item de dados como um ponto no espaço n-dimensional, com o valor de cada recurso sendo o valor de uma determinada coordenada.</p>
        <p>Então, executamos a classificação encontrando o hiperplano que diferencia muito bem as duas classes</p>""", None

    @property
    def best_parameters(self):
        self.best_params = self.gs_svc.best_params_

    def fit(self, X_train, y_train):
        params = self.best_params
        classifier = SVC(kernel=params['kernel'], C=params['C'])
        classifier.fit(X_train, y_train)
        return classifier

    def accuracy(self, classifier, y_test, X_test):
        y_pred = classifier.predict(X_test)
        return accuracy_score(y_test, y_pred), y_pred
