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
    SD_group = None  # list of sensitive items associated with groups
    QID_items = None  # list of quasi identifiers

    def __init__(self, band_matrix, sensitive_items, p_degree, alpha_=4):
        self.original_dataframe = band_matrix.copy()
        self.sensitive_items = sensitive_items
        self.p_degree = p_degree
        self.alpha_ = alpha_
        self.QID_items = [i for i in list(self.original_dataframe) if i not in self.sensitive_items]

    def compute_hist(self):
        # call band matrix
        # get the hist of sensitive items
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

    def anonymize(self):
        pass


if __name__ == "__main__":
    pass
