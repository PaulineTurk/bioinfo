from data.pfam_blocks import is_sequence, build_pfam_blocks, count_pfam_blocks
from config import BLOSUM_CONFIG_TEST
from itertools import islice
import pytest

class TestPfamBlocks:
    class TestIsSequence:
        @pytest.mark.parametrize(
            "line, expected", [
                ("", False),
                ("#123", False),
                ("//", False),
                ("seq1 ABCD", True)
            ]
        )
        def test_is_sequence(self, line, expected):
            assert is_sequence(line) == expected

    def test_build_pfam_blocks(self):
        stream = build_pfam_blocks(BLOSUM_CONFIG_TEST.pfam_path)
        blocks = list(islice(stream, 3))
        assert len(blocks) == 3
        assert blocks[0].accession.startswith("PF")
        assert len(blocks[0].sequences) > 1
        assert blocks[0].accession != blocks[1].accession
    
    def test_count_pfam_blocks(self):
        count = count_pfam_blocks(BLOSUM_CONFIG_TEST.pfam_path)
        expected_count = 10
        assert count == expected_count


