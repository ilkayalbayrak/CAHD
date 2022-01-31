import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from band_matrix import compute_band_matrix, logger

if __name__ == "__main__":
    p_range_m10_df = pd.read_csv("Data_to_plot/Merged_outputs/BMS1_p_range_m10.csv")
    p_range_m20_df = pd.read_csv("Data_to_plot/Merged_outputs/BMS1_p_range_m20.csv")

    m_range_p10_df = pd.read_csv("Data_to_plot/Merged_outputs/BMS1_m_range_p10.csv")
    m_range_p20_df = pd.read_csv("Data_to_plot/Merged_outputs/BMS1_m_range_p20.csv")

    r_range_pm10_df = pd.read_csv("Data_to_plot/Merged_outputs/BMS1_r_range_p10.csv")

    logger("BMS1_m10_privacy_ranged_df", p_range_m10_df)
    logger("BMS1_m20_privacy_ranged_df", p_range_m20_df)

    logger("BMS1_p10_sensitive_ranged", m_range_p10_df)
    logger("BMS1_p20_sensitive_ranged", m_range_p20_df)

    #TODO: get the count of items per p_degree or m
    # calculate the average KLD for each p_degree or m

    avg_p_m10 = []
    avg_p_m20 = []

    avg_m_p10 = []
    avg_m_p20 = []

    avg_r = []
    # p_range_m10_df = p_range_m10_df.replace(0, np.NaN)
    # p_range_m20_df = p_range_m20_df.replace(0, np.NaN)
    #
    # m_range_p10_df = m_range_p10_df.replace(0, np.NaN)
    # m_range_p20_df = m_range_p20_df.replace(0, np.NaN)

    for i in p_range_m10_df["p_degree"].unique():
        count = 0
        avg_p_m10.append(p_range_m10_df["KLD_value"][p_range_m10_df["p_degree"] == i].mean())
    print(avg_p_m10)

    for i in p_range_m20_df["p_degree"].unique():
        count = 0
        avg_p_m20.append(p_range_m20_df["KLD_value"][p_range_m20_df["p_degree"] == i].mean())
    print(avg_p_m20)

    for i in m_range_p10_df["num_sensitive"].unique():
        count = 0
        avg_m_p10.append(m_range_p10_df["KLD_value"][m_range_p10_df["num_sensitive"] == i].mean())
    print(avg_m_p10)

    for i in m_range_p20_df["num_sensitive"].unique():
        count = 0
        avg_m_p20.append(m_range_p20_df["KLD_value"][m_range_p20_df["num_sensitive"] == i].mean())
    print(avg_m_p20)

    for i in r_range_pm10_df["r"].unique():
        count = 0
        avg_r.append(r_range_pm10_df["KLD_value"][r_range_pm10_df["r"] == i].mean())
    print(avg_r)
    # plot KLD vs p degree
    plt.figure(figsize=(12, 8))

    x_range = [4,6, 8, 10, 12, 14, 16, 18, 20]

    # Plot KLD values wrt a range of privacy degrees
    plt.plot(p_range_m10_df["p_degree"].unique(), avg_p_m10, marker='o', linestyle='-', color='b', label="m=10")
    plt.plot(p_range_m20_df["p_degree"].unique(), avg_p_m20, marker='^', linestyle='-', color='r', label="m=20")
    # plt.ylim(ymax=0.1)
    plt.ylim(ymin=0)
    # plt.xlim(xmin=0)
    plt.xlabel("Privacy degree")
    plt.ylabel("KL_Divergence")
    plt.xticks(x_range, x_range)
    plt.title("KLD values over a range of p degrees (r = 4) BMS1 m = 10 & m = 20 ")
    plt.legend()
    plt.savefig('./Plots/BMS1_p_vs_KLD.png')
    plt.show()

    # Plot KLD values over a changing quantity of sensitive items
    x_range = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    plt.figure(figsize=(12, 8))
    plt.plot(m_range_p10_df["num_sensitive"].unique(), avg_m_p10, marker='o', linestyle='-', color='b', label="p=10")
    plt.plot(m_range_p20_df["num_sensitive"].unique(), avg_m_p20, marker='^', linestyle='-', color='r', label="p=20")
    # plt.ylim(ymax=0.2)
    plt.ylim(ymin=0)
    # plt.xlim(xmin=0)
    plt.xlabel("Number of Sensitive Items")
    plt.ylabel("KL_Divergence")
    plt.xticks(x_range, x_range)
    plt.title("KLD values over a range of number of sensitive items  (r = 4) BMS1 p = 10 & p = 20 ")
    plt.legend()
    plt.savefig('./Plots/BMS1_m_vs_KLD.png')
    plt.show()

    # print(map())
    # Plot CAHD execution times vs privacy degrees
    # x_range = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    # plt.figure(figsize=(12, 8))
    # plt.plot(p_range_m10_df["p_degree"].unique(), p_range_m10_df["CAHD_exec_time"], marker='o', linestyle='-', color='b', label="m=10")
    # plt.plot(p_range_m20_df["p_degree"].unique(), p_range_m20_df["CAHD_exec_time"], marker='^', linestyle='-', color='r', label="m=20")
    # # plt.ylim(ymax=0.2)
    # plt.ylim(ymin=0)
    # # plt.xlim(xmin=0)
    # plt.xlabel("Number of Sensitive Items")
    # plt.ylabel("Execution Time (Seconds)")
    # plt.xticks(x_range, x_range)
    # plt.title("CAHD Execution Times Over Privacy Degrees (r = 4) BMS1 m = 10 & m = 20 ")
    # plt.legend()
    # plt.savefig('./Plots/BMS1_CAHD_exec_time_vs_p.png')
    # plt.show()

