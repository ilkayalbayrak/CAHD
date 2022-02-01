import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from band_matrix import compute_band_matrix, logger


def prepare_avg_values(df, depend_col):
    avg_value_dict = dict({
        "avg_KLD_value": [],
        "CAHD_exec_time": [],
        "KLD_exec_time": []
    })

    for i in df[depend_col].unique():
        avg_value_dict["avg_KLD_value"].append(df["KLD_value"][df[depend_col] == i].mean())
        avg_value_dict["CAHD_exec_time"].append(df["CAHD_exec_time"][df[depend_col] == i].mean())
        avg_value_dict["KLD_exec_time"].append(df["KLD_exec_time"][df[depend_col] == i].mean())

    return avg_value_dict


if __name__ == "__main__":
    # p_range_m10_df = pd.read_csv("Data_to_plot/Merged_outputs/BMS1_p_range_m10.csv")
    p_range_m10_df = pd.read_csv("Data_to_plot/TEST2_BMS1_seed_42_1000_m10.csv")
    p_range_m20_df = pd.read_csv("Data_to_plot/TEST1_BMS1_seed_42_1000_m20.csv")

    m_range_p10_df = pd.read_csv("Data_to_plot/S_TEST1_BMS1_seed_42_1000_p10_m_change.csv")
    m_range_p20_df = pd.read_csv("Data_to_plot/S_TEST1_BMS1_seed_42_1000_p20_m_change.csv")

    r_range_pm10_df = pd.read_csv("Data_to_plot/Merged_outputs/BMS1_r_range_p10.csv")

    # p_range_m10_df = p_range_m10_df.replace(0, np.NaN)
    # p_range_m20_df = p_range_m20_df.replace(0, np.NaN)

    avg_p_m10 = prepare_avg_values(p_range_m10_df, "p_degree")
    avg_p_m20 = prepare_avg_values(p_range_m20_df, "p_degree")

    avg_m_p10 = prepare_avg_values(m_range_p10_df, "num_sensitive")
    avg_m_p20 = prepare_avg_values(m_range_p20_df, "num_sensitive")

    avg_r = prepare_avg_values(r_range_pm10_df, "r")

    # plot KLD vs p degree
    plt.figure(figsize=(12, 8))

    x_range = [4, 6, 8, 10, 12, 14, 16, 18, 20]

    # Plot KLD values wrt a range of privacy degrees
    plt.plot(p_range_m10_df["p_degree"].unique(), avg_p_m10["avg_KLD_value"], marker='o', linestyle='-', color='b',
             label="m=10")
    plt.plot(p_range_m20_df["p_degree"].unique(), avg_p_m20["avg_KLD_value"], marker='^', linestyle='-', color='r',
             label="m=20")
    plt.ylim(ymax=2)
    plt.ylim(ymin=0)
    # plt.xlim(xmin=0)
    plt.xlabel("Privacy degree")
    plt.ylabel("KL_Divergence")
    plt.xticks(x_range, x_range)
    plt.title("KLD values over a range of p degrees (r = 4) BMS1 m = 10 & m = 20 ")
    plt.legend()
    plt.savefig('./Plots/TEST2_BMS1_p_vs_KLD.png')
    plt.show()

    # Plot KLD values over a changing quantity of sensitive items
    x_range = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    plt.figure(figsize=(12, 8))
    plt.plot(m_range_p10_df["num_sensitive"].unique(), avg_m_p10["avg_KLD_value"], marker='o', linestyle='-', color='b',
             label="p=10")
    plt.plot(m_range_p20_df["num_sensitive"].unique(), avg_m_p20["avg_KLD_value"], marker='^', linestyle='-', color='r',
             label="p=20")
    plt.ylim(ymax=2)
    plt.ylim(ymin=0)
    # plt.xlim(xmin=0)
    plt.xlabel("Number of Sensitive Items")
    plt.ylabel("KL_Divergence")
    plt.xticks(x_range, x_range)
    plt.title("KLD values over a range of number of sensitive items  (r = 4) BMS1 p = 10 & p = 20 ")
    plt.legend()
    plt.savefig('./Plots/BMS1_m_vs_KLD.png')
    plt.show()

    # Plot CAHD execution times vs privacy degrees
    x_range = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    plt.figure(figsize=(12, 8))
    plt.plot(p_range_m10_df["p_degree"].unique(), avg_p_m10["CAHD_exec_time"], marker='o', linestyle='-', color='b',
             label="m=10")
    plt.plot(p_range_m20_df["p_degree"].unique(), avg_p_m20["CAHD_exec_time"], marker='^', linestyle='-', color='r',
             label="m=20")
    # plt.ylim(ymax=0.2)
    plt.ylim(ymin=0)
    # plt.xlim(xmin=0)
    plt.xlabel("Number of Sensitive Items")
    plt.ylabel("Execution Time (Seconds)")
    plt.xticks(x_range, x_range)
    plt.title("CAHD Execution Times Over Privacy Degrees (r = 4) BMS1 m = 10 & m = 20 ")
    plt.legend()
    plt.savefig('./Plots/BMS1_CAHD_exec_time_vs_p.png')
    plt.show()

    # Plot CAHD execution times vs privacy degrees
    x_range = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    plt.figure(figsize=(12, 8))
    plt.plot(m_range_p10_df["num_sensitive"].unique(), avg_m_p10["CAHD_exec_time"], marker='o', linestyle='-',
             color='b', label="m=10")
    plt.plot(m_range_p20_df["num_sensitive"].unique(), avg_m_p20["CAHD_exec_time"], marker='^', linestyle='-',
             color='r', label="m=20")
    # plt.ylim(ymax=0.2)
    plt.ylim(ymin=0)
    # plt.xlim(xmin=0)
    plt.xlabel("Number of Sensitive Items")
    plt.ylabel("Execution Time (Seconds)")
    plt.xticks(x_range, x_range)
    plt.title("CAHD Execution Times Over a Count of Sensitive Items (r = 4) BMS1 p = 10 & p = 20 ")
    plt.legend()
    plt.savefig('./Plots/BMS1_CAHD_exec_time_vs_p.png')
    plt.show()
