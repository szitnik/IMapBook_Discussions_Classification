"""
File for functions for retrieving data.
"""

import pandas as pd
import yaml
from sklearn.model_selection import KFold


def get_data():
    return pd.read_excel('../data/imapBook/AllDiscussionDataCODED_USE_THIS_14Feb2020_MH.xls')


def split_train_test(x, y, split=0.8):
    split = int(len(x) * split)
    xtrain = x.iloc[:split]
    ytrain = y.iloc[:split]
    xtest = x.iloc[split:]
    ytest = y.iloc[split:]
    return xtrain, ytrain, xtest, ytest


def select_columns(x=('Message', 'Topic'), y='Book relevance', shuffle=True, *, correct_typos=False):
    data = get_data()
    data[y] = data[y].astype('category')
    data = data.dropna(subset=list(x) + [y])
    if shuffle:
        data = data.sample(frac=1, random_state=0)
    data = data.reset_index(drop=True)
    x = data.loc[:, x]
    y = data.loc[:, y]

    if correct_typos:
        replace_with_corrected_typos(x)

    return split_train_test(x, y)


def kfolds(x=('Message', 'Topic'), y='Book relevance', k=5, shuffle=True, *, correct_typos=False):
    assert k >= 1
    if k == 1:
        yield select_columns(x, y, shuffle, correct_typos=correct_typos)
        return

    data = get_data()
    data = data.dropna(subset=list(x) + [y])
    if shuffle:
        data = data.sample(frac=1, random_state=0)
    data = data.reset_index(drop=True)
    x = data.loc[:, x]
    y = data.loc[:, y].astype('category')

    if correct_typos:
        replace_with_corrected_typos(x)

    kf = KFold(n_splits=k, shuffle=shuffle, random_state=0)
    for train_index, test_index in kf.split(x):
        xtrain, xtest = x.iloc[train_index], x.iloc[test_index]
        ytrain, ytest = y.iloc[train_index], y.iloc[test_index]
        yield xtrain, ytrain, xtest, ytest


def replace_with_corrected_typos(data):
    messages = yaml.load(open('../data/messages_without_typos.yaml'), yaml.Loader)

    for i in range(data.shape[0]):
        m = str(data['Message'].iloc[i])
        assert m in messages
        data['Message'].iloc[i] = ' '.join(messages[m]['corrected'])


if __name__ == '__main__':
    # example:
    xtrain, ytrain, xtest, ytest = select_columns()
    print("Data imported")
