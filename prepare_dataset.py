import numpy as np
import pandas as pd
import os
import itertools

"""
This is the .py version of the prepare_dataset.ipynb, 
created just for convenience
"""


def find_unique_items(input_path, output_path):
    """function for finding the unique items in BMS txt file"""
    input_file = open(input_path, "r")
    output_file = open(output_path, "w")

    input_contents = input_file.read()
    item_list = input_contents.split()
    unique_items = set(item_list)

    unique_items.difference_update({"-1", "-2"})

    for item in unique_items:
        output_file.write(str(item) + "\n")

    input_file.close()
    output_file.close()


def sequence_to_binary_matrix(data_path, item_names_path, output_path):
    """
    converts sequences of data into binary matrix format
    and creates a new csv file to store it
    """
    data_file = open(data_path, "r")
    item_names_file = open(item_names_path, "r")

    item_names = item_names_file.read().split()

    # create item index dictionary to create binary matrix
    item_index = {}
    idx = 0
    for item in [int(item) for item in item_names]:
        item_index[item] = idx
        idx += 1

    # read and clean sequence rows (original form of the data)
    binary_matrix = list()
    with open(data_path) as file:
        for line in file:
            row = [int(value) for value in set(line.rstrip().split()) if value != "-1" and value != "-2"]

            # vector of zeros
            vec = np.zeros(len(item_names))
            for item in row:
                for key, idx in item_index.items():
                    if item == key:
                        vec[idx] = 1
            binary_matrix.append(vec)

    df = pd.DataFrame(binary_matrix, columns=item_index.keys(), dtype=np.int)
    df.to_csv(output_path, index=None)


if __name__ == "__main__":
    find_unique_items("./Dataset/BMS1_spmf.txt", "./Dataset/BMS1_item_names.txt")
    sequence_to_binary_matrix("./Dataset/BMS1_spmf.txt", "./Dataset/BMS1_item_names.txt", "./Dataset/BMS1_table.csv")
