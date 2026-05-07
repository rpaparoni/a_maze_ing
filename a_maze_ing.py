#!/usr/bin/env python3
"""Main entry point for A-Maze-ing maze generator."""

import sys
from typing import Optional

from config_parser import Config, parse_config, ConfigError
from mazegen import MazeGenerator
from maze_writer import write_maze, WriterError
from display import interactive_display


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
    except ConfigError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    gen = _create_maze(config)
    if gen is None:
        sys.exit(1)

    try:
        write_maze(gen, config.output_file)
        print(f"Maze written to {config.output_file}")
    except WriterError as e:
        print(f"Output error: {e}")
        sys.exit(1)

    try:
        interactive_display(gen, lambda: _create_maze(config))
    except KeyboardInterrupt:
        print("\nGoodbye!")


def _create_maze(config: Config) -> Optional[MazeGenerator]:
    try:
        gen = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit_=config.exit_,
            seed=config.seed,
            perfect=config.perfect,
        )
        gen.generate()
        return gen
    except ValueError as e:
        print(f"Generation error: {e}")
        return None


if __name__ == "__main__":
    main()
