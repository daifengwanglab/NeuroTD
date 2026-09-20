# Repository migration and validation

This reorganization separates the importable package, runnable paper examples,
input data and generated results. It does not change delay estimators, statistical
methods, random seeds or the simulation grids.

## Migration map

All paths below are relative to the repository root.

| Previous location | New location |
| --- | --- |
| `src/neurotd/fig1_scheme_xy_curves_freeform_.py` | `examples/simulations/fig1_scheme_xy_curves_freeform_.py` |
| `src/neurotd/fig2_simulation_discrete_shift.py` | `examples/simulations/fig2_simulation_discrete_shift.py` |
| `src/neurotd/fig3_simulation_continuous_shift.py` | `examples/simulations/fig3_simulation_continuous_shift.py` |
| `src/neurotd/simulation_upsampling*.py` | `examples/simulations/` (same filenames) |
| `src/neurotd/app_iEEG/fig4_app_iEEG.py` | `examples/ieeg/fig4_app_iEEG.py` |
| `src/neurotd/app_ephys_gene/fig5_app_ephys_gene.py` and four preprocessing scripts | `examples/patchseq/` (same filenames) |
| `src/neurotd/simulation.py` and `temp_demonstrate_why_this_method.py` | `examples/legacy/` (same filenames) |
| `src/neurotd/app_ephys_gene/data/processed/` | `data/processed/` |
| `src/neurotd/img/` | `docs/assets/` |

Reusable modules remain under `src/neurotd/`, including the Patch-seq `core`,
`plotting` and path helpers. Existing `import neurotd` library imports remain
available. Old script paths change; use `python examples/run.py fig2 --headless`
or the other figure names described in the root README.

## Path and packaging changes

- The launcher runs each example in `results/<figure>/` by default. Existing
  output files can be overwritten on rerun; select a fresh `--output-dir` to
  retain previous results.
- iEEG input uses `--ieeg-dir` or `NEUROTD_IEEG_DIR`, replacing a machine-specific
  recording path. Raw recordings are not downloaded automatically.
- Shared data and output helpers support `NEUROTD_DATA_DIR` and
  `NEUROTD_OUTPUT_DIR`. The legacy `NEUROTD_APP_EPHYS_GENE_DIR` data-root override
  remains supported. See `data/README.md` for the precise layout.
- Patch-seq metadata falls back to the metadata already shipped with the
  repository. Output directories are created where needed.
- Example scripts and datasets are not installed as package modules or package
  data. Run paper examples from a checkout. Figure 1 has an optional
  `python-pptx` dependency (`pip install -e '.[examples]'`).
- Generated results, virtual environments and raw inputs are ignored by Git.
  The four already-published processed data files are explicitly allowlisted.

## Validation performed

The comparison baseline was upstream commit
`1a6c4f23818bcfe3152f947c54c553a92edeca0c`. Before and after runs used Python
3.12.14 and the same numerical dependency environment on macOS. A separate local
editable installation was used for the reorganized checkout.

| Check | Result |
| --- | --- |
| Offline unit tests (`python -m unittest discover -s tests -v`) | 11 tests passed |
| Figure 2 full grid, 11 noise levels by 6 window sizes | All 66 result rows and columns exactly equal before and after; CSV bytes also equal |
| Figure 3 reduced grid: noise 0 and 0.02, window 129 | Both result rows and all columns exactly equal before and after |
| Five moved simulation/schematic scripts | Byte-identical to baseline |
| Four moved data files and five moved images | Byte-identical to baseline |
| Wheel build | Succeeded; wheel excludes data, images and example entry points |

The Figure 3 comparison uses `tests/run_continuous_smoke.py`. This validation-only
harness replaces the grid assignment in memory; it does not edit the example or
change its estimators. The full Figure 3 grid was **not** completed as part of
this validation. To run the unchanged full experiment, use the standard launcher.

## Scope and limitations

- Raw iEEG and raw Patch-seq analyses were not reproduced: they require external
  recordings, local data preparation and substantially greater resources.
  Figure 5's processed-data analysis was not run in this validation either.
- The schematic and legacy exploratory scripts were not execution-tested.
  Legacy scripts retain missing historical dependencies, as documented in
  `examples/README.md`; they are preserved for reference, not advertised as
  supported examples.
- Baseline-wrapper smoke tests check output shape and finiteness, not scientific
  correctness. This change does not repair or endorse CTW/FFT implementations,
  reassess comparative performance or revise manuscript novelty claims.
- Exact agreement verifies that the checked simulation outputs were preserved
  by this reorganization; it is not an independent validation of the paper's
  conclusions or a guarantee across other dependency versions.
