import itertools
import numpy as np


class KLDivergence:
    def __init__(self, band_matrix, QID_select, SD_groups, group_list, SD_items, Cells):
        """

        :param band_matrix: The square matrix we get from RCM calculation
        :param QID_select: r number of selected QID items a.k.a QID_subset
        :param SD_groups: Groups that have sensitive item
        :param group_list: All Formed groups
        :param SD_items: All sensitive items
        :param Cells: all possible int(n) cell combinations, n=4 -> [0000], [1000], [0100], ...
        """
        self.band_matrix = band_matrix
        self.QID_select = QID_select
        self.SD_groups = SD_groups
        self.group_list = group_list
        self.SD_items = SD_items
        self.Cells = Cells

    @staticmethod
    def get_all_combinations_of_QID_subset(n):
        """
        compute all possible combination of n in CELL, n=4 -> [0000], [1000], ...
        :param n: number of items in QID subset
        :return lst: all possible combinations of n value
        """
        lst = [list(i) for i in itertools.product([0, 1], repeat=n)]
        return lst

    def calculate_act(self, cell, SD_item):
        """
        Function for computing the actual probability distribution given the sensitive item s
        for a specific cell C
        :param cell: A single one of int(n) cell combinations, n=4 -> [0000], [1000], [0100], ...
        :param SD_item: Sensitive item label (column name), or it could be a list of SD items
        :return:
        """

        # number of occurrences s in T(all dataset)
        # if sensitive items is single
        row_sensitive = list()

        if type(SD_item) is str:

            # indices of rows(transactions) that have sensitive items
            row_sensitive = self.band_matrix[self.band_matrix[SD_item] == 1].index.tolist()
            # print(f"ROW SENSITIVE index: {row_sensitive}, SDs:{self.band_matrix[self.band_matrix[SD_item] == 1]}")
            number_s_t = len(row_sensitive)
            set_row = set(row_sensitive)
            # control all values
            for i in range(0, len(self.QID_select)):
                set_temp = self.band_matrix[self.band_matrix[self.QID_select[i]] == cell[i]].index.tolist()
                set_temp = set(set_temp)
                # check the intersection
                set_row = set_row.intersection(set_temp)
                # number of occurrences of s in C (where QID_list conditions are true)
            number_s_c = len(set_row)
            if number_s_t > 0:
                return number_s_c / number_s_t
            else:
                # print("##################### fail ######################")
                return 0
        elif type(SD_item) is list:
            occurrence_list = list()
            for s in SD_item:
                value = self.calculate_act(cell, s)
                occurrence_list.append(value)
            return occurrence_list
        else:
            # print("##################### fail list ######################")
            return 0

    def calculate_est(self, cell, SD_item):
        """
        Function for computing the actual probability distribution given the sensitive item s
        for a specific cell C

        a * b / |G|
         where "a" is the number of sensitive items in group G
         b the number of transitions that match the QIDs in the group
         |G| is the cardinality of the group
         and calculate with all the groups that intersect cell C
        :param cell: A single one of int(n) cell combinations, n=4 -> [0000], [1000], [0100], ...
        :param SD_item: Sensitive item label (column name), or it could be a list of SD items
        :return:
        """
        value_tot = 0
        # for each group, look for the cells that match the condition

        for index in range(0, len(self.group_list)):
            cardinality_G = len(self.group_list[index])
            set_row = set(self.group_list[index].index.tolist())

            for i in range(0, len(self.QID_select)):
                set_temp = self.group_list[index][self.group_list[index][self.QID_select[i]] == cell[i]].index.tolist()
                set_temp = set(set_temp)
                # check intersection
                set_row = set_row.intersection(set_temp)
                # number of occurrences of s in C (where QID_list conditions are true)

            # value B for index group
            value_b = len(set_row)
            # sensitive item number in the index group
            value_a = self.SD_groups[index][SD_item]
            value_tot = value_tot + ((value_a * value_b) / cardinality_G)

        row_sensitive = self.band_matrix[self.band_matrix[SD_item] == 1].index.tolist()
        number_s_t = len(row_sensitive)
        if number_s_t > 0:
            value_tot = value_tot / number_s_t
        else:
            value_tot = 0
        return value_tot

    def compute_KLDivergence_value(self):
        """
        Function for calculating the KLDivergence value

        :return: KL_Divergence value, float
        """
        print(f"SD_items: {self.SD_items}")
        KL_Divergence = 0
        for sd in self.SD_items:
            # for each sd in SD subset, calculate ACT and EST for KL Divergence
            temp_KLD = 0
            for cell in self.Cells:
                act = self.calculate_act(cell, sd)
                est = self.calculate_est(cell, sd)

                if act > 0 and est > 0:
                    temp = act * np.log(act / est)
                else:
                    temp = 0

                # temp_KLD is just for printing KLD value per sensitive item
                temp_KLD += temp
                KL_Divergence += temp
            print(f"KLDivergence: {temp_KLD} Sensitive Item: {sd}")

        return KL_Divergence
