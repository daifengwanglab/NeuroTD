"""Validation harness: restrict the final Figure 3 grid in memory, not in source.

Runs the unchanged preliminary figures and two original grid combinations:
(noise=0, W=129) and (noise=0.02, W=129). This is not a full-grid reproduction.
Pass either the pre-migration or migrated script to compare them identically.
"""

import argparse
import ast
import os
from pathlib import Path


class RestrictGrid(ast.NodeTransformer):
    def visit_Assign(self, node):
        if any(isinstance(target, ast.Name) and target.id == "param_grid" for target in node.targets):
            node.value = ast.parse("[(0.0, 129), (0.02, 129)]", mode="eval").body
        return self.generic_visit(node)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    script = args.script.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    tree = ast.fix_missing_locations(RestrictGrid().visit(ast.parse(script.read_text())))
    os.environ["MPLBACKEND"] = "Agg"
    os.chdir(output)
    exec(compile(tree, str(script), "exec"), {"__name__": "__main__", "__file__": str(script)})
