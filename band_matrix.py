import pandas as pd
import numpy as np
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix
import matplotlib.pylab as plt


def logger(label, obj):
    print(f'\n{"-" * 20}\n{label}:\n{obj}\n{"-" * 20}\n')


def plot_band_matrix(square_matrix, square_band_matrix, bandwidth_1, bandwidth_2, save_plot=False):
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    f.set_figheight(8)
    f.set_figwidth(16)
    f.suptitle("Before & After RCM Bandwidth Reduction")

    ax1.spy(square_matrix, marker='.', markersize='2')
    ax1.set_title("Original Sparse Data")

    ax2.spy(square_band_matrix, marker='.', markersize='2')
    ax2.set_title("Data after RCM")

    if save_plot:
        plt.savefig('./Plots/band_matrix_plot.png')
    plt.show()

    print("Bandwidth before RCM: ", bandwidth_1)
    print("Bandwidth after RCM", bandwidth_2)


def compute_band_matrix(dataset=None, bm_size=1000, num_sensitive=1, plot=False):
    # input : unsymmetric matrix A
    # compute symmetric matrix B = AxA.T
    # sigma = RCM(sigma)
    # A'= permutation sigma applied to A
    # return A'

    # TODO: Add a zero padding method for the 'matrix slicing' so we can have bigger matrices then len(items)
    if dataset is not None and len(dataset) >= bm_size:
        logger('Original df head', dataset.head())
        items = None # FIXME: this should probably go in the if else statements, rather than being global
        # logger('Items', items[:10])

        # define a random seed for np.random operations
        np.random.seed(seed=42)

        random_column = None
        random_row = None

        # check if we need to add zero filler columns
        if len(dataset.columns) >= bm_size:
            items = dataset.columns # FIXME: this may need to be converted to a list explicitly, check if it runs correctly
            # random permutation of rows and columns
            random_column = np.random.permutation(dataset.shape[1])[:bm_size]
            logger('Random columns', random_column[:10])

            random_row = np.random.permutation(dataset.shape[0])[:bm_size]
            logger('Random rows', random_row[:10])

        else:
            random_row = np.random.permutation(dataset.shape[0])
            dataset = dataset.iloc[random_row][:bm_size]
            dataset = dataset.reset_index()
            dataset.drop('index', axis=1, inplace=True)

            columns = dataset.columns

            # fill the gap between the features and wanted dimension size with zeros
            zero_data_to_add = np.zeros(shape=(len(dataset), len(dataset) - len(columns)))
            columns_to_add = [f"temp_{x}" for x in range(0, len(dataset) - len(columns))]

            df_to_add = pd.DataFrame(zero_data_to_add, columns=columns_to_add, index=dataset.index, dtype='uint8')

            # add all prepared filler zeros to dataset
            dataset = pd.concat([dataset, df_to_add], axis=1)

            # shuffle rows and cols
            np.random.seed(seed=42)
            items = dataset.columns

            random_column = np.random.permutation(dataset.shape[1])
            random_row = np.random.permutation(dataset.shape[0])

            dataset.columns = [str(i) for i in range(len(dataset.columns))]

        items_reordered = [items[i] for i in random_column]
        logger('Items reordered', items_reordered[:10])

        # cut selected size of square piece from the dataset
        df_square = dataset.iloc[random_row, random_column]
        logger('df_square', df_square.head())

        # spy method is for plotting sparsity pattern of 2D arrays
        # plt.spy(df_square, marker='.', markersize='1')

        # select sensitive items
        sensitive_items = df_square.columns[-num_sensitive:]
        # sensitive_items = np.random.choice(df_square.columns, num_sensitive)
        logger('Sensitive items', sensitive_items)

        # Convert df to sparse matrix format
        sparse = csr_matrix(df_square)

        # Compute RCM
        # RCM func assumes the input matrix is not symmetric
        # therefore no need to try to create a symmetric matric beforehand
        # TODO: try out preparing a symmetric input matrix to see if anything changes
        order = reverse_cuthill_mckee(sparse)
        logger('RCM', order)
        # plt.spy(order, marker='.', markersize='1')


        columns_final_order = [df_square.columns[i] for i in order]
        logger('Columns final order', columns_final_order)

        # items_final_order = [items_reordered[i] for i in order]
        items_final_order = [items_reordered[i] for i in order]

        logger('Items final order', items_final_order)
        logger('Items final order LENGTH', len(items_final_order))
        # items_final_test = dict(zip(columns_final_order, items_final_order))
        # logger("######################3 TEST ###############3", list(items_final_test))

        # Band matrix
        df_square_band = df_square.iloc[order][columns_final_order]

        # Band of the inital dataframe
        [i, j] = np.where(df_square == 1)
        bw1 = max(i - j) + 1

        # Band after RCM --> it will be reduced
        [i, j] = np.where(df_square_band == 1)
        bw2 = max(i - j) + 1

        if plot:
            plot_band_matrix(df_square, df_square_band, bw1, bw2)

        return df_square_band, items_final_order, sensitive_items
    # elif dataset is not None and len(dataset) >= bm_size:
    #     pass


if __name__ == '__main__':
    df = pd.read_csv('./Dataset/BMS1_table.csv', index_col=False)
    df_square, items, sensitive_items = compute_band_matrix(dataset=df, bm_size=1000, num_sensitive=5)
    logger("Band matrix shape", df_square.shape)
    logger("band matrix columns", df_square.columns)

