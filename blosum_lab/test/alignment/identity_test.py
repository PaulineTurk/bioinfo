from alignment.identity import compute_identity, compute_identity_on_block
from data.models import PfamBlock
import pytest

class TestIdentity:
    @pytest.mark.parametrize("seq1, seq2, expected_identity",
        [(
        "AIQFSDTH.G.EVCPANW.QE..........GEEAM...KPTTE.G..VADYLTR",
        "MIREVEKNGGKQVCPANW.RR..........GEKMM...HASFE.G..VKNYLGQ",
        44),
        ("AbC",
        "ABD",
        50),
        ("A-C",
        "A-D",
        50),
        ("ABC",
         "DEF", 
         0)
        ])
    def test_real_example_pairwise_identity(self, seq1, seq2, expected_identity):
        assert compute_identity(seq1, seq2) == expected_identity


    def test_pairwise_identity_throws_error_for_seq_with_different_length(self):
        seq1= "A.CDE"
        seq2= "ABC."
        with pytest.raises(ValueError, match="Aligned sequences must have the same length"):
            compute_identity(seq1, seq2) 


    def test_compute_identity_on_block(self):
        block = PfamBlock(
            accession="PF00000",
            sequences={
                "seqA": "AECW",
                "seqC": "AFCW",
                "seqB": "AECW",
            }
        )
        expected_result = [
            ("seqA", "seqC", 75),
            ("seqA", "seqB", 100),
            ("seqB", "seqC", 75)
        ]
        result = list(compute_identity_on_block(block))
        assert result == expected_result
