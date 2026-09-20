import ast
import importlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_library_imports_from_this_checkout(self):
        import neurotd
        self.assertEqual(Path(neurotd.__file__).resolve().parent, ROOT / "src/neurotd")
        for module in ("utils", "neuro_signal", "time_varying_shift", "simulation_plotting",
                       "hiEEG_functions", "app_ephys_gene.core", "app_ephys_gene.plotting"):
            importlib.import_module("neurotd." + module)

    def test_package_contains_only_python_source(self):
        paths = [p for p in (ROOT / "src/neurotd").rglob("*")
                 if p.is_file() and "__pycache__" not in p.parts]
        self.assertTrue(paths)
        self.assertTrue(all(p.suffix == ".py" for p in paths))
        self.assertFalse(any(p.name.startswith("fig") for p in paths))

    def test_scripts_parse_without_executing_them(self):
        for path in (ROOT / "examples").rglob("*.py"):
            with self.subTest(path=path):
                ast.parse(path.read_text(), filename=str(path))

    def test_readme_images_exist(self):
        images = re.findall(r'<img src="([^"]+)"', (ROOT / "README.md").read_text())
        self.assertEqual(len(images), 3)
        for image in images:
            self.assertTrue((ROOT / image).is_file())

    def test_data_and_path_overrides(self):
        from neurotd import paths
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(paths.data_path(), ROOT / "data")
            self.assertEqual(paths.output_path(), ROOT / "results")
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            with patch.dict(os.environ, {"NEUROTD_DATA_DIR": str(base / "inputs"),
                                         "NEUROTD_OUTPUT_DIR": str(base / "outputs")}, clear=True):
                self.assertEqual(paths.data_path(), base / "inputs")
                self.assertEqual(paths.output_path(), base / "outputs")
                self.assertFalse((base / "inputs").exists())
                self.assertFalse((base / "outputs").exists())
            with patch.dict(os.environ, {"NEUROTD_APP_EPHYS_GENE_DIR": str(base)}, clear=True):
                self.assertEqual(paths.data_path(), base / "data")

    def test_metadata_fallback(self):
        from neurotd.app_ephys_gene import paths
        with patch.dict(os.environ, {"NEUROTD_DATA_DIR": str(ROOT / "data")}, clear=True):
            importlib.reload(paths)
            self.assertEqual(paths.META_FILE_PATH, ROOT / "data/processed/m1_patchseq_meta_data.csv")
            self.assertTrue(paths.META_FILE_PATH.is_file())
            self.assertTrue(paths.CVS_MAP_PATH.is_file())
        importlib.reload(paths)

    def test_launcher_help_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(ROOT / "examples/run.py"), "--help"],
                                    cwd=directory, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--headless", result.stdout)

    def test_launcher_rejects_data_as_output(self):
        result = subprocess.run([sys.executable, str(ROOT / "examples/run.py"), "fig2",
                                 "--output-dir", str(ROOT / "data/processed")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_identical_signals(self):
        from neurotd.time_varying_shift import compute_windowed_mse_with_hop
        x = np.random.default_rng(14).normal(size=512)
        centers, shifts = compute_windowed_mse_with_hop(x, x.copy(), 65, 32)
        self.assertGreater(len(centers), 0)
        np.testing.assert_array_equal(shifts, np.zeros_like(shifts))

    def test_known_shift(self):
        from neurotd.time_varying_shift import compute_windowed_mse_with_hop
        x = np.random.default_rng(14).normal(size=512)
        y = np.concatenate([np.zeros(7), x[:-7]])
        _, shifts = compute_windowed_mse_with_hop(x, y, 65, 32)
        np.testing.assert_array_equal(shifts, np.full_like(shifts, 7))

    def test_baseline_wrappers_return_finite_values(self):
        from neurotd.time_varying_shift import CTWShift, DTWShift, FFTShift
        from neurotd.utils import SlidingWindowPair
        x = np.random.default_rng(14).normal(size=129)
        for method in (DTWShift, CTWShift, FFTShift):
            pair = SlidingWindowPair(x, x.copy(), window_size=33, hop_size=16)
            estimator = method(pair, is_filter=False) if method is FFTShift else method(pair)
            self.assertEqual(estimator.shifts.shape, estimator.indices.shape)
            self.assertTrue(np.isfinite(estimator.shifts).all())
        # This is an interface smoke test, not a claim that every estimator is calibrated.


if __name__ == "__main__":
    unittest.main()
