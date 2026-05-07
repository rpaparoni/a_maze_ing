"""
Terminal ASCII display for A-Maze-ing.

Renders the maze using block characters in a colored terminal.
Provides an interactive menu for re-generation, path toggle, and color change.
"""

import os
import sys
from typing import Callable, Optional

from mazegen import MazeGenerator

RESET = "\033[0m"
BOLD = "\033[1m"

WALL_COLORS = [
    "\033[47m",
    "\033[43m",
    "\033[42m",
    "\033[44m",
    "\033[41m",
    "\033[45m",
]
WALL_COLOR_NAMES = ["White", "Yellow", "Green", "Blue", "Red", "Magenta"]

PATH_COLOR = "\033[46m"
ENTRY_COLOR = "\033[45m"
EXIT_COLOR = "\033[41m"
PATTERN_COLOR = "\033[43m"
FLOOR_COLOR = "\033[40m"


def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def render_maze(
    gen: MazeGenerator,
    wall_color_idx: int = 0,
    show_path: bool = False,
    show_pattern: bool = False,
) -> str:
    W: int = gen.width
    H: int = gen.height
    grid = gen.grid
    path_set: set[tuple[int, int]] = set()
    if show_path:
        path_set = set(gen.solution)
    pattern_set: set[tuple[int, int]] = set()
    if show_pattern:
        try:
            pattern_set = gen.pattern_cells
        except RuntimeError:
            pattern_set = set()

    wall_col = WALL_COLORS[wall_color_idx % len(WALL_COLORS)]

    pixel_rows = 2 * H + 1
    pixel_cols = 2 * W + 1

    pixels: list[list[str]] = [
        ['wall'] * pixel_cols for _ in range(pixel_rows)
    ]

    for y in range(H):
        for x in range(W):
            px, py = 2 * x + 1, 2 * y + 1
            if (x, y) in pattern_set:
                pixels[py][px] = 'pattern'
            elif (x, y) == gen.entry:
                pixels[py][px] = 'entry'
            elif (x, y) == gen.exit:
                pixels[py][px] = 'exit'
            elif show_path and (x, y) in path_set:
                pixels[py][px] = 'path'
            else:
                pixels[py][px] = 'open'

    for y in range(H):
        for x in range(W):
            cell = grid[y][x]
            px, py = 2 * x + 1, 2 * y + 1
            if not (cell & 1):
                pixels[py - 1][px] = 'open'
                if show_path and (x, y) in path_set and (x, y - 1) in path_set:
                    pixels[py - 1][px] = 'path'
            if not (cell & 2):
                pixels[py][px + 1] = 'open'
                if show_path and (x, y) in path_set and (x + 1, y) in path_set:
                    pixels[py][px + 1] = 'path'
            if not (cell & 4):
                pixels[py + 1][px] = 'open'
                if show_path and (x, y) in path_set and (x, y + 1) in path_set:
                    pixels[py + 1][px] = 'path'
            if not (cell & 8):
                pixels[py][px - 1] = 'open'
                if show_path and (x, y) in path_set and (x - 1, y) in path_set:
                    pixels[py][px - 1] = 'path'

    use_color = _supports_color()
    lines: list[str] = []

    for row in pixels:
        line = ""
        for ptype in row:
            if use_color:
                if ptype == 'wall':
                    line += wall_col + "  " + RESET
                elif ptype == 'path':
                    line += PATH_COLOR + "  " + RESET
                elif ptype == 'entry':
                    line += ENTRY_COLOR + "  " + RESET
                elif ptype == 'exit':
                    line += EXIT_COLOR + "  " + RESET
                elif ptype == 'pattern':
                    line += PATTERN_COLOR + "  " + RESET
                else:
                    line += FLOOR_COLOR + "  " + RESET
            else:
                if ptype == 'wall':
                    line += "##"
                elif ptype == 'path':
                    line += ".."
                elif ptype == 'entry':
                    line += "EN"
                elif ptype == 'exit':
                    line += "EX"
                elif ptype == 'pattern':
                    line += "42"
                else:
                    line += "  "
        lines.append(line)

    return "\n".join(lines)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def interactive_display(
    gen: MazeGenerator,
    on_regenerate: Callable[[], Optional[MazeGenerator]],
) -> None:
    wall_color_idx = 0
    show_path = False
    show_pattern = False

    while True:
        clear_screen()
        print(render_maze(gen, wall_color_idx, show_path, show_pattern))
        print()
        title = (
            f"{BOLD}==== A-Maze-ing ===={RESET}"
            if _supports_color()
            else "==== A-Maze-ing ===="
        )
        print(title)
        print("1. Re-generate a new maze")
        print(f"2. {'Hide' if show_path else 'Show'} path from entry to exit")
        print(f"3. {'Hide' if show_pattern else 'Show'} 42 pattern highlight")
        color_name = WALL_COLOR_NAMES[wall_color_idx % len(WALL_COLORS)]
        print(f"4. Rotate maze wall colors (current: {color_name})")
        print("5. Quit")
        print()
        choice = input("Choice? (1-5): ").strip()

        if choice == "1":
            new_gen = on_regenerate()
            if new_gen is not None:
                gen = new_gen
                show_path = False
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            show_pattern = not show_pattern
        elif choice == "4":
            wall_color_idx += 1
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Press Enter to continue.")
            input()
