from math import log2
from matrix.blosum import compute_log_2_odds_matrix


def test_compute_log_2_odds_matrix():
    #seq1: AAA
    #seq2: AAE
    p_AA = 2/3
    p_AE = 1/3
    p_EE = 0
    p_A = 5/6
    p_E = 1/6
    pair_frequency = {("A", "A"): p_AA, ("A", "E"): p_AE, ("E", "E"): p_EE}
    single_frequency = {"A": p_A, "E": p_E}
    alphabet = ["A", "E"]

    expected_score = {
        ("A", "A"): 0,
        ("A", "E"): 1
        }
    assert compute_log_2_odds_matrix(pair_frequency, single_frequency, alphabet) == expected_score
