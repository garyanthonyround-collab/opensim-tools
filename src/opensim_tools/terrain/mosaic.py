import numpy as np

from dataclasses import dataclass, field

from .os_grid import OSTile

from .ascii_grid import read_ascii_grid

from .model import TerrainModel

@dataclass
class TerrainMosaic:
    tiles: list[OSTile] = field(default_factory=list)

    @classmethod
    def from_tiles(cls, *tile_refs):
        mosaic = cls()
        for tile_ref in tile_refs:
            mosaic.add_tile(tile_ref)
        return mosaic

    def add_tile(self, tile_ref):
        tile = tile_ref if isinstance(tile_ref, OSTile) else OSTile(tile_ref)
        self.tiles.append(tile)
        return self

    @property
    def references(self):
        return [tile.reference for tile in self.tiles]

    @property
    def paths(self):
        return [tile.path for tile in self.tiles]

    def missing_tiles(self):
        return [tile for tile in self.tiles if not tile.exists]

    def validate(self):
        missing = self.missing_tiles()
        if missing:
            refs = ", ".join(tile.reference for tile in missing)
            raise FileNotFoundError(f"Missing OS Terrain 50 tiles: {refs}")
        return self

    @property
    def extent(self):
        self.validate()

        bounds = [tile.bounds for tile in self.tiles]

        min_x = min(b[0] for b in bounds)
        min_y = min(b[1] for b in bounds)
        max_x = max(b[2] for b in bounds)
        max_y = max(b[3] for b in bounds)

        return min_x, min_y, max_x, max_y

    def to_model(self) -> TerrainModel:
        self.validate()

        loaded = []

        for tile in self.tiles:
            header, data = read_ascii_grid(tile.path)

            x = int(header["xllcorner"])
            y = int(header["yllcorner"])

            loaded.append((x, y, data))

        if not loaded:
            raise ValueError("Cannot create terrain model from an empty mosaic")

        shapes = {data.shape for _, _, data in loaded}

        if len(shapes) != 1:
            raise ValueError("All mosaic tiles must have the same dimensions")

        tile_height, tile_width = shapes.pop()

        xs = sorted({x for x, _, _ in loaded})
        ys = sorted({y for _, y, _ in loaded}, reverse=True)

        rows = len(ys)
        cols = len(xs)

        if rows * cols != len(loaded):
            raise ValueError("Mosaic tiles do not form a complete rectangular grid")

        output = np.empty(
            (rows * tile_height, cols * tile_width),
            dtype=loaded[0][2].dtype,
        )

        lookup = {(x, y): data for x, y, data in loaded}

        for row, y in enumerate(ys):
            for col, x in enumerate(xs):
                origin = (x, y)

                if origin not in lookup:
                    raise ValueError(f"Missing tile at origin {origin}")

                output[
                    row * tile_height:(row + 1) * tile_height,
                    col * tile_width:(col + 1) * tile_width,
                ] = lookup[origin]

        return TerrainModel(
            {
                "ncols": output.shape[1],
                "nrows": output.shape[0],
                "xllcorner": min(xs),
                "yllcorner": min(ys),
                "cellsize": 50,
                "nodata_value": -9999,
            },
            output,
        )
