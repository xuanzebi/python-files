import pandas as pd
from keras.preprocessing import text, sequence
from keras.preprocessing.sequence import pad_sequences
import jieba
import numpy as np
import torch
from torch import nn
from torch.utils import data
import torch.utils.data
from torch.nn import functional as F


def preprocess(text):
    """Sentence tokenization."""
    words = jieba.lcut_for_search(text)
    return words


train = pd.read_csv('./test.csv')
train['content'] = train['content'].apply(preprocess)
tokenizer = text.Tokenizer()
tokenizer.fit_on_texts(train['content'])

x_train = tokenizer.texts_to_sequences(train['content'])

_len = np.array([len(x) for x in x_train])
# print(_len)
# x_train = np.array(pad_sequences(x_train, maxlen=100))

y = torch.empty(np.array(x_train).shape[0], dtype=torch.long).random_(2)
# print(y)
#
#
# print(y.shape)