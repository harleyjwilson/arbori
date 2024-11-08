from pathlib import Path
import tomllib

import click

from arbori.io import build_directory_structure, parse_input_file
from arbori.tree import Tree


def _get_version():
    """Read version from pyproject.toml"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


@click.version_option(_get_version(), prog_name="arbori")
@click.command(help="Create a directory structure given a simple input format")
@click.argument("input", type=click.File("r"))
@click.argument(
    "output",
    type=click.Path(exists=True, file_okay=False, readable=True, path_type=Path),
)
def arbori(input, output):
    """
    Create a directory structure from a tree-like format file.

    INPUT: Path to input file containing the tree structure
    OUTPUT: Path to output directory where the structure will be created
    """
    input_contents = input.read()
    processed_lines = parse_input_file(input_contents)

    tree = Tree(output.resolve().name, processed_lines)

    build_directory_structure(tree.root, output.resolve().parent)
