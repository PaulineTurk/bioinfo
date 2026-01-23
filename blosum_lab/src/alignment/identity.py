from itertools import combinations
from typing import Iterable, Tuple
from data.models import PfamBlock
from config import BlosumConfig


def compute_identity_on_block(
    block: PfamBlock
)-> Iterable[Tuple[str, str, int]]:
    seqs = block.sequences
    for (id1, seq1), (id2, seq2) in combinations(seqs.items(), 2):
        if id1> id2:
            id1, id2 = id2, id1
            seq1, seq2 = seq2, seq1
        identity = compute_identity(seq1, seq2)
        yield id1, id2, identity

def compute_identity(
    seq1: str,
    seq2: str
) -> int:
    if len(seq1) != len(seq2):
        raise ValueError("Aligned sequences must have the same length")
    matches = 0
    comparable = 0

    for a, b in zip(seq1, seq2):
        if a in BlosumConfig.STANDARDS_AA and b in BlosumConfig.STANDARDS_AA:
            comparable += 1
            matches += (a==b)
    return 100*matches//comparable if comparable > 0 else 0
