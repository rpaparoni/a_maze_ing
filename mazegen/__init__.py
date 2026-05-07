"""
mazegen - A reusable maze generation library.

Basic usage::

    from mazegen import MazeGenerator

    gen = MazeGenerator(width=20, height=15, seed=42)
    gen.generate(perfect=True)

    # Access maze grid (list of lists of int bitmasks)
    grid = gen.grid

    # Access solution path
    path = gen.solution   # list of (x, y) tuples

    # Access entry/exit
    print(gen.entry, gen.exit)
"""

from .generator import MazeGenerator

__all__ = ["MazeGenerator"]
