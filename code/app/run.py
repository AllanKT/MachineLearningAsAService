
# -*- coding: utf-8 -*- 



import importlib.util
import os, sys
import datetime
import time
from pprint import pprint
sys.path.append('./mlaas')
sys.path.append('./settings')
sys.path.append('./utils')

import warnings
warnings.filterwarnings("ignore")

from processing.process import Process
from training.train import run

from arguments import Arguments
# from log import logger
from configuration import Configuration

def main():
    config = Configuration()
    arg = Arguments()
    args = vars(arg.parser.parse_args())

    print("System is runing")

    try:
        file = args["file"]
        label = args["class"]
        sep = args["sep"]
        encoding = args["encoding"]
    except Exception as e:
        print(e)

    if file == None or label == None:
        print("All fields has been declared.")
        exit()

    processing = Process(file, sep, encoding, label)
    df = processing.read_csv
    df_train, (X, y), (X_rus, y_rus, id_rus), (hist_df_1, hist_df_2) = processing.clean(df)
    X_train, X_test, y_train, y_test = processing.split(X, y)

    data = {
        "images": {
            "hist_df_1": hist_df_1,
            "hist_df_2": hist_df_2
        }
    }

    run(data, X_train, X_test, y_train, y_test)


if __name__ == '__main__':
    main()