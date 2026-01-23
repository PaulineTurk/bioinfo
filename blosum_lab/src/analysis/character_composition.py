from collections import Counter
from data.stockholm_format import METADATA_STARTER, BLOCK_ENDING
from config import load_config

config =  load_config(is_test=False)

def collect_characters(file_name: str) -> Counter:
    counter = Counter()
    with open(file_name) as file:
        for line in file:
            line = line.rstrip()
            if not line or line.startswith(METADATA_STARTER) or line.startswith(BLOCK_ENDING):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            seq = parts[1]
            counter.update(seq)

    return counter

print(collect_characters(config.PFAM_PATH))