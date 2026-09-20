# Data inputs

Only the four processed files already published in the original repository are
tracked here. Moving them does not change their content, provenance or licensing.
Do not add patient recordings, private metadata, credentials or unpublished data.
The allowlist in `.gitignore` excludes raw recordings and additional generated data.

## Included Patch-seq files (`processed/`)

- `cell_name_to_cell_id_and_sample_id.csv`: cell/sample mapping used by the scripts.
- `m1_patchseq_meta_data.csv`: supplied metadata (tab-delimited despite its suffix).
- `time_delays_all_cells.csv`: previously computed sweep-level delay features.
- `gxp_total_log2_filtered_pc.zip`: compressed processed gene-expression CSV.

Figure 5 reads the uncompressed `gxp_total_log2_filtered_pc.csv`. From the repository
root, inspect the archive and extract it without overwriting an existing CSV:

```bash
unzip -l data/processed/gxp_total_log2_filtered_pc.zip
unzip -n data/processed/gxp_total_log2_filtered_pc.zip -d data/processed
```

The extracted CSV is deliberately not tracked. Source dataset: mouse motor cortex
Patch-seq, Scala et al., linked by the original project to
[DANDI 000008](https://dandiarchive.org/dandiset/000008).
Full preprocessing additionally expects gene-count/length tables, a protein-coding
gene list, and the source metadata described in `gene_expr_data_processing_XH.py`.
These inputs are not all shipped with this repository.

## External iEEG recordings

Source: Boran et al., [DANDI 000574](https://dandiarchive.org/dandiset/000574).
Download the required sessions separately and preserve their filenames and subject
directory structure. The directory supplied via `NEUROTD_IEEG_DIR` or the launcher's
`--ieeg-dir` must directly contain `sub-01/`, etc. The default is `data/raw/000574/`.
The current script retains its original subject/session settings (subject 1,
sessions 1, 2 and 3) and serial execution. Check required files before running.
The loader's original session-ordering behavior is unchanged.

## Configuration

Set environment variables before importing application modules:

| Variable | Meaning | Default in a source checkout |
| --- | --- | --- |
| `NEUROTD_DATA_DIR` | Data root containing `raw/` and `processed/` | `<repository>/data` |
| `NEUROTD_OUTPUT_DIR` | Results root | `<repository>/results` |
| `NEUROTD_IEEG_DIR` | Directory containing iEEG subject folders | `<data>/raw/000574` |
| `NEUROTD_META_FILE` | Explicit Patch-seq metadata file | Raw metadata if present, otherwise the supplied processed copy |

The legacy `NEUROTD_APP_EPHYS_GENE_DIR` variable is supported as an application root
whose `data/` child is used when `NEUROTD_DATA_DIR` is absent. In wheel installations,
the default data root is `<current working directory>/data`; explicit configuration
is recommended. No data or image files are included in the Python wheel.

Raw Patch-seq scripts expect NWB files under `<data>/raw/raw_data_ephys/` and can
create large intermediate pickles under `<data>/raw/raw_data_ephys_dict/`.
The original script documents a roughly 20 GB response pickle. Do not run that
pipeline on a small machine without checking memory and storage requirements.
Preprocessing may overwrite processed files; use a separate `NEUROTD_DATA_DIR`
when recomputing them. No download, extraction or raw-data processing runs on import
of the package path-configuration modules.
