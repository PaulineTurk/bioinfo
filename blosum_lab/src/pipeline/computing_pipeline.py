from storage.sqlite import DatabaseBlosumStore
from matrix import counting
from matrix.blosum import compute_log_2_odds_matrix
from matrix.visualisation import visualize_blosum_matrix, compare_to_reference


def run(
        db_path:str, 
        threshold:int, 
        pairwise_count_file:str, 
        blosum_like_path:str, 
        reference_matrix:str, 
        matrix_difference_path:str):
    store = DatabaseBlosumStore(db_path)
    #TODO: renommer result en clusters elements ..
    result = store.get_clusters(threshold)
    total_pair = counting.global_count(result, pairwise_count_file)
    pij = counting.compute_pij(total_pair)
    pi = counting.compute_pi(pij)
    counting.run_sanity_checks(pij, pi)
    score = compute_log_2_odds_matrix(pij, pi)
    visualize_blosum_matrix(score, blosum_like_path)
    compare_to_reference(score, reference_matrix, matrix_difference_path)