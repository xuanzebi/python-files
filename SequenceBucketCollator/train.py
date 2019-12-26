import torch
from torch import nn
from torch.utils import data
import torch.utils.data
from torch.nn import functional as F
from keras.preprocessing.sequence import pad_sequences

from sequencemodel1 import LenMatchBatchSampler
from data_load import x_train, y

maxlen = 64
x_train_padded = torch.from_numpy(pad_sequences(x_train, maxlen=maxlen))
batch_size = 64
train_dataset = data.TensorDataset(torch.tensor(x_train_padded, dtype=torch.long),
                                   torch.tensor(y, dtype=torch.float))

# 产生分batch的 indices
# batch_samper = data.BatchSampler(ran_sampler, batch_size=64,drop_last=False)
# train_dataset2 = data.TensorDataset(torch.tensor(x_train, dtype=torch.long),
#                                     torch.tensor(y, dtype=torch.float))
# train_loader2 = data.DataLoader(train_dataset, sampler=ran_sampler, batch_size=64)

from tqdm import tqdm


ran_sampler = data.RandomSampler(train_dataset)
len_sampler = LenMatchBatchSampler(ran_sampler, batch_size=batch_size, drop_last=False)

"""
batch_sampler 返回数据的indices  collate_fn 返回数据
"""
train_loader = data.DataLoader(train_dataset, batch_sampler=len_sampler)
tk0 = tqdm(enumerate(train_loader), total=len(train_loader), leave=False)

# for i, batch in tk0:
#     x_batch, y_batch = tuple(t for t in batch)
#     print(x_batch, y_batch)

print('````````````````````')
import torch

for x, y in train_loader:
    cc = []
    for i in x:
        count_zeros = torch.sum(i == 0)
        cc.append(count_zeros)
    print(cc)
    # print(x, y)
