from matrix.counting import group_by_pfam, count_aa_by_column

class TestCounting():
    def test_group_by_pfam(self):
        data = [
            ("PF1", 1, "id1", "AAAA"),
            ("PF1", 2, "id2", "BBBB"),
            ("PF2", 1, "id3", "CCCC"),
        ]

        grouped = group_by_pfam(data)

        assert set(grouped.keys()) == {"PF1", "PF2"}
        assert len(grouped["PF1"]) == 2
        assert len(grouped["PF2"]) == 1

    def test_count_aa_by_column(self):
        data = [
            ("PF1", 0, 0, 1, "AECb"),
            ("PF1", 0, 0, 2, "AEDA"),
            ("PF1", 0, 0, 3, "AAAc"),
        ]
        expected_aa_count = {
            ("A", "A"): 11,
            ("A", "E"): 9, 
            ("A", "C"): 3,
            ("A", "D"): 6, 
            ("C", "D"): 2,
            ("E", "E"): 2 
        }
        assert count_aa_by_column(data) == expected_aa_count