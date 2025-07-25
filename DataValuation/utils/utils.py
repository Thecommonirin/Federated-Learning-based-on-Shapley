import numpy as np
import torch
import torch.nn as nn
import random


def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

def model_name(args, src, tgt):

    ext_n = str(args.model)
    ds_n = 'DeepSets'
    ext_n += '_' + str(args.n_owners) + 'o' + str(args.data_size) + 's_' + str(12347)
    ds_n += '_' + str(args.n_owners) + 'o' + str(args.data_size) + 's_' + str(12347)
    if args.noisey:
        ext_n += '_' + str(args.prob_hold) + 'noisey_' + str(12347)
        ds_n += '_' + str(args.prob_hold) + 'noisey_' + str(12347)
    ext_n += '.pth'
    ds_n += '.pth'
    return ext_n, ds_n

def collect_from_loader(dataloaders):
    src_loader, tgt_loader = dataloaders
    x, y = [], []
    if src_loader is None:
        for (image, label) in iter(tgt_loader):
            x.append(image)
            y.append(label)

    else:
        for (image, label) in iter(src_loader):
            x.append(image)
            y.append(label)
    data = (torch.cat(x), torch.cat(y))
    return data

def array_to_lst(X_feature):
    if type(X_feature) == list:
        return X_feature

    X_feature = list(X_feature)
    for i in range(len(X_feature)):
        X_feature[i] = X_feature[i].nonzero()[0]
    return X_feature


def featureExtract_cycda(x, ext):
    score, out = ext(x, with_ft=True)
    return out.view(out.size(0), -1)


def featureExtract_cycday(x, y, ext):
    x = x.cuda()
    y = y.cuda()
    score, out = ext(x, y, with_ft=True)
    return out.view(out.size(0), -1)


def sample_count(n_select, n_owners, ub_prob):
    toss = np.random.uniform()
    alpha = np.ones(n_owners) * 5
    p = np.random.dirichlet(alpha=alpha)
    data_for_each_owner = np.random.multinomial(n_select, p, 1)[0]

    return data_for_each_owner


def val_to_dataind(v):
    one_hot = np.array([int(x) for x in bin(v)[2:]])[::-1]
    return one_hot.nonzero()[0]


def dataind_to_val(arr):
    val = 0
    for i in arr:
        val += 2 ** i
    return val


class SiLU_(nn.Module):
    def forward(self, x):
        return 1 / 2 * x + 1 / 4 * x ** 2


class Square(nn.Module):
    def forward(self, x):
        return x ** 2


class Flatten(nn.Module):
    def forward(self, x):
        return x.view(x.size(0), -1)


def metric(accuracy, r_accuracy, percentage, low2high=True):
    if low2high:
        score = accuracy - r_accuracy
    else:
        score = r_accuracy - accuracy
    return np.sum(score * percentage)

