from data.pfam_blocks import count_pfam_blocks, build_pfam_blocks
from alignment.identity import compute_identity_on_block
from storage.sqlite import DatabaseBlosumStore
from tqdm import tqdm

def run(pfam_file: str, db_file: str):
    store = DatabaseBlosumStore(db_file)
    blocks_count = count_pfam_blocks(pfam_file)
    stream = build_pfam_blocks(pfam_file)

    for block in tqdm(stream, total=blocks_count, desc="Pfam identity running"):
        rows = compute_identity_on_block(block)
        store.insert_pairwise_identity(block.accession, rows)
