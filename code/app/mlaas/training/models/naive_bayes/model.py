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


class NaiveBayes():
    def __init__(self):
        self.gs_nb = GridSearchCV(MultinomialNB(), self.parameters)
        self.best_params = {}

    @property
    def parameters(self):
        return {
            'alpha': np.linspace(0.5, 1.5, 6),
            'fit_prior': [True, False]
        }

    def train(self, X_train, y_train, X_test, y_test):
        start = time.time()
        self.gs_nb = self.gs_nb.fit(X_train, y_train)
        print("Time run NaiveBayes: ", time.time() - start)
        self.best_parameters

        return f"""<h3>Naive Bayes</h3>
        <p>O algoritmo <b>Naive Bayes</b> é um classificador probabilístico baseado no “Teorema de Bayes”.</p>
        <p>Por ser muito simples e rápido, possui um desempenho relativamente maior do que outros classificadores. Além disso, o Naive Bayes só precisa de um pequeno número de dados de teste para concluir classificações com uma boa precisão.</p>""", None

    @property
    def best_parameters(self):
        self.best_params = self.gs_nb.best_params_

    def fit(self, X_train, y_train):
        params = self.best_params
        classifier = MultinomialNB(alpha=params['alpha'], fit_prior=params['fit_prior'])
        classifier.fit(X_train, y_train)
        return classifier

    def accuracy(self, classifier, y_test, X_test):
        y_pred = classifier.predict(X_test)
        return accuracy_score(y_test, y_pred), y_pred
