import os
from pathlib import Path


def find_project_root(current_path: Path) -> Path:
    """
    Search upwards from the current path to find the project root.
    The project root is identified by the presence of the 'pyproject.toml' file.
    """
    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError("Project root with 'pyproject.toml' not found.")
