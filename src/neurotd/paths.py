"""Configurable locations. Importing this module creates no files.

Source checkouts default to <repository>/data. Wheel installations use
<working directory>/data unless NEUROTD_DATA_DIR is set before importing.
"""

import os
from pathlib import Path


def repository_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file() and (parent / "src/neurotd").is_dir():
            return parent
    return Path.cwd()


def data_path():
    if "NEUROTD_DATA_DIR" in os.environ:
        return Path(os.environ["NEUROTD_DATA_DIR"]).expanduser().resolve()
    if "NEUROTD_APP_EPHYS_GENE_DIR" in os.environ:
        return (Path(os.environ["NEUROTD_APP_EPHYS_GENE_DIR"]).expanduser() / "data").resolve()
    return repository_root() / "data"


def output_path():
    return Path(os.environ.get("NEUROTD_OUTPUT_DIR", repository_root() / "results")).expanduser().resolve()
