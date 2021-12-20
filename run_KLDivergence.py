import BandMatrix
import pandas as pd
from CAHD import CAHD
import time
import numpy as np
import KLDivergence
import random
from band_matrix import compute_band_matrix, logger

if __name__ == "__main__":
    bm_size = 1000  # band matrix size
    num_sensitive = 10  # number of sensitive items
    p_degree = 5  # the degree of privacy
    alpha = 3
    p_degree_list = [4, 6, 8, 10]
    KL_values = list()

    # load the data
    data_path = './Dataset/BMS1_table.csv'
    df = pd.read_csv(data_path, index_col=False)

    # get the start time to calculate execution time
    start_time = time.time()

    print("Calculating band matrix")
    df_square, items, sensitive_items = compute_band_matrix(dataset=df, bm_size=487, num_sensitive=10, plot=True)

    for privacy_degree in p_degree_list:
        # Apply CAHD algorithm to create
        cahd = CAHD(band_matrix=df_square, sensitive_items=sensitive_items, p_degree=p_degree, alpha_=alpha)
        print(cahd.group_dict)
        cahd.compute_hist()
        hist_item = cahd.hist
        print("Start Anonymization process")
        cahd.create_groups()
        end_time = time.time() - start_time
        print(f"Privacy-degree: {cahd.p_degree}\nTime required for creating the anonymized groups: {end_time}\n")

        r = 4
        QID = cahd.group_list[0].columns.tolist()
        logger("QID list", QID)
        QID_select = list()
        while len(QID_select) < r:
            temp = random.choice(QID)
            if temp not in QID_select:
                QID_select.append(temp)

        logger("QID select", QID_select)

        # computation of all combinations for cell C
        all_value = KLDivergence.get_all_combination_of_n(r)
        logger("KLD all combinations of n for cell C", all_value)

        # get the item with the most value from the histogram
        # change the item dtype to str because the column names(item names) in band matrix are str
        # otherwise they dont match and KL divergence calculation fails
        sensitive_item = str(max(hist_item.keys(), key=(lambda k: hist_item[k])))
        logger("Sensitive item, MAX VAL from histogram", sensitive_item)
        logger("DEBUG", type(df_square[df_square[sensitive_items] == 1].index.tolist()[0]))

        # calculate actsc and estsc  for KL Divergence
        KL_Divergence = 0

        for value in all_value:
            actsc = KLDivergence.compute_act_s_in_c(df_square, QID_select, value, sensitive_item)
            logger("ACTSC value", actsc)
            estsc = KLDivergence.compute_est_s_in_c(df_square, cahd.SD_groups,
                                                    cahd.group_list, QID_select, value, sensitive_item)
            logger("ESTSC value", estsc)
            if actsc > 0 and estsc > 0:
                temp = actsc * np.log(actsc / estsc)
            else:
                temp = 0
            KL_Divergence = KL_Divergence + temp
        KL_values.append(KL_Divergence)

    # open a file to note KLD values for different privacy degrees
    file = open("./KLD_values/KLD_BMS1_values.txt", "w")
    file.write(f"num_sensitive {num_sensitive}\n")
    file.write(f"bm_size {bm_size}\n")
    logger("p degree list lenght", len(p_degree_list))
    logger("KL values list length ", len(KL_values))
    for idx in range(len(p_degree_list)):
        file.write(f"{p_degree_list[idx]} {KL_values[idx]}\n")

    file.close()
