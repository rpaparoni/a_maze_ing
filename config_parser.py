"""
Configuration file parser for A-Maze-ing.

Reads KEY=VALUE pairs from a plain text file.
Lines starting with '#' are treated as comments.
"""

import os


REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


class ConfigError(Exception):
    """Raised when the configuration file is invalid."""
    pass


class Config:
    """
    Holds parsed maze configuration.

    Attributes:
        width: Maze width in cells.
        height: Maze height in cells.
        entry: (x, y) entry cell.
        exit_: (x, y) exit cell.
        output_file: Path to the output file.
        perfect: Whether to generate a perfect maze.
        seed: Optional random seed for reproducibility.
        algorithm: Optional algorithm name (default: 'dfs').
    """

    def __init__(self) -> None:
        """Initialize with default values."""
        self.width: int = 0
        self.height: int = 0
        self.entry: tuple[int, int] = (0, 0)
        self.exit_: tuple[int, int] = (0, 0)
        self.output_file: str = "maze.txt"
        self.perfect: bool = True
        self.seed: int | None = None
        self.algorithm: str = "dfs"


def parse_config(filepath: str) -> Config:
    """
    Parse a maze configuration file.

    Args:
        filepath: Path to the configuration file.

    Returns:
        A Config object with all parsed values.

    Raises:
        ConfigError: If the file is missing, malformed, or has invalid values.
    """
    if not os.path.isfile(filepath):
        raise ConfigError(f"Configuration file not found: '{filepath}'")

    raw: dict[str, str] = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigError(
                        f"Line {lineno}: invalid format "
                        f"(expected KEY=VALUE): {line!r}"
                    )
                key, _, value = line.partition("=")
                key = key.strip().upper()
                value = value.strip()
                raw[key] = value
    except OSError as e:
        raise ConfigError(f"Cannot read configuration file: {e}") from e

    # Check required keys
    missing = REQUIRED_KEYS - raw.keys()
    if missing:
        raise ConfigError(
            f"Missing required configuration keys: "
            f"{', '.join(sorted(missing))}"
        )

    cfg = Config()

    # Parse WIDTH and HEIGHT
    cfg.width = _parse_positive_int(raw, "WIDTH")
    cfg.height = _parse_positive_int(raw, "HEIGHT")
    if cfg.width < 3 or cfg.height < 3:
        raise ConfigError("WIDTH and HEIGHT must both be at least 3.")

    # Parse ENTRY
    cfg.entry = _parse_coords(raw, "ENTRY", cfg.width, cfg.height)

    # Parse EXIT
    cfg.exit_ = _parse_coords(raw, "EXIT", cfg.width, cfg.height)

    if cfg.entry == cfg.exit_:
        raise ConfigError("ENTRY and EXIT must be different cells.")

    # Parse OUTPUT_FILE
    cfg.output_file = raw["OUTPUT_FILE"]
    if not cfg.output_file:
        raise ConfigError("OUTPUT_FILE cannot be empty.")

    # Parse PERFECT
    perfect_str = raw["PERFECT"].lower()
    if perfect_str not in ("true", "false"):
        raise ConfigError(
            f"PERFECT must be 'True' or 'False', got: {raw['PERFECT']!r}"
        )
    cfg.perfect = perfect_str == "true"

    # Parse optional SEED
    if "SEED" in raw:
        try:
            cfg.seed = int(raw["SEED"])
        except ValueError:
            raise ConfigError(f"SEED must be an integer, got: {raw['SEED']!r}")

    # Parse optional ALGORITHM
    if "ALGORITHM" in raw:
        cfg.algorithm = raw["ALGORITHM"].lower()
        if cfg.algorithm not in ("dfs", "prim", "kruskal"):
            raise ConfigError(
                f"ALGORITHM must be 'dfs', 'prim', or 'kruskal', "
                f"got: {raw['ALGORITHM']!r}"
            )

    return cfg


def _parse_positive_int(raw: dict[str, str], key: str) -> int:
    """Parse a mandatory positive integer from raw config dict."""
    try:
        value = int(raw[key])
    except ValueError:
        raise ConfigError(f"{key} must be an integer, got: {raw[key]!r}")
    if value <= 0:
        raise ConfigError(f"{key} must be a positive integer, got: {value}")
    return value


def _parse_coords(
    raw: dict[str, str], key: str, width: int, height: int
) -> tuple[int, int]:
    """Parse a mandatory X,Y coordinate from raw config dict."""
    val = raw[key]
    parts = val.split(",")
    if len(parts) != 2:
        raise ConfigError(
            f"{key} must be in format 'x,y', got: {val!r}"
        )
    try:
        x, y = int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ConfigError(
            f"{key} coordinates must be integers, got: {val!r}"
        )
    if not (0 <= x < width and 0 <= y < height):
        raise ConfigError(
            f"{key} ({x},{y}) is outside maze bounds ({width}x{height})."
        )
    return (x, y)
