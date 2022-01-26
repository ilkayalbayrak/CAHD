import pandas as pd
import matplotlib.pyplot as plt
from band_matrix import compute_band_matrix, logger

if __name__ == "__main__":
    BMS1_m10_privacy_ranged_df = pd.read_csv("./Data_to_plot/BMS1_seed_42_1000_10.csv")
    BMS1_m20_privacy_ranged_df = pd.read_csv("./Data_to_plot/BMS1_seed_42_1000_20.csv")

    BMS1_p10_sensitive_ranged = pd.read_csv("./Data_to_plot/BMS1_seed_42_1000_p10_m_change.csv")
    BMS1_p20_sensitive_ranged = pd.read_csv("./Data_to_plot/BMS1_seed_42_1000_p20_m_change.csv")

    logger("BMS1_m10_privacy_ranged_df", BMS1_m10_privacy_ranged_df)
    logger("BMS1_m20_privacy_ranged_df", BMS1_m20_privacy_ranged_df)

    logger("BMS1_p10_sensitive_ranged", BMS1_p10_sensitive_ranged)
    logger("BMS1_p20_sensitive_ranged", BMS1_p20_sensitive_ranged)

    # plot KLD vs p degree
    plt.figure(figsize=(12, 8))

    x_range = [6, 8, 10, 12, 14, 16, 18, 20]
    BMS1_m10 = BMS1_m10_privacy_ranged_df[BMS1_m10_privacy_ranged_df["KLD_value"] > 0]
    BMS1_m20 = BMS1_m20_privacy_ranged_df[BMS1_m20_privacy_ranged_df["KLD_value"] > 0]

    BMS1_p10 = BMS1_p10_sensitive_ranged[BMS1_p10_sensitive_ranged["KLD_value"]>0]
    BMS1_p20 = BMS1_p20_sensitive_ranged[BMS1_p20_sensitive_ranged["KLD_value"]>0]
    logger("XXXXXXXX", BMS1_m10)

    # Plot KLD values wrt a range of privacy degrees
    plt.plot(BMS1_m10["p_degree"], BMS1_m10["KLD_value"], marker='o', linestyle='-', color='b', label="m=10")
    plt.plot(BMS1_m20["p_degree"], BMS1_m20["KLD_value"], marker='^', linestyle='-', color='r', label="m=20")
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
    plt.plot(BMS1_p10["num_sensitive"], BMS1_p10["KLD_value"], marker='o', linestyle='-', color='b', label="p=10")
    plt.plot(BMS1_p20["num_sensitive"], BMS1_p20["KLD_value"], marker='^', linestyle='-', color='r', label="p=20")
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

    # Plot CAHD execution times vs privacy degrees
    x_range = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    plt.figure(figsize=(12, 8))
    plt.plot(BMS1_m10_privacy_ranged_df["p_degree"], BMS1_m10_privacy_ranged_df["CAHD_exec_time"], marker='o', linestyle='-', color='b', label="m=10")
    plt.plot(BMS1_m20_privacy_ranged_df["p_degree"], BMS1_m20_privacy_ranged_df["CAHD_exec_time"], marker='^', linestyle='-', color='r', label="m=20")
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

