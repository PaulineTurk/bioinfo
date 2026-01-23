import sqlite3
from typing import Iterable
from data.models import PfamBlock
from pathlib import Path


class DatabaseBlosumStore:

    def __init__(self, db_path:str):
        path = Path(db_path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        self.conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sequence (
            pfam TEXT,
            id TEXT,
            seq TEXT,
            PRIMARY KEY (pfam, id)
        )
        """)
        self.conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_sequence_id ON sequence (id)
        """)
                
        self.conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pairwise_identity (
            pfam TEXT,
            id1 TEXT,
            id2 TEXT,
            identity INTEGER,
            PRIMARY KEY (pfam, id1, id2)
        )
        """)

        self.conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_pairwise_pfam
        ON pairwise_identity (pfam)
        """)

        
        self.conn.commit()

    def insert_sequences(
        self,
        block: PfamBlock
    ):
        self.conn.executemany(
            "INSERT OR REPLACE INTO sequence VALUES (?,?,?)",
            ((block.accession, id, seq) for id, seq in block.sequences.items())
        )
        self.conn.commit()

    def insert_pairwise_identity(
        self,
        pfam: str,
        rows: Iterable[tuple[str, str, int]]
    ):
        self.conn.executemany(
            "INSERT OR REPLACE INTO pairwise_identity VALUES (?,?,?,?)",
            ((pfam, id1, id2, identity) for id1, id2, identity in rows)
        )
        self.conn.commit()
    
    #TODO: add test
    def get_all_pfam(self)-> set[str]:
        query = "SELECT DISTINCT pfam FROM sequence"
        cursor =  self.conn.execute(query)
        return {row[0] for row in cursor.fetchall()}
    



    def init_cluster(self, threshold: int):
        table_name = f"cluster_{threshold}"
        self.conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            pfam TEXT,
            id INTEGER,
            seq_id TEXT,
            weight REAL,
            PRIMARY KEY (pfam, seq_id)
            )
        """)
        self.conn.commit()

    def save_cluster(self, pfam: str, threshold: int, clusters:list[set[str]], weights:dict[str, float]):
        table_name = f"cluster_{threshold}"
        data = []
        for id, cluster in enumerate(clusters):
            for seq_id in cluster:
                data.append((pfam, id, seq_id, weights[seq_id]))
        self.conn.executemany(f"""
        INSERT OR REPLACE INTO {table_name} 
            (pfam, id, seq_id, weight)
            VALUES (?,?,?,?)
            """, data     
            )
        self.conn.commit()

    #TODO: refactor with get_all_pfam
    def get_all_pairwise_identity(self, pfam: str):
        query = f"SELECT pfam, id1, id2, identity FROM pairwise_identity WHERE pfam=?"
        cursor = self.conn.execute(query, (pfam, ))
        return {row for row in cursor.fetchall()}
    

    #TODO: to delete
    def get_random_representatives_with_seq(self, threshold: int):
        table_name = f"cluster_{threshold}"
        query = f"""
            SELECT pfam, id, seq_id, seq
            FROM (
                SELECT c.pfam, c.id, c.seq_id, s.seq
                FROM {table_name} c
                JOIN sequence s
                ON c.seq_id = s.id
                AND c.pfam = s.pfam
                ORDER BY RANDOM()
            )
            GROUP BY pfam, id;
        """
        cursor = self.conn.execute(query)
        return cursor.fetchall()
    
    def get_clusters(self, threshold: int):
        table_name = f"cluster_{threshold}"
        query = f"""
            SELECT pfam, id, seq_id, weight, seq
            FROM (
                SELECT c.pfam, c.id, c.seq_id, c.weight, s.seq
                FROM {table_name} c
                JOIN sequence s
                ON c.seq_id = s.id
                AND c.pfam = s.pfam
            )
        """
        cursor = self.conn.execute(query)
        return cursor.fetchall()
        