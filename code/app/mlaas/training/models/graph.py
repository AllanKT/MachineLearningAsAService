import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.metrics import confusion_matrix, accuracy_score


class Graph():
    def __init__(self, model):
        self.model = model
        self.path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'images',
            self.model
            )
        self.__mkdir_images_folder
        self.__mkdir_model_folder

    @property
    def __mkdir_images_folder(self):
        if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)),'images')):
            os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)),'images'))

    @property
    def __mkdir_model_folder(self):
        if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)),'images', self.model)):
            os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)),'images', self.model))

    def conf_matrix(self, y_test, y_pred):
        mat = confusion_matrix(y_test, y_pred)
        sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False)
        plt.xlabel('true label')
        plt.ylabel('predicted label')
        plt.savefig(os.path.join(self.path, f'{self.model}_confusion_matrix.png'))
        plt.close()
        return os.path.join(self.path, f'{self.model}_confusion_matrix.png')

    def hist_df(self, df, column, title, name):
        df[column].value_counts().plot(kind="bar")
        plt.title(title)
        plt.savefig(os.path.join(self.path, f'{self.model}_{name}_hist_df.png'))
        plt.close()
        return os.path.join(self.path, f'{self.model}_{name}_hist_df.png')

    def hist_dashed(self, hist, title, xlabel, ylabel, figsize, min, max):
        plt.figure(figsize=figsize)
        plt.plot(range(min, max), hist, color='red', linestyle='dashed',
            marker='o', markerfacecolor='blue', markersize=10)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(os.path.join(self.path, f'{self.model}_hist_dashed.png'))
        plt.close()
        return os.path.join(self.path, f'{self.model}_hist_dashed.png')
