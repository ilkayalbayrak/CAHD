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
    # p_degree = 5  # the degree of privacy
    alpha = 3
    # [4, 6, 8, 10, 12, 14, 16, 18, 20]
    p_degree_list = [4, 6, 8, 10, 12, 14, 16, 18, 20]

    # TODO: note execution times for CAHD and KLD computations for plots
    CAHD_execution_times = list()
    KLD_execution_times = list()
    KL_values = list()

    # load the data
    data_path = './Dataset/BMS1_table.csv'
    df = pd.read_csv(data_path, index_col=False)

    # get the start time to calculate execution time
    start_time = time.time()

    print("Calculating band matrix")
    df_square, items, sensitive_items = compute_band_matrix(dataset=df, bm_size=bm_size, num_sensitive=num_sensitive,
                                                            plot=True)

    for privacy_degree in p_degree_list:
        # Apply CAHD algorithm to create
        cahd = CAHD(band_matrix=df_square, sensitive_items=sensitive_items, p_degree=privacy_degree, alpha_=alpha)
        print(cahd.group_dict)
        cahd.compute_hist()
        hist_item = cahd.hist
        print("Start Anonymization process")
        cahd.create_groups()
        end_time = time.time() - start_time
        # append CAHD execution time for current parameters
        CAHD_execution_times.append(int(end_time))
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

        # start timer for KLD computation
        start_time = time.time()

        # computation of all combinations for cell C
        all_value = KLDivergence.get_all_combination_of_n(r)
        logger("KLD all combinations of n for cell C", all_value)

        # get the item with the most value from the histogram
        # change the item dtype to str because the column names(item names) in band matrix are str
        # otherwise they dont match and KL divergence calculation fails
        sensitive_item = str(max(hist_item.keys(), key=(lambda k: hist_item[k])))
        logger("Sensitive item, MAX VAL from histogram", sensitive_item)
        logger("DEBUG", df_square[df_square[sensitive_items] == 1].index.tolist())
        # logger("DEBUG 2", type(df_square[0].index[0]))

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

        # append KLD values and respective calculation times
        end_time = time.time() - start_time
        KLD_execution_times.append(int(end_time))
        KL_values.append(KL_Divergence)

    # open a file to note KLD values for different privacy degrees
    # create df to write plotable data
    dict_to_plot = {"num_sensitive": num_sensitive,
                    "bm_size": bm_size,
                    "r": 4,
                    "p_degree": [],
                    "KLD_value": [],
                    "KLD_exec_time": [],
                    "CAHD_exec_time": []
                    }
    for idx in range(len(p_degree_list)):
        dict_to_plot["p_degree"].append(p_degree_list[idx])
        dict_to_plot["KLD_value"].append(KL_values[idx])
        dict_to_plot["KLD_exec_time"].append(KLD_execution_times[idx])
        dict_to_plot["CAHD_exec_time"].append(CAHD_execution_times[idx])

    df_to_plot = pd.DataFrame.from_dict(dict_to_plot)
    df_to_plot.to_csv(f"./Data_to_plot/BMS1_{bm_size}_{num_sensitive}.csv", index=False)
