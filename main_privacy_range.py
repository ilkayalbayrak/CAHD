import pandas as pd
from CAHD import CAHD
import time
import numpy as np
from KLDivergence import KLDivergence
import random
from band_matrix import compute_band_matrix, logger

if __name__ == "__main__":
    bm_size = 1000  # band matrix size
    num_sensitive = 10  # number of sensitive items
    alpha = 3
    r = 4
    p_degree_list = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    n_QID_combinations = 5

    # load the data
    data_path = './Dataset/BMS1_table.csv'
    df = pd.read_csv(data_path, index_col=False)

    # open a file to note KLD values for different privacy degrees
    # create df to write plotable data
    dict_to_plot = {"num_sensitive": num_sensitive,
                    "bm_size": bm_size,
                    "r": r,
                    "p_degree": [],
                    "KLD_value": [],
                    "KLD_exec_time": [],
                    "CAHD_exec_time": []
                    }

    # get the start time to calculate execution time
    start_time = time.time()

    print("Calculating band matrix")
    band_matrix, items, sensitive_items = compute_band_matrix(dataset=df, bm_size=bm_size, num_sensitive=num_sensitive,
                                                              plot=True)

    for privacy_degree in p_degree_list:
        # Apply CAHD algorithm to create
        cahd = CAHD(band_matrix=band_matrix, sensitive_items=sensitive_items, p_degree=privacy_degree, alpha_=alpha)
        print(cahd.group_dict)
        cahd.compute_hist()
        hist_item = cahd.hist
        print(f"\nStarting the anonymization process for Privacy_Degree: {privacy_degree}")
        logger("Histogram Items", hist_item)
        cahd.create_groups()
        cahd_ex_time = time.time() - start_time

        # append CAHD execution time for current parameters
        print(f"Privacy-degree: {cahd.p_degree}\nTime required for creating the anonymized groups: {cahd_ex_time}\n")

        QID = cahd.group_list[0].columns.tolist()
        np.random.shuffle(QID)
        # QID_select = [i for i in list(chunks(QID,r)) if len(i) == r][:5]
        QID_select_list = list(cahd.chunks(QID, r))[:n_QID_combinations]

        # logger("QID select", QID_select)

        # start timer for KLD computation
        start_time = time.time()

        # get the item with the most value from the histogram
        # change the item dtype to str because the column names(item names) in band matrix are str
        # otherwise they dont match and KL divergence calculation fails
        sensitive_item = str(max(hist_item.keys(), key=(lambda k: hist_item[k])))

        # computation of all combinations for cell C
        all_value = KLDivergence.get_all_combinations_of_QID_subset(r)
        # logger("KLD all combinations of n for cell C", all_value)

        for QID_select in QID_select_list:
            # Calculate KL_Divergence value
            KL_Divergence = KLDivergence(band_matrix, QID_select, cahd.SD_groups,
                                         cahd.group_list,
                                         sensitive_items, all_value)
            KLD_value = KL_Divergence.compute_KLDivergence_value()

            print(f"\n{'-' * 20}\nKL_Divergence Total: {KLD_value}, Privacy degree: {privacy_degree},"
                  f"Sensitive Item: {sensitive_item}\nQID_select: {QID_select}\n{'-' * 20}\n")

            # append KLD values and respective calculation times
            end_time = time.time() - start_time

            dict_to_plot["p_degree"].append(privacy_degree)
            dict_to_plot["KLD_value"].append(KLD_value)
            dict_to_plot["KLD_exec_time"].append(end_time)
            dict_to_plot["CAHD_exec_time"].append(cahd_ex_time)

    df_to_plot = pd.DataFrame.from_dict(dict_to_plot)
    df_to_plot.to_csv(f"./Data_to_plot/asd_cahd-bm-forKLD-test_{bm_size}_m{num_sensitive}.csv", index=False)
