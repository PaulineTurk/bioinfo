from dataclasses import dataclass


@dataclass(frozen=True)
class BlosumConfig:
    PFAM_URL:str = "https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.seed.gz"
    PFAM_PATH:str = "./blosum_lab/src/Pfam-A.seed"
    DB_PATH :int = "./blosum_lab/src/db/blosum.db"
    RESULT_DIRECTORY: str = "./blosum_lab/src/result"
    IDENTITY_THRESHOLD:float = 62
    MIN_PFAM_SIZE: int = 10
    ROUNDING_BLOSUM_STANDARD = 2

    @classmethod
    def load_test_config(self):
        return self(
            PFAM_PATH = "./blosum_lab/test/Pfam-A_test.seed",
            DB_PATH = "./blosum_lab/test/db/blosum_test.db",
            RESULT_DIRECTORY = "./blosum_lab/test/result"
        )
    
def load_config(is_test:bool):
    return  BlosumConfig.load_test_config() if is_test else BlosumConfig()
    