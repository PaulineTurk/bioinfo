from data.data_import import load_pfam_online
from data.pfam_blocks import count_pfam_blocks, build_pfam_blocks
from storage.sqlite import DatabaseBlosumStore
from tqdm import tqdm

def run(pfam_url:str, pfam_file: str, db_file:str):
    load_pfam_online(pfam_url, pfam_file)
    store = DatabaseBlosumStore(db_file)
    blocks_count = count_pfam_blocks(pfam_file)
    stream = build_pfam_blocks(pfam_file)

    for block in tqdm(stream, total=blocks_count, desc="Saving Pfam in db"):
        store.insert_sequences(block)
