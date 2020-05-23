# Out of bag evaluation

import pickle

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score as accuracy
from sklearn.preprocessing import LabelEncoder

from classifier_BERT.model import Bert_Model
from classifier_elmo.model import ElmoClassifier
from classifier_handcrafted_features.model import HandcraftedFeatures
from plots.plot_deep_models import plot
from utils.data import select_columns

plt.style.use('ggplot')

targets = ['Book relevance', 'Type', 'CategoryBroad']

results = []
for t in targets:
    print('Evaluating on target:', t)

    train_X, train_y, test_X, test_y = select_columns(x=['Message', 'Translation', 'Topic'], y=t)
    enc = LabelEncoder()
    enc.fit(train_y.values)
    test_y = enc.transform(test_y.values)

    print('Baseline')
    rf = HandcraftedFeatures('RF', target=t)
    rf.fit(train_X[['Message', 'Topic']], train_y)
    pred_rf = enc.transform(rf.predict(test_X[['Message', 'Topic']]))

    print('ELMo')
    elmo = ElmoClassifier('RF', target=t)
    elmo.fit(train_X[['Message', 'Topic']], train_y)
    pred_elmo = enc.transform(elmo.predict(test_X[['Message', 'Topic']]))

    print('BERT on Slovene messages')
    bert_slo = Bert_Model(t)
    bert_slo.fit(train_X, train_y)
    pred_bert_slo = bert_slo.predict(test_X)

    print('BERT on English messages')
    bert_eng = Bert_Model(t, True)
    bert_eng.fit(train_X, train_y)
    pred_bert_eng = bert_eng.predict(test_X)

    results.append([accuracy(test_y, pred_rf),
                    accuracy(test_y, pred_elmo),
                    accuracy(test_y, pred_bert_slo),
                    accuracy(test_y, pred_bert_eng)])

results = pd.DataFrame(results, columns=['RF', 'ELMo'])
results.index = targets

pickle.dump(results, open('../results/results_deep_models', 'wb+'))

plot()