from pathlib import Path
import shutil
from urllib.request import urlretrieve
import gzip

def load_pfam_online(url :str, file_path: str):
    path = Path(file_path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        gz_path = path.with_suffix(".gz")
        urlretrieve(url, gz_path)
        with gzip.open(gz_path, "rb") as file_in:
            with open(path, "wb") as file_out:
                shutil.copyfileobj(file_in, file_out)
        gz_path.unlink()