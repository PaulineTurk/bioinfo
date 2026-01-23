from collections import Counter
from math import log2
from tqdm import tqdm
from config import BlosumConfig

BLOSUM_ORDER = [
    'C', 'S', 'T', 'P', 'A', 'G', 'N', 'D', 'E', 'Q',
    'H', 'R', 'K', 'M', 'I', 'L', 'V', 'F', 'Y', 'W'
    ]

def compute_log_2_odds_matrix(
        pair_frequency: Counter, 
        single_frequency: Counter, 
        alphabet: list[str] = BLOSUM_ORDER):
    score = {}

    alphabet_size = len(alphabet)
    for i, aa1 in tqdm(enumerate(alphabet), desc="Blosum computing", total=alphabet_size):
        for aa2 in alphabet[i:]:
            key = (aa1, aa2) if (aa1, aa2) in pair_frequency else (aa2, aa1)
            p_ij = pair_frequency[key]            
            p_i = single_frequency.get(aa1, 0.0)
            p_j = single_frequency.get(aa2, 0.0)
            if p_ij == 0 or p_i == 0 or p_j == 0:
                continue
            if aa1 == aa2:
                excepted = p_i*p_i
            else:
                excepted = 2*p_i*p_j
            score[aa1, aa2] =  log2(p_ij/excepted)
    return {k:round(v*BlosumConfig.ROUNDING_BLOSUM_STANDARD) for k,v in score.items()}


