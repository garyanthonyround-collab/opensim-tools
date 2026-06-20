from dataclasses import dataclass
from pathlib import Path

DEFAULT_DATASET = Path("/srv/gis/os-terrain50/data")


@dataclass(frozen=True)
class OSTile:
    reference: str
    dataset: Path = DEFAULT_DATASET

    def __post_init__(self):
        ref = self.reference.upper()
        if len(ref) != 4 or not ref[:2].isalpha() or not ref[2:].isdigit():
            raise ValueError(f"Invalid OS Terrain 50 tile reference: {self.reference}")
        object.__setattr__(self, "reference", ref)

    @property
    def path(self) -> Path:
        return self.dataset / self.reference[:2].lower() / f"{self.reference}.asc"

    @property
    def exists(self) -> bool:
        return self.path.exists()


def tile_to_path(tile: str, dataset=DEFAULT_DATASET) -> Path:
    return OSTile(tile, dataset=dataset).path


def tile_exists(tile: str) -> bool:
    return OSTile(tile).exists
