from pathlib import Path

DEFAULT_DATASET = Path("/srv/gis/os-terrain50/data")


def tile_to_path(tile: str, dataset=DEFAULT_DATASET) -> Path:
    """
    Convert an OS Terrain 50 tile reference into a file path.

    Example:
        NY43 -> /srv/gis/os-terrain50/data/ny/NY43.asc
    """
    tile = tile.upper()

    if len(tile) != 4:
        raise ValueError(f"Invalid tile '{tile}'")

    prefix = tile[:2].lower()

    return dataset / prefix / f"{tile}.asc"


def tile_exists(tile: str) -> bool:
    return tile_to_path(tile).exists()


def tile_origin(tile: str):
    """
    Return National Grid origin for the tile.

    Placeholder for now.
    """
    raise NotImplementedError
