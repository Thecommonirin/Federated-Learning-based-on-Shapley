import torch
from scipy.special import comb
import numpy as np

from utils.utils import val_to_dataind, utility_score, utility_score_y
from proxy_models import cnn_data_to_acc, logistic_data_to_acc


def comb_shapley_exactly(data, data_test, score_dict, target_ind):
    data_owner_X, data_owner_y = data
    n_data = len(data_owner_X)

    sv = 0
    for v in range(1, 2 ** n_data):
        ind_set = val_to_dataind(v)
        if target_ind in ind_set:
            pass
        else:
            s = len(ind_set)
            train_X = torch.vstack([data_owner_X[i] for i in ind_set])
            train_y = torch.hstack([torch.tensor(data_owner_y[i]) for i in ind_set])

            if str(set(ind_set)) not in score_dict.keys():
                acc_without = cnn_data_to_acc(train_X, train_y, data_test)
                score_dict[str(set(ind_set))] = acc_without
            else:
                acc_without = score_dict[str(set(ind_set))]

            v_sand = list(ind_set) + [target_ind]
            train_X = torch.vstack([data_owner_X[i] for i in v_sand])
            train_y = torch.hstack([torch.tensor(data_owner_y[i]) for i in v_sand])
            if str(set(v_sand)) not in score_dict.keys():
                acc_with = cnn_data_to_acc(train_X, train_y, data_test)
                score_dict[str(set(v_sand))] = acc_with
            else:
                acc_with = score_dict[str(set(v_sand))]

            weight = 1 / n_data * (1 / comb(n_data - 1, s))
            sv += weight * (acc_with - acc_without)

    return sv, score_dict


def comb_shapley_uf(data, extractor, deepset, score_dict, target_ind):
    """
    By Utility function
    """
    data_owner_X, data_owner_y = data
    n_data = len(data_owner_X)

    sv = 0
    for v in range(1, 2 ** n_data):
        team_without = val_to_dataind(v).tolist()
        if target_ind in team_without:
            pass
        else:
            s = len(team_without)
            if str(set(team_without)) not in score_dict.keys():
                train_X = torch.cat([data_owner_X[i] for i in team_without])
                score_without = utility_score(train_X, extractor, deepset).cpu().data.numpy()[0]
                score_dict[str(set(team_without))] = score_without
            else:
                score_without = score_dict[str(set(team_without))]

            team_with = list(team_without) + [target_ind]
            if str(set(team_with)) not in score_dict.keys():
                train_X = torch.vstack([data_owner_X[i] for i in team_with])
                score_with = utility_score(train_X, extractor, deepset).cpu().data.numpy()[0]
                score_dict[str(set(team_with))] = score_with
            else:
                score_with = score_dict[str(set(team_with))]

            weight = 1 / n_data * (1 / comb(n_data - 1, s))
            sv += weight * (score_with - score_without)

    return sv, score_dict


def shapley_sampling(data, data_test, score_dict, target_ind):
    """
    sampling method for exactly sv
    """
    data_owner_X, data_owner_y = data
    n_data = len(data_owner_X)
    marginal_value = []
    n_sample = int(n_data * np.log(n_data))

    for _ in range(n_sample):
        perm = np.random.permutation(range(n_data))

        i = (perm == target_ind).nonzero()[0][0]
        if i == 0:
            continue

        team_without = perm[:i]
        if str(set(team_without)) not in score_dict.keys():
            train_X = torch.vstack([data_owner_X[i] for i in team_without])
            train_y = torch.hstack([data_owner_y[i] for i in team_without])
            score_without = logistic_data_to_acc(train_X, train_y, data_test)
            score_dict[str(set(team_without))] = score_without
        else:
            score_without = score_dict[str(set(team_without))]

        team_with = perm[:i + 1]
        if str(set(team_with)) not in score_dict.keys():
            train_X = torch.vstack([data_owner_X[i] for i in team_with])
            train_y = torch.hstack([data_owner_y[i] for i in team_with])
            score_with = logistic_data_to_acc(train_X, train_y, data_test)
            score_dict[str(set(team_with))] = score_with
        else:
            score_with = score_dict[str(set(team_with))]

        marginal_value.append(score_with - score_without)
    return np.average(marginal_value), score_dict


def perm_shapley_sampling(data, extractor, deepset, score_dict, target_ind):
    data_owner_X, data_owner_y = data
    n_data = len(data_owner_X)
    marginal_value = []
    n_sample = int(n_data * np.log(n_data))

    for _ in range(n_sample):
        perm = np.random.permutation(range(n_data))

        i = (perm == target_ind).nonzero()[0][0]
        if i == 0:
            continue

        team_without = perm[:i]
        if str(set(team_without)) not in score_dict.keys():
            train_X = torch.vstack([data_owner_X[i] for i in team_without])
            score_without = utility_score(train_X, extractor, deepset).cpu().data.numpy()[0]
            score_dict[str(set(team_without))] = score_without
        else:
            score_without = score_dict[str(set(team_without))]

        team_with = perm[:i + 1]
        if str(set(team_with)) not in score_dict.keys():
            train_X = torch.vstack([data_owner_X[i] for i in team_with])
            score_with = utility_score(train_X, extractor, deepset).cpu().data.numpy()[0]
            score_dict[str(set(team_with))] = score_with
        else:
            score_with = score_dict[str(set(team_with))]

        marginal_value.append(score_with - score_without)
    return np.average(marginal_value), score_dict


def get_shapley(n_owners, data_owner_X, data_owner_y, extractor, deepset, valid_data=None):
    shapley_value_exactly = np.zeros(n_owners)
    score_dict_exactly = {}

    for i in range(n_owners):
        shapley_value_exactly[i], score_dict_exactly = shapley_sampling((data_owner_X, data_owner_y),
                                                                            valid_data, score_dict_exactly, i)
    return shapley_value_exactly
