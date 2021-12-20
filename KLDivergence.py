import itertools
from band_matrix import logger


def compute_act_s_in_c(band_matrix, QID_list, QID_values, sensitive_items):
    """
    Function for computing the probability distribution given the sensitive item s
    for a specific cell C
    :param band_matrix:
    :param QID_list:
    :param QID_values:
    :param sensitive_items:
    :return:
    """

    # number of occurrences s in T(all dataset)
    # if sensitive items is single
    row_sensitive = list()

    if type(sensitive_items) is str:
        print("computing act s in c")
        logger("type(sensitive_items) TRUE", row_sensitive)
        logger("band_matrix[band_matrix[sensitive_items] == 1]",type(band_matrix[band_matrix[sensitive_items] == 1].index.tolist()[0]))

        row_sensitive = band_matrix[band_matrix[sensitive_items] == 1].index.tolist()
        # break
        number_s_t = len(row_sensitive)
        set_row = set(row_sensitive)
        # control all values
        for i in range(0, len(QID_list)):
            set_temp = band_matrix[band_matrix[QID_list[i]] == QID_values[i]].index.tolist()
            set_temp = set(set_temp)
            # check the intersection
            set_row = set_row.intersection(set_temp)
            # number of occurrences of s in C (where QID_list conditions are true)
        number_s_c = len(set_row)
        if number_s_t > 0:
            return number_s_c / number_s_t
        else:
            return 0
    elif type(sensitive_items) is list:
        occurrence_list = list()
        for s in sensitive_items:
            value = compute_act_s_in_c(band_matrix, QID_list, QID_values, s)
            occurrence_list.append(value)
        return occurrence_list
    else:
        return 0


def compute_est_s_in_c(band_matrix, SD_groups, groups_list, QID_list, QID_values, sensitive_items):
    """
    a * b / |G|
     where "a" is the number of sensitive items in group G
     b the number of transitions that match the QIDs in the group
     |G| is the cardinality of the group
     and calculate with all the groups that intersect cell C
    """
    value_tot = 0
    # for each group, look for the cells that match the condition
    # print("len",len(groups_list))

    for index in range(0, len(groups_list)):
        cardinality_G = len(groups_list[index])
        set_row = set(groups_list[index].index.tolist())
        for i in range(0, len(QID_list)):
            set_temp = groups_list[index][groups_list[index][QID_list[i]] == QID_values[i]].index.tolist()
            set_temp = set(set_temp)
            # check intersection
            set_row = set_row.intersection(set_temp)
            # number of occurrences of s in C (where QID_list conditions are true)

        # value B for index group
        value_b = len(set_row)
        # print("b",value_b)
        # sensitive item number in the index group
        value_a = SD_groups[index][sensitive_items]
        # print("a",value_a)
        value_tot = value_tot + ((value_a * value_b) / cardinality_G)

    row_sensitive = band_matrix[band_matrix[sensitive_items] == 1].index.tolist()
    number_s_t = len(row_sensitive)
    if number_s_t > 0:
        value_tot = value_tot / number_s_t
    else:
        value_tot = 0
    return value_tot


def get_all_combination_of_n(n):
    """
    compute all possible combination of n bit
    :param n: number of QID items
    :return lst: all possible combinations of n value
    """
    lst = [list(i) for i in itertools.product([0, 1], repeat=n)]
    return lst
