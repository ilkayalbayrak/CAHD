import pandas as pd
from cahd_update import CAHD
import time
import numpy as np
import KLDivergence
import random
from band_matrix import compute_band_matrix, logger

if __name__ == "__main__":
    bm_size = 1000  # band matrix size
    # num_sensitive_list = [4, 6, 8, 10, 12, 14, 16, 18, 20]  # number of sensitive items
    num_sensitive_list = [4]
    # p_degree = 5  # the degree of privacy
    alpha = 3
    r = 4
    # [4, 6, 8, 10, 12, 14, 16, 18, 20]
    p_degree = 10
    # p_degree_list = [4, 6]
    n_QID_combinations = 5

    CAHD_execution_times = list()
    KLD_execution_times = list()
    KL_values = list()

    # load the data
    data_path = './Dataset/BMS1_table.csv'
    df = pd.read_csv(data_path, index_col=False)

    dict_to_plot = {"num_sensitive": [],
                    "bm_size": bm_size,
                    "r": r,
                    "p_degree": p_degree,
                    "KLD_value": [],
                    "KLD_exec_time": [],
                    "CAHD_exec_time": []
                    }

    # get the start time to calculate execution time
    start_time = time.time()


    for m in num_sensitive_list:

        print("Calculating band matrix")
        df_square, items, sensitive_items = compute_band_matrix(dataset=df, bm_size=bm_size, num_sensitive=m,
                                                                plot=True)
        # Apply CAHD algorithm to create
        cahd = CAHD(band_matrix=df_square, sensitive_items=sensitive_items, p_degree=p_degree, alpha_=alpha)
        print(cahd.group_dict)
        cahd.compute_hist()
        hist_item = cahd.hist
        print(f"\nStarting the anonymization process for Number of Sensitive Items: {m}")
        logger("Histogram Items", hist_item)
        cahd.create_groups()
        cahd_ex_time = time.time() - start_time

        # append CAHD execution time for current parameters
        CAHD_execution_times.append(int(cahd_ex_time))
        print(f"Privacy-degree: {cahd.p_degree}, Num. Sensitive:{m}\nTime required for creating the anonymized groups: {cahd_ex_time}\n")

        # r = 4
        QID = cahd.group_list[0].columns.tolist()
        # logger("QID list", QID)
        # QID_select = list()
        # while len(QID_select) < r:
        #     temp = random.choice(QID)
        #     if temp not in QID_select:
        #         QID_select.append(temp)

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
        # logger("Sensitive item, MAX VAL from histogram", sensitive_item)
        # logger("hist_item",hist_item )
        # logger("DEBUG", df_square[df_square[sensitive_items] == 1].index.tolist())
        # logger("DEBUG 2", type(df_square[0].index[0]))

        # computation of all combinations for cell C
        all_value = KLDivergence.get_all_combination_of_n(r)
        # logger("KLD all combinations of n for cell C", all_value)

        for QID_select in QID_select_list:
            # Calculate KL_Divergence value
            KL_Divergence = KLDivergence.compute_KLDivergence_value(df_square, QID_select, cahd.SD_groups,
                                                                    cahd.group_list,
                                                                    sensitive_items, all_value)

            print(f"\n{'-' * 20}\nKL_Divergence Total: {KL_Divergence}, Privacy degree: {p_degree},"
                  f"Sensitive Item: {sensitive_item}\nQID_select: {QID_select}\n{'-' * 20}\n")

            # append KLD values and respective calculation times
            end_time = time.time() - start_time
            KLD_execution_times.append(int(end_time))
            KL_values.append(KL_Divergence)

            dict_to_plot["num_sensitive"].append(m)
            dict_to_plot["KLD_value"].append(KL_Divergence)
            dict_to_plot["KLD_exec_time"].append(end_time)
            dict_to_plot["CAHD_exec_time"].append(cahd_ex_time)

        # # Calculate KL_Divergence value
        # KL_Divergence = KLDivergence.compute_KLDivergence_value(df_square, QID_select, cahd.SD_groups, cahd.group_list,
        #                                                         sensitive_items, all_value)
        #
        # print(f"\n{'-' * 20}\nKL_Divergence Total: {KL_Divergence}, Num_sensitive: {m} Privacy degree: {p_degree},"
        #       f"Sensitive Item: {sensitive_item}\nQID_select: {QID_select}\n{'-' * 20}\n")
        #
        # # append KLD values and respective calculation times
        # end_time = time.time() - start_time
        # KLD_execution_times.append(int(end_time))
        # KL_values.append(KL_Divergence)



    # # open a file to note KLD values for different privacy degrees
    # # create df to write plotable data
    # dict_to_plot = {"num_sensitive": [],
    #                 "bm_size": bm_size,
    #                 "r": 4,
    #                 "p_degree": p_degree,
    #                 "KLD_value": [],
    #                 "KLD_exec_time": [],
    #                 "CAHD_exec_time": []
    #                 }
    # for idx in range(len(num_sensitive_list)):
    #     dict_to_plot["num_sensitive"].append(num_sensitive_list[idx])
    #     dict_to_plot["KLD_value"].append(KL_values[idx])
    #     dict_to_plot["KLD_exec_time"].append(KLD_execution_times[idx])
    #     dict_to_plot["CAHD_exec_time"].append(CAHD_execution_times[idx])

    df_to_plot = pd.DataFrame.from_dict(dict_to_plot)
    df_to_plot.to_csv(f"./Data_to_plot/S_TEST1_BMS1_seed_42_{bm_size}_p{p_degree}_m_change.csv", index=False)
