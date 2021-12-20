import operator
import time
from band_matrix import compute_band_matrix, logger

import numpy as np
import pandas as pd


class CAHD:
    original_dataframe = None  # copia del dataframe bandizzato
    id_sensitive_transaction = None  # list of sensitive transactions id
    band_matrix = None  # banded matrix, output of RCM
    sensitive_items = None  # list of sensitive items
    p_degree = None  # privacy degree
    alpha_ = None
    hist = None  # histogram of sensitive data frequencies
    group_dict = None  # dictionary for binding groups and sensitive data
    group_list = None  # list of anonymization groups
    SD_groups = None  # list of sensitive items associated with groups
    QID_items = None  # list of quasi identifiers

    def __init__(self, band_matrix, sensitive_items, p_degree, alpha_=4):
        self.original_dataframe = band_matrix.copy()
        self.band_matrix = band_matrix
        self.sensitive_items = sensitive_items
        self.p_degree = p_degree
        self.alpha_ = alpha_
        self.QID_items = [i for i in list(self.original_dataframe) if i not in self.sensitive_items]

    def compute_hist(self):
        # call band matrix
        # get the hist of sensitive items
        logger('band matrix', self.band_matrix)
        logger('sensitive items', self.sensitive_items)

        self.hist = dict(self.band_matrix[self.sensitive_items].sum())
        return self.hist

    def check_conflict(self, row_i, position_j):
        # function for checking any sensitive items in conflict in the same group
        # if there are sensitive items in common, there is conflict
        row_j = list(self.band_matrix.iloc[position_j][self.sensitive_items])
        for position in range(len(self.sensitive_items)):
            if row_i[position] + row_j[position] > 1:
                return True
        return False

    # def check_conflict(self, row_i, row_j):
    # function for checking any sensitive items in conflict in the same group
    # if there are sensitive items in common, there is conflict
    #     sensitive_data_row_i = self.sensitive_items[np.where(self.band_matrix.iloc[row_i][self.sensitive_items] == 1)]
    #     sensitive_data_row_i = self.sensitive_items[np.where(self.band_matrix.iloc[row_j][self.sensitive_items] == 1)]
    #     # create set
    #     set_j = set(sensitive_data_row_i)
    #     set_i = set(sensitive_data_row_i)
    #     # check intersection
    #     return len(set_i.intersection(set_j)) > 0

    # function for checking the final validity state of the group
    # mainly for reducing the code redundancy in compute_candidate_list function
    def check_list(self, i, idx_sensitive_transaction, k, candidate_list):
        row_i = list(self.band_matrix.iloc[i][self.sensitive_items])
        if self.check_conflict(row_i, idx_sensitive_transaction):
            k = k + 1
        else:
            conflict_list = False
            for index in candidate_list:
                if self.check_conflict(row_i, index):
                    conflict_list = True
                    break
            if not conflict_list:
                candidate_list.append(i)
            else:
                k = k + 1
        return k

    def select_best_transactions(self, candidate_list, transaction_target):
        distance = list()
        list_1 = self.band_matrix.iloc[transaction_target][self.QID_items]
        for row in candidate_list:
            list_2 = self.band_matrix.iloc[row][self.QID_items]
            similarity = [(i and j) for i, j in zip(list_1, list_2)]
            distance.append(sum(similarity))

        best_rows = list()
        for i in range(self.p_degree - 1):
            max_index, max_value = max(enumerate(distance), key=operator.itemgetter(1))
            best_rows.append(candidate_list[max_index])
            distance[max_index] = -1
        return best_rows

    # calculate the list of candidate groups
    def compute_candidate_list(self, idx_sensitive_transaction):
        alpha_p = self.alpha_ * self.p_degree
        candidate_list = list()
        k = 1
        i = idx_sensitive_transaction - 1
        while i > max(idx_sensitive_transaction - alpha_p - k, -1):
            k = self.check_list(i, idx_sensitive_transaction, k, candidate_list)
            i -= 1

        k = 1
        i = idx_sensitive_transaction + 1
        while i < min(idx_sensitive_transaction + alpha_p + k, len(self.band_matrix)):
            k = self.check_list(i, idx_sensitive_transaction, k, candidate_list)
            i += 1
        error = False
        if len(candidate_list) < self.p_degree:
            error = True
        return candidate_list, error

    def create_groups(self):
        # compute histogram of sensitive items
        self.compute_hist()
        # candidate_list = dict()
        self.id_sensitive_transaction = self.band_matrix.iloc[
            list(set(list(np.where(self.band_matrix[self.sensitive_items] == 1)[0])))].index
        group_dict = list()
        group_list = list()
        sd_groups = list()

        for att in range(1):
            id_sensitive_transaction = np.random.permutation(self.id_sensitive_transaction)
            remaining = len(self.band_matrix)
            ts_idx = 0  # sensitive transaction index
            while ts_idx < len(id_sensitive_transaction):
                q = id_sensitive_transaction[ts_idx]
                t = self.band_matrix.index.get_loc(q)
                candidate_list, error = self.compute_candidate_list(t)
                if not error:
                    group = self.select_best_transactions(candidate_list, t)
                    group.append(t)

                    # update histogram
                    selected_sensitive_items = self.band_matrix.iloc[group][self.sensitive_items].sum()
                    temp_hist = self.hist.copy()
                    for idx in selected_sensitive_items.index:
                        temp_hist[idx] -= selected_sensitive_items.loc[idx]

                    # check formation of group or the creation of the last group
                    th_max = max(temp_hist.values())
                    if th_max * self.p_degree > remaining - len(group):
                        ts_idx += 1
                    else:
                        self.hist = temp_hist.copy()
                        group_label = self.band_matrix.iloc[group].index
                        id_sensitive_transaction = [i for i in id_sensitive_transaction if i not in group_label]

                        group_dict.append(self.band_matrix.index[group])
                        group_list.append(
                            self.band_matrix.loc[list(self.band_matrix.index[group]), self.QID_items])

                        sd_groups.append(selected_sensitive_items)

                        self.band_matrix = self.band_matrix.drop(
                            list(self.band_matrix.index[group]))

                        remaining = len(self.band_matrix.index)
                else:
                    ts_idx += 1
            # create the last group and update data structures
            selected_sensitive_items = self.band_matrix[self.sensitive_items].sum()
            max_v = max(dict(selected_sensitive_items).values())
            if max_v * self.p_degree <= len(self.band_matrix):
                group_list.append(self.band_matrix[self.QID_items])
                group_dict.append(self.band_matrix.index)
                sd_groups.append(selected_sensitive_items)
                self.band_matrix = None
                self.SD_groups = sd_groups
                self.group_list = group_list
                self.group_dict = group_dict
                return True
        return False


# if __name__ == "__main__":
#     df = pd.read_csv('./Dataset/BMS1_table.csv', index_col=False)
#     df_square, items, sensitive_items = compute_band_matrix(dataset=df, bm_size=487, num_sensitive=10, plot=True)
#     print(df_square.shape)
#
#     cahd = CAHD(band_matrix=df_square, sensitive_items=sensitive_items, p_degree=4, alpha_=4)
#     cahd.create_groups()
#     print(cahd.group_dict)
