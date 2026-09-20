import os
from pathlib import Path

from neurotd.paths import data_path, output_path, repository_root

DATA_PATH = data_path()
DATA_PROCESSED_PATH = DATA_PATH / "processed"
RESULT_PATH = output_path()
FIGURE_PATH = RESULT_PATH / "figures"

# Compatibility aliases, no longer tied to a particular workstation.
GOOGLE_DRIVE_ROOT = DATA_PATH.parent
DROPBOX_APP_PATH = repository_root()

CVS_MAP_PATH = DATA_PROCESSED_PATH / "cell_name_to_cell_id_and_sample_id.csv"
_raw_meta = DATA_PATH / "raw/patchseq-Scala/data/m1_patchseq_meta_data.csv"
META_FILE_PATH = Path(os.environ["NEUROTD_META_FILE"]).expanduser().resolve() if "NEUROTD_META_FILE" in os.environ else (
    _raw_meta if _raw_meta.is_file() else DATA_PROCESSED_PATH / "m1_patchseq_meta_data.csv"
)
