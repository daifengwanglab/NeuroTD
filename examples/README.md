# Example entry points

Install the package first (`python -m pip install -e .` from the checkout).
Use `python examples/run.py --help` for the paper-example launcher.

| Directory | Contents |
| --- | --- |
| `simulations/` | Figure 1 schematic, Figure 2 discrete delays, Figure 3 continuous delays, and two supplementary upsampling demonstrations |
| `ieeg/` | Figure 4; requires separately downloaded recordings |
| `patchseq/` | Figure 5 and raw-data preparation scripts |
| `legacy/` | Archived exploratory code with known missing dependencies; not a supported reproduction route |

The simulation and schematic files were moved without editing their contents.
Reusable plotting, signal-generation and application helpers remain in `neurotd`.
Example scripts are not importable library APIs: most execute work at top level.
Do not import every example to test package imports.

## Patch-seq workflow

For Figure 5 alone, use the supplied processed inputs and extract the expression
CSV following [data/README.md](../data/README.md). The preprocessing scripts are
only needed to regenerate those inputs:

1. `ephys_data_phase0_load_ephys_data_build_dict.py`: build NWB response/stimulus dictionaries.
2. `ephys_data_processing.py`: filter sweeps and calculate delay features.
3. `gene_expr_data_processing_XH.py`: prepare the expression tables (additional inputs required).
4. `fig5_app_ephys_gene.py`: correlate expression and electrophysiological features.

`ephys_data_phase0_load_ephys_data_temp_check_onesweep.py` is a diagnostic script,
not a prerequisite. Check paths and resource requirements before running raw-data
steps. Preserve stimulation, filtering and statistical parameters when reproducing
the original analysis. The enrichment step uses an external service manually;
the launcher does not upload gene lists.

## Preserved limitations

`legacy/simulation.py` imports the unavailable `neurotd.visualization` module.
`legacy/temp_demonstrate_why_this_method.py` imports the unavailable `app1` module
and contains exploratory sections requiring additional state. These pre-existing
issues are documented rather than fixed as part of a directory-only refactor.
Moving these scripts does not turn them into validated examples.
