import matplotlib.pyplot as plt
import seaborn 
import pandas
import numpy 
from data.amino_acids import BLOSUM_ORDER
from collections import Counter
from Bio.Align import substitution_matrices


def canonical_pair(a, b):
    if BLOSUM_ORDER.index(a) <= BLOSUM_ORDER.index(b):
        return (a, b)
    else:
        return (b, a)

def visualize_blosum_matrix(score: Counter, path_save: str):
    alphabet = BLOSUM_ORDER
    size = len(alphabet)
    matrix = numpy.full((size, size), numpy.nan)
    for i, aa1 in enumerate(alphabet):
        for j, aa2 in enumerate(alphabet):
            key = canonical_pair(aa1, aa2)
            if key in score:
                matrix[i,j] = score[key]
    dataframe = pandas.DataFrame(matrix, index=alphabet, columns=alphabet)

    mask = numpy.triu(numpy.ones_like(dataframe, dtype=bool), k=1)
    plt.figure(figsize=(12,10))
    seaborn.heatmap(dataframe, mask=mask, annot=True, cmap="vlag_r", center=0, square=True, cbar_kws={"shrink": .8})
    plt.yticks(rotation = 0)
    plt.title('BLOSUM-like')
    plt.savefig(path_save)
    plt.close()


def compare_to_reference(my_scores:Counter, matrix_name:str, path_save:str):
    ref_matrix = substitution_matrices.load(matrix_name)
    alphabet = BLOSUM_ORDER
    
    size = len(alphabet)
    my_mat = numpy.zeros((size, size))
    ref_mat = numpy.zeros((size, size))

    for i, aa1 in enumerate(alphabet):
        for j, aa2 in enumerate(alphabet):
            pair = (aa1, aa2)
            rev_pair = (aa2, aa1)
            my_mat[i, j] = my_scores.get(pair) or my_scores.get(rev_pair) or 0
            ref_mat[i, j] = ref_matrix[aa1][aa2]

    diff_mat = my_mat - ref_mat
    
    df_diff = pandas.DataFrame(diff_mat, index=list(alphabet), columns=list(alphabet))

    mask = numpy.triu(numpy.ones_like(df_diff, dtype=bool), k=1)

    plt.figure(figsize=(12, 10))
    seaborn.heatmap(df_diff, mask=mask, annot=True, cmap="vlag_r", center=0, square=True)
    plt.yticks(rotation = 0)
    mean_absolute_error = compute_mean_absolute_error(my_mat, ref_mat)

    plt.title(f"BLOSUM-like - BLOSUM with mean absolute error {mean_absolute_error:.3f}")
    plt.savefig(path_save)
    plt.close()


def compute_mean_absolute_error(your_matrix, ref_matrix):
    mask = numpy.tril(numpy.ones_like(your_matrix, dtype=bool))
    my_vals = your_matrix[mask].flatten()
    ref_vals = ref_matrix[mask].flatten()
    mean_absolute_error = numpy.mean(numpy.abs(my_vals - ref_vals))
    return mean_absolute_error


