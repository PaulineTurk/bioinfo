from collections import defaultdict, Counter
from itertools import combinations
from tqdm import tqdm
import pickle
from pathlib import Path
import os
from config import BlosumConfig

PFAM_POSITION = 0
WEIGHT_POSITION = 3
SEQ_POSITION = 4
def group_by_pfam(result):
    pfams = defaultdict(list)
    for row in result:
        pfams[row[PFAM_POSITION]].append(row)
    return pfams

def count_aa_by_column(pfam_rows):
    pair_count = Counter()
    alignment_length = len(pfam_rows[0][SEQ_POSITION])
    for index in range(alignment_length):
        column = []
        for row in pfam_rows:
            aa = row[SEQ_POSITION][index]
            if aa in BlosumConfig.STANDARDS_AA:
                column.append((aa, row[WEIGHT_POSITION]))
        if len(column) < 2:
            continue
        for (aa1, weight1), (aa2, weight2) in combinations(column, 2):
            composed_weight = weight1*weight2
            if aa1 <= aa2:
                pair_count[(aa1, aa2)] += composed_weight
            else:
                pair_count[(aa2, aa1)] += composed_weight
    return pair_count

#TODO: add test
def compute_global_count(result):
    pfams = group_by_pfam(result)
    total_pair = Counter()
    pfams_total = len(pfams)

    for pfam_rows in tqdm(pfams.values(), total=pfams_total, desc="Pair computing"):
        if len(pfam_rows) < BlosumConfig.MIN_PFAM_SIZE:
            continue
        pfam_pair = count_aa_by_column(pfam_rows)
        total_pair.update(pfam_pair)
    return total_pair

def global_count(result, pairwise_path:str):
    if os.path.exists(pairwise_path):
        return load_counter(pairwise_path)
    total_pair = compute_global_count(result)
    save_counter(total_pair, pairwise_path)
    return total_pair

#TODO: test utils
def compute_pij(total_pair):
    total = sum(total_pair.values())
    return safe_divide(total_pair, total)

def compute_pi(pij):
    pi = {aa:0.0 for aa in BlosumConfig.STANDARDS_AA}
    for (a,b), v in pij.items():
        if a==b:
            pi[a] += v
        else:
            pi[a] += v/2
            pi[b] += v/2
    return pi

    
def safe_divide(counter: Counter, divisor: int):
    if divisor == 0:
        raise ValueError("divisor must be non-zero")
    return Counter({k: v/divisor for k,v in counter.items()})


def save_counter(counter:Counter, path:str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as file:
        pickle.dump(counter, file, protocol=pickle.HIGHEST_PROTOCOL)

def load_counter(path:str):
    with open(path, "rb") as file:
        return pickle.load(file)
    
def run_sanity_checks(pij, pi):
    print("--- Rapport de Sanity Check ---")
    
    total_pij = sum(pij.values())
    print(f"Somme totale pij : {total_pij:.6f} {'[OK]' if abs(total_pij - 1.0) < 1e-6 else '[ERREUR]'}")
    
    total_pi = sum(pi.values())
    print(f"Somme totale pi  : {total_pi:.6f} {'[OK]' if abs(total_pi - 1.0) < 1e-6 else '[ERREUR]'}")
    
    for aa in pi:
        reconstructed_pi = 0
        for (a, b), val in pij.items():
            if a == b and a == aa:
                reconstructed_pi += val
            elif a == aa or b == aa:
                reconstructed_pi += val / 2
        
        diff = abs(reconstructed_pi - pi[aa])
        if diff > 1e-6:
            print(f"Incohérence pour {aa}: pi={pi[aa]:.4f}, reconstruit={reconstructed_pi:.4f}")