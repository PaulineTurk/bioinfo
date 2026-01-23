from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class PfamBlock:
    accession: str
    sequences: Dict[str, str] #[id, seq]
