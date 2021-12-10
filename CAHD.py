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



        pass

    def candidate_list(self):
        pass

    def anonymize(self):
        pass


if __name__ == "__main__":
    pass


