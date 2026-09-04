"""Print pyproject.toml's [project.dependencies], one per line, minus nninteractive-client.

Used by the Dockerfile to install the declared dependencies without asking pip
to resolve nninteractive-client (already installed from the bundled ./client
source -- see the comment above the `pip install ./client` step).

The dependencies array in pyproject.toml is valid Python list syntax (TOML's
comment/trailing-comma rules match Python's here), so it's parsed with
ast.literal_eval instead of a TOML library -- no extra dependency, no
Python-version constraint.
"""

import ast
import pathlib
import re
import sys

pyproject = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "pyproject.toml").read_text()
match = re.search(r"dependencies = (\[.*?\n\])", pyproject, re.S)
deps = ast.literal_eval(match.group(1))
for dep in deps:
    if not dep.startswith("nninteractive-client"):
        print(dep)
