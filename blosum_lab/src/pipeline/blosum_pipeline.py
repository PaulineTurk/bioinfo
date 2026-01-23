from config import load_config
from pipeline import clustering_pipeline, database_initialisation_pipeline, identity_pipeline, computing_pipeline

config =  load_config(is_test=False)
pfam_url = config.PFAM_URL
pfam_path = config.PFAM_PATH
db_path = config.DB_PATH
threshold = config.IDENTITY_THRESHOLD
pairwise_count_file = f"{config.RESULT_DIRECTORY}/{threshold}/aa_pairwise_count"
blosum_like_path = f"{config.RESULT_DIRECTORY}/{threshold}/blosum"
reference_matrix = f"BLOSUM{threshold}"
matrix_difference_path = f"{config.RESULT_DIRECTORY}/{threshold}/blosum_difference"


database_initialisation_pipeline.run(pfam_url, pfam_path, db_path)
identity_pipeline.run(pfam_path, db_path)
clustering_pipeline.run(threshold, db_path)
computing_pipeline.run(db_path, threshold, pairwise_count_file, blosum_like_path, reference_matrix, matrix_difference_path)


