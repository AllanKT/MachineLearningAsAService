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


class Process():
    def __init__(self, file, sep, encoding, label):
        self.graph = Graph('PreProcess')
        self.file = file
        self.sep = sep
        self.encoding = encoding
        self.label = label

    @property
    def read_csv(self):
        return pd.read_csv(self.file, sep=self.sep, encoding=self.encoding)

    def clean(self, df):
        # Removendo linhas que possuam valores nulos
        print('Removendo linhas que possuam valores nulos')
        df.dropna(inplace=True)

        # Label Encoder
        print('Label Encoder')
        le = preprocessing.LabelEncoder()
        for i in df:
            le.fit(df[i])
            df[i] = le.transform(df[i])

        # Separando dados
        print('Separando dados')
        X = df.drop([self.label], axis=1)
        y = df[self.label]
        le.fit(y)
        y = le.transform(y)

        # Dados desbalanceados
        print('Dados desbalanceados')
        hist_df_1 = self.graph.hist_df(df, self.label, 'Distribuição dos dados originais', '1')
        X_rus, y_rus, id_rus, hist_df_2 = self.under_resampling(X, y)

        hist_df_1 = ['<h3>Distribuição de dados</h3><p>Distribuição inicial dos dados:</p>', hist_df_1]
        hist_df_2 = ['<p>Distribuição dos dados após realizar o balanceamento com UnderSampling:</p>', hist_df_2]

        return df, (X, y), (X_rus, y_rus, id_rus), (hist_df_1, hist_df_2)

    def under_resampling(self, X, y):
        rus = RandomUnderSampler(return_indices=True)
        X_rus, y_rus, id_rus = rus.fit_sample(X, y)
        df_rus = pd.concat([pd.DataFrame(X_rus), pd.DataFrame(y_rus, columns=['y'])], axis=1)
        return X_rus, y_rus, id_rus, self.graph.hist_df(df_rus, 'y', 'Distribuição dos dados balanceados', '2')

    def split(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        return X_train, X_test, y_train, y_test