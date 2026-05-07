"""Tests for mazegen package."""

from mazegen import MazeGenerator


def test_generate_perfect_maze() -> None:
    gen = MazeGenerator(width=10, height=10, seed=42)
    gen.generate(perfect=True)
    assert gen.width == 10
    assert gen.height == 10
    assert len(gen.grid) == 10
    assert len(gen.grid[0]) == 10
    assert len(gen.solution) > 0
    assert gen.solution[0] == gen.entry
    assert gen.solution[-1] == gen.exit


def test_generate_imperfect_maze() -> None:
    gen = MazeGenerator(width=10, height=10, seed=42)
    gen.generate(perfect=False)
    assert len(gen.solution) > 0


def test_solution_as_directions() -> None:
    gen = MazeGenerator(width=10, height=10, seed=42)
    gen.generate()
    dirs = gen.solution_as_directions()
    assert all(c in "NESW" for c in dirs)
    assert len(dirs) > 0


def test_minimum_size() -> None:
    gen = MazeGenerator(width=3, height=3, seed=42)
    gen.generate()
    assert len(gen.grid) == 3


def test_invalid_dimensions() -> None:
    try:
        MazeGenerator(width=2, height=2)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_42_pattern() -> None:
    gen = MazeGenerator(width=20, height=15, seed=42)
    gen.generate()
    assert len(gen.pattern_cells) > 0


def test_reproducibility() -> None:
    gen1 = MazeGenerator(width=10, height=10, seed=123)
    gen1.generate()
    gen2 = MazeGenerator(width=10, height=10, seed=123)
    gen2.generate()
    assert gen1.grid == gen2.grid
    assert gen1.solution == gen2.solution


def test_entry_exit_inside_bounds() -> None:
    gen = MazeGenerator(width=5, height=5, entry=(2, 2), exit_=(4, 4), seed=42)
    gen.generate()
    assert gen.entry == (2, 2)
    assert gen.exit == (4, 4)
