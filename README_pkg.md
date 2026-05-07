# mazegen

Reusable maze generation library for the A-Maze-ing 42 project.

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Basic Usage

```python
from mazegen import MazeGenerator

# Create and generate a perfect maze
gen = MazeGenerator(width=20, height=15, seed=42)
gen.generate(perfect=True)

# Access grid (list of lists of int bitmasks)
grid = gen.grid          # grid[row][col] = bitmask
print(gen.entry)         # (0, 0)
print(gen.exit)          # (19, 14)

# Access solution
path = gen.solution      # [(0,0), (1,0), ...]
dirs = gen.solution_as_directions()  # 'EESSNW...'
```

## Custom Parameters

```python
gen = MazeGenerator(
    width=30,
    height=20,
    entry=(0, 0),
    exit_=(29, 19),
    seed=1234,
    perfect=False,   # allows loops
)
gen.generate()
```

## Bitmask Format

Each cell in `grid[row][col]` encodes walls as bits:

| Bit | Direction | Value |
|-----|-----------|-------|
|  0  | North     |   1   |
|  1  | East      |   2   |
|  2  | South     |   4   |
|  3  | West      |   8   |

A bit of `1` means the wall is **closed**. Example: `0xF` (15) = all walls closed.