"""
Maze generation module using recursive backtracker (DFS) algorithm.

Each cell is represented as a bitmask integer:
  Bit 0 (1)  = North wall closed
  Bit 1 (2)  = East wall closed
  Bit 2 (4)  = South wall closed
  Bit 3 (8)  = West wall closed

A wall being closed means there is a wall (bit = 1).
"""

import random
from collections import deque
from typing import Optional


# Direction constants: (bit, dx, dy, opposite_bit)
NORTH = 0   # bit 0
EAST = 1    # bit 1
SOUTH = 2   # bit 2
WEST = 3    # bit 3

OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
DX = {NORTH: 0, SOUTH: 0, EAST: 1, WEST: -1}
DY = {NORTH: -1, SOUTH: 1, EAST: 0, WEST: 0}


class MazeGenerator:
    """
    Generates a maze using recursive backtracker (DFS) algorithm.

    Args:
        width: Number of columns (cells). Must be >= 5.
        height: Number of rows (cells). Must be >= 5.
        entry: (x, y) tuple for the entry cell. Defaults to (0, 0).
        exit_: (x, y) tuple for the exit cell. Defaults to (width-1, height-1).
        seed: Optional integer seed for reproducible generation.
        perfect: If True, generates a perfect maze (exactly one path between
                 any two cells). If False, some loops may be added.

    Example::

        from mazegen import MazeGenerator

        gen = MazeGenerator(width=20, height=15, seed=42)
        gen.generate(perfect=True)
        print(gen.entry)     # (0, 0)
        print(gen.exit)      # (19, 14)
        print(gen.solution)  # [(0,0), (1,0), ...]
        print(gen.grid[0])   # first row as list of hex bitmasks
    """

    NORTH = NORTH
    EAST = EAST
    SOUTH = SOUTH
    WEST = WEST

    def __init__(
        self,
        width: int = 20,
        height: int = 15,
        entry: tuple[int, int] = (0, 0),
        exit_: Optional[tuple[int, int]] = None,
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        """Initialize the MazeGenerator with configuration."""
        if width < 3 or height < 3:
            raise ValueError("Maze dimensions must be at least 3x3.")
        ex, ey = entry
        if not (0 <= ex < width and 0 <= ey < height):
            raise ValueError(f"Entry {entry} is outside maze bounds.")
        if exit_ is None:
            exit_ = (width - 1, height - 1)
        ox, oy = exit_
        if not (0 <= ox < width and 0 <= oy < height):
            raise ValueError(f"Exit {exit_} is outside maze bounds.")
        if entry == exit_:
            raise ValueError("Entry and exit must be different cells.")

        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit_
        self._seed = seed
        self._perfect = perfect
        self._rng = random.Random(seed)
        self._grid: list[list[int]] = []
        self._solution: list[tuple[int, int]] = []
        self._pattern_cells: set[tuple[int, int]] = set()
        self._generated = False

    @property
    def width(self) -> int:
        """Maze width in cells."""
        return self._width

    @property
    def height(self) -> int:
        """Maze height in cells."""
        return self._height

    @property
    def entry(self) -> tuple[int, int]:
        """Entry cell (x, y)."""
        return self._entry

    @property
    def exit(self) -> tuple[int, int]:
        """Exit cell (x, y)."""
        return self._exit

    @property
    def grid(self) -> list[list[int]]:
        """
        2D grid of bitmask integers [row][col].
        Must call generate() first.
        """
        if not self._generated:
            raise RuntimeError("Call generate() before accessing grid.")
        return self._grid

    @property
    def solution(self) -> list[tuple[int, int]]:
        """
        Shortest path from entry to exit as list of (x,y) tuples.
        Must call generate() first.
        """
        if not self._generated:
            raise RuntimeError("Call generate() before accessing solution.")
        return self._solution

    @property
    def pattern_cells(self) -> set[tuple[int, int]]:
        """
        Set of (x,y) cells that belong to the '42' pattern.
        Must call generate() first.
        """
        if not self._generated:
            raise RuntimeError(
                "Call generate() before accessing pattern_cells."
            )
        return self._pattern_cells

    def generate(self, perfect: Optional[bool] = None) -> None:
        """
        Generate the maze.

        Args:
            perfect: Override the perfect flag set at init if provided.
        """
        if perfect is not None:
            self._perfect = perfect
        self._rng = random.Random(self._seed)
        self._grid = self._init_full_walls()

        self._place_42_pattern()
        self._dfs_generate()
        if not self._perfect:
            self._add_loops()
        self._seal_borders()
        self._seal_42_pattern()
        self._ensure_open_entry_exit()
        self._solution = self._bfs_solve()
        self._generated = True

    def _init_full_walls(self) -> list[list[int]]:
        """Initialize grid with all walls closed (0xF = 15)."""
        return [[0xF] * self._width for _ in range(self._height)]

    def _remove_wall(self, x: int, y: int, direction: int) -> None:
        """Remove a wall between cell (x,y) and its neighbor in direction."""
        self._grid[y][x] &= ~(1 << direction)
        nx, ny = x + DX[direction], y + DY[direction]
        self._grid[ny][nx] &= ~(1 << OPPOSITE[direction])

    def _has_wall(self, x: int, y: int, direction: int) -> bool:
        """Return True if cell (x,y) has a wall in given direction."""
        return bool(self._grid[y][x] & (1 << direction))

    def _in_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) is within maze bounds."""
        return 0 <= x < self._width and 0 <= y < self._height

    def _dfs_generate(self) -> None:
        """Generate maze using iterative DFS (recursive backtracker)."""
        visited: list[list[bool]] = [
            [False] * self._width for _ in range(self._height)
        ]

        # Pre-mark 42 pattern cells as visited (obstacles)
        for (px, py) in self._pattern_cells:
            if 0 <= px < self._width and 0 <= py < self._height:
                visited[py][px] = True

        ex, ey = self._entry
        if visited[ey][ex]:
            raise RuntimeError("Entry cell is inside the 42 pattern.")
        stack: list[tuple[int, int]] = [(ex, ey)]
        visited[ey][ex] = True

        while stack:
            x, y = stack[-1]
            dirs = [NORTH, EAST, SOUTH, WEST]
            self._rng.shuffle(dirs)
            moved = False
            for d in dirs:
                nx, ny = x + DX[d], y + DY[d]
                if self._in_bounds(nx, ny) and not visited[ny][nx]:
                    self._remove_wall(x, y, d)
                    visited[ny][nx] = True
                    stack.append((nx, ny))
                    moved = True
                    break
            if not moved:
                stack.pop()

        # Ensure 42 pattern cells remain fully closed after DFS
        for (px, py) in self._pattern_cells:
            if 0 <= px < self._width and 0 <= py < self._height:
                self._grid[py][px] = 0xF

    def _seal_borders(self) -> None:
        """Ensure all border cells have outer walls closed."""
        for x in range(self._width):
            self._grid[0][x] |= (1 << NORTH)
            self._grid[self._height - 1][x] |= (1 << SOUTH)
        for y in range(self._height):
            self._grid[y][0] |= (1 << WEST)
            self._grid[y][self._width - 1] |= (1 << EAST)

    def _seal_42_pattern(self) -> None:
        """Reinforce 42 cells and mark orphaned cells as part of pattern."""
        for (px, py) in self._pattern_cells:
            if 0 <= px < self._width and 0 <= py < self._height:
                self._grid[py][px] = 0xF

        # Find any non-pattern cells enclosed by the 42 pattern
        # by flood-filling from entry and collecting 0xF cells not visited
        visited: set[tuple[int, int]] = set()
        stack = [self._entry]
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for d in [NORTH, EAST, SOUTH, WEST]:
                nx, ny = x + DX[d], y + DY[d]
                if self._in_bounds(nx, ny) and not self._has_wall(x, y, d):
                    if (nx, ny) not in visited:
                        stack.append((nx, ny))

        for y in range(self._height):
            for x in range(self._width):
                if (x, y) not in visited and (x, y) not in self._pattern_cells:
                    self._grid[y][x] = 0xF
                    self._pattern_cells.add((x, y))

    def _add_loops(self) -> None:
        """Add some random wall removals to create loops (imperfect maze)."""
        num_loops = (self._width * self._height) // 10
        for _ in range(num_loops):
            x = self._rng.randint(0, self._width - 1)
            y = self._rng.randint(0, self._height - 1)
            if (x, y) in self._pattern_cells:
                continue
            dirs = [NORTH, EAST, SOUTH, WEST]
            self._rng.shuffle(dirs)
            for d in dirs:
                nx, ny = x + DX[d], y + DY[d]
                if not self._in_bounds(nx, ny):
                    continue
                if (nx, ny) in self._pattern_cells:
                    continue
                if self._has_wall(x, y, d):
                    self._remove_wall(x, y, d)
                    break

    def _ensure_open_entry_exit(self) -> None:
        """Make sure entry/exit cells are reachable."""
        ex, ey = self._entry
        ox, oy = self._exit
        # entry: open a wall toward the interior if completely blocked
        self._open_cell_if_needed(ex, ey)
        self._open_cell_if_needed(ox, oy)

    def _open_cell_if_needed(self, x: int, y: int) -> None:
        """Open at least one interior-facing wall if all closed."""
        directions = [NORTH, EAST, SOUTH, WEST]
        self._rng.shuffle(directions)
        for d in directions:
            nx, ny = x + DX[d], y + DY[d]
            if self._in_bounds(nx, ny):
                if self._has_wall(x, y, d):
                    self._remove_wall(x, y, d)
                return

    def _place_42_pattern(self) -> None:
        """Embed the '42' digit pattern as fully-closed cells in the maze.
        The pattern is placed in the upper-left quadrant.
        Cells belonging to '42' have all 4 walls closed.
        """
        pattern_w = 11
        pattern_h = 7
        if self._width < pattern_w + 4 or self._height < pattern_h + 4:
            print(
                "Warning: Maze too small to embed '42' pattern. "
                "Minimum size is at least 15x11."
            )
            return

        start_x = 2
        start_y = 2
        self._pattern_cells = set()

        four = [
            "  X  ",
            " XX  ",
            "X X  ",
            "XXXXX",
            "  X  ",
            "  X  ",
            "  X  ",
        ]
        two = [
            "XXXXX",
            "    X",
            "    X",
            "XXXXX",
            "X    ",
            "X    ",
            "XXXXX",
        ]

        for row_idx, row in enumerate(four):
            for col_idx, ch in enumerate(row):
                if ch == 'X':
                    cy = start_y + row_idx
                    cx = start_x + col_idx
                    if 0 <= cx < self._width and 0 <= cy < self._height:
                        self._grid[cy][cx] = 0xF
                        self._pattern_cells.add((cx, cy))

        offset_x = 6
        for row_idx, row in enumerate(two):
            for col_idx, ch in enumerate(row):
                if ch == 'X':
                    cy = start_y + row_idx
                    cx = start_x + offset_x + col_idx
                    if 0 <= cx < self._width and 0 <= cy < self._height:
                        self._grid[cy][cx] = 0xF
                        self._pattern_cells.add((cx, cy))

    def _bfs_solve(self) -> list[tuple[int, int]]:
        """
        Find shortest path from entry to exit using BFS.

        Returns:
            List of (x, y) tuples forming the path, or [] if no path.
        """
        ex, ey = self._entry
        ox, oy = self._exit
        if (ex, ey) == (ox, oy):
            return [(ex, ey)]

        queue: deque[tuple[int, int]] = deque([(ex, ey)])
        parent: dict[tuple[int, int], Optional[tuple[int, int]]] = {
            (ex, ey): None
        }

        while queue:
            x, y = queue.popleft()
            if (x, y) == (ox, oy):
                break
            for d in [NORTH, EAST, SOUTH, WEST]:
                if not self._has_wall(x, y, d):
                    nx, ny = x + DX[d], y + DY[d]
                    if (nx, ny) not in parent:
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

        if (ox, oy) not in parent:
            return []

        # Reconstruct path
        path: list[tuple[int, int]] = []
        cur: Optional[tuple[int, int]] = (ox, oy)
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path

    def solution_as_directions(self) -> str:
        """
        Return solution path as a string of N/E/S/W characters.

        Returns:
            String like 'EESSWN...'
        """
        if not self._solution or len(self._solution) < 2:
            return ""
        dir_map = {
            (0, -1): 'N',
            (1, 0): 'E',
            (0, 1): 'S',
            (-1, 0): 'W',
        }
        result = []
        for i in range(len(self._solution) - 1):
            x0, y0 = self._solution[i]
            x1, y1 = self._solution[i + 1]
            result.append(dir_map[(x1 - x0, y1 - y0)])
        return "".join(result)
