# https://www.kaggle.com/bminixhofer/speed-up-your-rnn-with-sequence-bucketing
import torch
from torch import nn
from torch.utils import data
import torch.utils.data
from torch.nn import functional as F

from data_load import x_train, y, _len

# class SimpleCustomBatch:
#     def __init__(self, data):
#         transposed_data = list(zip(*data))
#         self.inp = torch.stack(transposed_data[0], 0)
#         self.tgt = torch.stack(transposed_data[1], 0)
#
#     def pin_memory(self):
#         self.inp = self.inp.pin_memory()
#         self.tgt = self.tgt.pin_memory()
#         return self
#
#
# def collate_wrapper(batch):
#     return SimpleCustomBatch(batch)
#
#
# inps = torch.arange(10 * 5, dtype=torch.float32).view(10, 5)
# tgts = torch.arange(10 * 5, dtype=torch.float32).view(10, 5)
#
# dataset = data.TensorDataset(inps, tgts)
# loader = data.DataLoader(dataset, batch_size=2, collate_fn=collate_wrapper,
#                          pin_memory=True)
# loader2 = data.DataLoader(dataset, batch_size=2)
# for batch_ndx, sample in enumerate(loader):
#     print(sample.inp.is_pinned())
#     print(sample.tgt.is_pinned())
#
#
# print(x_train, y)

import numpy as np
from keras.preprocessing.sequence import pad_sequences

"""
Method 1   分batch补 maxlen
"""

class TextDataset(data.Dataset):
    def __init__(self, text, lens, y=None):
        self.text = text
        self.lens = lens
        self.y = y

    def __len__(self):
        return len(self.lens)

    def __getitem__(self, idx):
        if self.y is None:
            return self.text[idx], self.lens[idx]
        return self.text[idx], self.lens[idx], self.y[idx]


# print(np.max(np.array(_len)))
MAX_LEN = 100


class Collator(object):
    def __init__(self, test=False, percentile=100):
        self.test = test
        self.percentile = percentile

    def __call__(self, batch):
        global MAX_LEN

        if self.test:
            texts, lens = zip(*batch)
        else:
            texts, lens, target = zip(*batch)

        lens = np.array(lens)
        max_len = min(int(np.percentile(lens, self.percentile)), MAX_LEN)
        texts = torch.tensor(pad_sequences(texts, maxlen=max_len), dtype=torch.long)

        if self.test:
            return texts

        return texts, torch.tensor(target, dtype=torch.float32)

# batch_size = 8
# train_collate = Collator(percentile=100)
# train_dataset = TextDataset(x_train, _len, y.numpy())
#
# train_loader = data.DataLoader(train_dataset, batch_size=batch_size,
#                                collate_fn=train_collate)
#
# for x, y in train_loader:
#     print(x.shape)


"""
Mehthod 2
"""
# import math
#
#
# class SequenceDataset(data.Dataset):
#     def __init__(self, sequences, choose_length, other_features=None, labels=None,
#                  indices=None, shuffle=False, batch_size=512):
#         super(SequenceDataset, self).__init__()
#
#         self.sequences = np.array(sequences)
#         self.lengths = np.array([len(x) for x in sequences])
#         self.n_samples = len(sequences)
#         self.choose_length = choose_length
#         self.other_features = other_features
#         self.labels = labels
#
#         if indices is not None:
#             self.indices = indices
#         else:
#             self.indices = np.arange(len(sequences))
#
#         self.batch_size = batch_size
#         self.shuffle = shuffle
#
#         if self.shuffle:
#             self._shuffle()
#
#     def __len__(self):
#         return math.ceil(len(self.indices) / self.batch_size)
#
#     def _shuffle(self):
#         self.indices = np.random.permutation(self.indices)
#
#     def __getitem__(self, i):
#         idx = self.indices[(self.batch_size * i):(self.batch_size * (i + 1))]
#
#         if self.shuffle and i == len(self) - 1:
#             self._shuffle()
#
#         pad_length = math.ceil(self.choose_length(self.lengths[idx]))
#         padded_sequences = pad_sequences(self.sequences[idx], maxlen=pad_length)
#
#         x_batch = [torch.tensor(padded_sequences, dtype=torch.long)]
#
#         if self.other_features is not None:
#             x_batch += [x[idx] for x in self.other_features]
#
#         if self.labels is not None:
#             out = x_batch, self.labels[idx]
#         else:
#             out = x_batch
#
#         return out
#
#
# batch_size = 8
# train_dataset = SequenceDataset(x_train, lambda _len: _len.max(),
#                                 other_features=[_len], shuffle=False,
#                                 batch_size=batch_size)
# train_loader = data.DataLoader(train_dataset, batch_size=1, shuffle=False)
#
# for x in train_loader:
#     print(len(x))
#     print(x)

"""
Mehtod 3   根据每个batch的最大length 切分 
"""

lengths = torch.from_numpy(np.array([len(x) for x in x_train]))
maxlen = lengths.max()
print(maxlen)
x_train_padded = torch.from_numpy(pad_sequences(x_train, maxlen=maxlen))
print(x_train_padded.shape)


class SequenceBucketCollator():
    def __init__(self, choose_length, sequence_index, length_index,
                 label_index=None):
        self.choose_length = choose_length
        self.sequence_index = sequence_index
        self.length_index = length_index
        self.label_index = label_index

    def __call__(self, batch):
        batch = [torch.stack(x) for x in list(zip(*batch))]

        sequences = batch[self.sequence_index]
        lengths = batch[self.length_index]

        length = self.choose_length(lengths).long()
        mask = torch.arange(start=maxlen, end=0, step=-1) < length

        print(sequences.shape)
        padded_sequences = sequences[:, mask]

        batch[self.sequence_index] = padded_sequences

        if self.label_index is not None:
            return [x for i, x in enumerate(batch) if i != self.label_index], batch[
                self.label_index]

        return batch


# batch_size = 8
# dataset = data.TensorDataset(x_train_padded, lengths, y)
# train_loader = data.DataLoader(dataset, batch_size=batch_size,
#                                collate_fn=SequenceBucketCollator(lambda x: x.max(), 0, 1, 2))

# for x, y in train_loader:
#     print(x[0].shape)

a = torch.arange(50).reshape(5, 10)
mask = torch.arange(50, 40, -1) < torch.tensor([45], dtype=torch.long)
print(mask)
print(a, a.shape)
print(a[:, mask])

"""
Method 2,3 比1 快
"""
