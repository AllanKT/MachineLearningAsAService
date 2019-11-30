import threading
from datetime import datetime

from training.models.knn.model import KNN
from training.models.naive_bayes.model import NaiveBayes
from training.models.svm.model import SVM
from training.models.graph import Graph

from utils.mail import Mail
from utils.s3 import S3
from settings.configuration import Configuration


def worker(index, results, algorithm, model, X_train, X_test, y_train, y_test):
    print(f"start train from {algorithm} model")
    train = model.train(X_train, y_train, X_test, y_test)
    classifier = model.fit(X_train, y_train)
    accuracy, y_pred = model.accuracy(classifier, y_test, X_test)
    print(f"Accuracy {algorithm}: ", accuracy)

    graph = Graph(algorithm)
    conf_matrix = graph.conf_matrix(y_test, y_pred)
    print(train)
    train[0] + f"""<p>A acuracia do treinamento deste modelo ficou com uma margem de {accuracy}.</p>""" 

    return {
        "algorithm": algorithm,
        "accuracy": accuracy,
        "images": {
            algorithm: [train[0] + f"""<p>A acuracia do treinamento deste modelo ficou com uma margem de {accuracy}.</p>""", train[1]],
            "confusion matrix": [f"<p>A matriz de confusão para o treino do modelo está apresentada abaixo:</p>", conf_matrix]
        }
    }

def run(process, X_train, X_test, y_train, y_test):
    knn, svm, nb = KNN(), SVM(), NaiveBayes()
    models = {
        "knn": knn,
        "svm": svm,
        "nb": nb
    }

    threads = list()
    results = [None]*4
    results[0] = process

    i = 1
    for key, model in models.items():
        print("Main    : create and start thread %d.", model)
        results.append(worker(i, results, key, model, X_train, X_test, y_train, y_test))
    #     x = threading.Thread(
    #         target=worker,
    #         args=(i, results, key, model, X_train, X_test, y_train, y_test,)
    #     )
    #     i+=1
    #     threads.append(x)
    #     x.start()

    # for index, thread in enumerate(threads):
    #     print("Main    : before joining thread %d.", index)
    #     thread.join()
    #     print("Main    : thread %d done", index)

    print(results)

    config = Configuration()
    mail = Mail(config.MAIL_USERNAME, config.MAIL_PASSWORD, config.MAIL_SERVER, config.MAIL_PORT)
    s3 = S3(config.BUCKET_NAME, config.ACCESS_KEY, config.SECRET_KEY)

    date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    for data in results:
        if data is not None:
            for key, info in data['images'].items():
                if info[1] is not None:
                    name = info[1].split("\\")[-1]
                    s3.upload_s3(info[1], f"{date}/{name}")

    subject, body = mail.content(results)
    print(subject)
    print(body)
    print(config.MAIL_FROM, config.MAIL_CC, subject, body)
    mail.send_email(config.MAIL_FROM,'allankltsn@gmail.com', subject, body, results)
    print('email enviado com sucesso')
