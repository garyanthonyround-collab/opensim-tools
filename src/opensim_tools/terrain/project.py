from dataclasses import dataclass
from pathlib import Path
from .os_grid import DEFAULT_DATASET, OSTile
from .mosaic import TerrainMosaic
from conftest import write_ascii_grid


@dataclass
class TerrainProject:
    dataset: Path = DEFAULT_DATASET
    centre_reference: str | None = None
    centre_point: tuple[int, int] | None = None
    size_m: int | None = None
    resolution_samples: int | None = None

    def resolution(self, samples: int):
        self.resolution_samples = samples
        return self

    def centre(self, reference: str):
        self.centre_reference = reference.upper()
        self.centre_point = self._parse_reference(reference)
        return self

    def size(self, metres: int):
        self.size_m = metres
        return self

    def _parse_reference(self, reference: str) -> tuple[int, int]:
        ref = reference.upper()

        if len(ref) != 6:
            raise ValueError(f"Invalid centre reference: {reference}")

        prefix = ref[:2]
        digits = ref[2:]

        if prefix != "NY" or not digits.isdigit():
            raise ValueError(f"Invalid centre reference: {reference}")

        east = int(digits[:2]) * 1000
        north = int(digits[2:]) * 1000

        return 300000 + east, 500000 + north

    def build(self):
        model = self.mosaic.to_model()

        min_x, min_y, max_x, max_y = self.bounds
        cellsize = model.header.get("cellsize", 1)

        crop_x = (min_x - model.header["xllcorner"]) // cellsize
        crop_y = (min_y - model.header["yllcorner"]) // cellsize
        crop_width = (max_x - min_x) // cellsize
        crop_height = (max_y - min_y) // cellsize

        return model.crop(crop_x, crop_y, crop_width, crop_height)

    @property
    def bounds(self):
        if self.centre_point is None:
            raise ValueError("Project centre has not been set")

        if self.size_m is None:
            raise ValueError("Project size has not been set")

        half = self.size_m // 2

        x, y = self.centre_point

        return (
            x - half,
            y - half,
            x + half,
            y + half,
        )

    @property
    def required_tile_references(self):
        min_x, min_y, max_x, max_y = self.bounds

        tile_min_x = min_x // 10000
        tile_max_x = (max_x - 1) // 10000
        tile_min_y = min_y // 10000
        tile_max_y = (max_y - 1) // 10000

        refs = []

        for tx in range(tile_min_x, tile_max_x + 1):
            for ty in range(tile_min_y, tile_max_y + 1):
                refs.append(self._tile_reference(tx, ty))

        return refs

    def _tile_reference(self, tile_x, tile_y):
        if not (30 <= tile_x <= 39 and 50 <= tile_y <= 59):
            raise ValueError("Only NY tile references are currently supported")

        return f"NY{tile_x - 30}{tile_y - 50}"

    @property
    def required_tiles(self):
        return [
            OSTile(reference, dataset=self.dataset)
            for reference in self.required_tile_references
        ]

    @property
    def mosaic(self):
        return TerrainMosaic.from_tiles(*self.required_tiles)
