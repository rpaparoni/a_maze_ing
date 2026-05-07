"""
Maze output file writer for A-Maze-ing.

Writes the maze grid in hexadecimal format (one hex digit per cell),
followed by an empty line, then entry coords, exit coords, and shortest path.
"""

from mazegen import MazeGenerator


class WriterError(Exception):
    """Raised when the output file cannot be written."""
    pass


def write_maze(gen: MazeGenerator, output_file: str) -> None:
    """
    Write the generated maze to a file.

    Format:
      - One row per line, one hex digit per cell (uppercase).
      - Empty line.
      - Entry coordinates: "x,y"
      - Exit coordinates: "x,y"
      - Shortest path as N/E/S/W string.

    Args:
        gen: A MazeGenerator with generate() already called.
        output_file: Path to write the output file.

    Raises:
        WriterError: If the file cannot be written.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            # Write grid rows
            for row in gen.grid:
                line = "".join(format(cell, 'X') for cell in row)
                f.write(line + "\n")
            # Empty line
            f.write("\n")
            # Entry
            ex, ey = gen.entry
            f.write(f"{ex},{ey}\n")
            # Exit
            ox, oy = gen.exit
            f.write(f"{ox},{oy}\n")
            # Path as N/E/S/W
            f.write(gen.solution_as_directions() + "\n")
    except OSError as e:
        raise WriterError(
            f"Cannot write output file '{output_file}': {e}"
        ) from e
