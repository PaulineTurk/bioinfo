from typing import Iterator, Dict
from data.models import PfamBlock
from data.stockholm_format import *

def is_sequence(line:str) -> bool:
    return bool(line) and not line.startswith(METADATA_STARTER) and not line.startswith(BLOCK_ENDING)

def build_pfam_blocks(file_name: str) -> Iterator[PfamBlock]:
    current_accession: str|None = None
    sequences: Dict[str, str] = {}

    with open(file_name) as file:
        for raw_line in file:
            line = raw_line.rstrip()
            if line.startswith(ACCESSION_STARTING_CODE):
                current_accession = line.split()[ACCESSION_POSITION]
            elif current_accession and is_sequence(line):
                seq_id, seq = line.split(maxsplit=SEQUENCE_LINE_FRACTION)
                sequences[seq_id] = seq
            elif line == BLOCK_ENDING:
                yield PfamBlock(current_accession, sequences)
                current_accession = None
                sequences = {}
                        

def count_pfam_blocks(file_name: str) -> int:
    count = 0
    with open(file_name) as file:
        for raw_line in file:
            if raw_line.startswith(ACCESSION_STARTING_CODE):
                count += 1
    return count