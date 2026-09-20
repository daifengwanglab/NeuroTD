"""Run a paper example with generated files isolated from source and input data."""

import argparse
import os
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = {
    "fig1": "simulations/fig1_scheme_xy_curves_freeform_.py",
    "fig2": "simulations/fig2_simulation_discrete_shift.py",
    "fig3": "simulations/fig3_simulation_continuous_shift.py",
    "fig4": "ieeg/fig4_app_iEEG.py",
    "fig5": "patchseq/fig5_app_ephys_gene.py",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("example", choices=SCRIPTS)
    parser.add_argument("--output-dir", type=Path, help="Defaults to results/<example> in the checkout")
    parser.add_argument("--data-dir", type=Path, help="Data root containing processed/ and raw/")
    parser.add_argument("--ieeg-dir", type=Path, help="DANDI 000574 directory containing sub-* folders")
    parser.add_argument("--headless", action="store_true", help="Save figures without opening GUI windows")
    args = parser.parse_args()
    output = (args.output_dir or ROOT / "results" / args.example).expanduser().resolve()
    from neurotd.paths import data_path
    data = args.data_dir.expanduser().resolve() if args.data_dir else data_path()
    protected = [ROOT / "src", ROOT / "examples", ROOT / "docs", ROOT / "data", data, ROOT / ".git"]
    if output == ROOT or any(output == path or path in output.parents for path in protected):
        parser.error("Choose an output directory outside source, examples, documentation and input data.")
    if args.data_dir:
        os.environ["NEUROTD_DATA_DIR"] = str(data)
    if args.ieeg_dir:
        os.environ["NEUROTD_IEEG_DIR"] = str(args.ieeg_dir.expanduser().resolve())
    os.environ["NEUROTD_OUTPUT_DIR"] = str(output)
    if args.headless:
        os.environ["MPLBACKEND"] = "Agg"
    output.mkdir(parents=True, exist_ok=True)
    script = Path(__file__).resolve().parent / SCRIPTS[args.example]
    print(f"Running {script.name}; output directory: {output}", flush=True)
    os.chdir(output)
    sys.argv = [str(script)]
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
